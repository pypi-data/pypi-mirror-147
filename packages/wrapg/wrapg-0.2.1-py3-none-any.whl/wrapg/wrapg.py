import os
from collections.abc import Iterable
import psycopg
from psycopg import sql, errors
import pandas as pd
from wrapg import util, snippet


# ===========================================================================
#  ?                                wrapg
#  @author         :  jturnercode
#  @createdOn      :  2/24/2022
#  @description    :  Wrapper around pyscopg (version 3). Use to easily run sql
# functions inside python code to interact with postgres database.
# Inspired by dataset library that wraps sqlalchemy
# ================================= TODO ================================
# TODO: Can query() return explain analyse info?
# TODO: Conditionally import config?
# TODO: Implement delete
# ===========================================================================

# TODO: Add proper exceptions if parameters are missing or do not work
# TODO: expose conn_import in init.py as class to easily modify attributes?? vs dict?
conn_import: dict = {
    "user": os.environ.get("PG_USER"),
    "password": os.environ.get("PG_PASSWORD"),
    "host": os.environ.get("PG_HOST"),
    "dbname": os.environ.get("PG_DBNAME"),
    "port": os.environ.get("PG_PORT"),
}


def query(raw_sql: str, to_df=False, conn_kwargs: dict = None):
    """Function to send raw sql query to postgres db.

    Args:
        raw_sql (str): sql query in string form.
        to_df (bool, optional): Return results of query in dataframe. Defaults to False.
        conn_kwargs (dict, optional): Specify/overide conn kwargs. See full list of options,
        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS.
        Defaults to None, recommend importing via .env file.

    Returns:
        _type_: iterator or Dataframe
    """

    # Initialize conn_kwargs to empty dict if no arguments passed
    # Merge args into conn_final
    if conn_kwargs is None:
        conn_kwargs = {}

    # Final connection args to pass to connect()
    # Set default return type (row factory) to dictionary, can be overwritten with kwargs
    conn_final = {"row_factory": psycopg.rows.dict_row, **conn_import, **conn_kwargs}

    # Connect to an existing database
    with psycopg.connect(**conn_final) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # Pass raw_sql to execute()
            # example: cur.execute("SELECT * FROM tablename WHERE id = 4")
            cur.execute(query=raw_sql)

            # Used for testing output of raw_sql
            # print("rowcount: ", cur.rowcount)
            # print("statusmessage: ", cur.statusmessage)
            # print(cur)

            # .statusmessage returns string of type of operation processed
            # If 'select' in status message return records as df or iter
            if "SELECT" in cur.statusmessage:
                if to_df is True:
                    return pd.DataFrame(cur, dtype="object")

                # Save memory return iterator
                return iter(cur.fetchall())


def insert(data: Iterable[dict] | pd.DataFrame, table: str, conn_kwargs: dict = None):

    """Function for SQL's INSERT

    Add a row(s) into specified table

    Args:
        data (Iterable[dict] | pd.DataFrame): data in form of dict, list of dict, or dataframe
        table (str): name of database table
        conn_kwargs (dict, optional): Specify/overide conn kwargs. See full list of options,
        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS.
        Defaults to None, recommend importing via .env file.
    """

    columns, rows, uniform = util.data_transform(data)

    # Initialize conn_kwargs to empty dict if no arguments passed
    # Merge args into conn_final
    if conn_kwargs is None:
        conn_kwargs = {}

    # Final conn args to pass to connect()
    conn_final = {**conn_import, **conn_kwargs}

    # Connect to an existing database
    with psycopg.connect(**conn_final) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # Typ insert statement format
            # INSERT INTO table (col1, col2) VALUES (300, "vehicles");

            if uniform == 1:
                # Dynamic insert query for dictionaries
                qry = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(table),
                    sql.SQL(", ").join(map(sql.Identifier, columns)),
                    sql.SQL(", ").join(map(sql.Placeholder, columns)),
                    # Dynamic insert query for list of tuples
                    # sql.SQL(", ").join(sql.Placeholder() * len(columns)),
                )
                # print(qry.as_string(conn))
                # One insert for all dictionaries
                cur.executemany(query=qry, params_seq=rows)

            else:
                # For non uniform data
                for row in rows:
                    # Dynamic insert query for dictionaries
                    qry = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                        sql.Identifier(table),
                        sql.SQL(", ").join(map(sql.Identifier, tuple(row))),
                        sql.SQL(", ").join(map(sql.Placeholder, tuple(row))),
                    )
                    # Seperate insert for each dictionary
                    cur.execute(query=qry, params=row)

            # Make the changes to the database persistent
            conn.commit()


def insert_ignore(
    data: Iterable[dict] | pd.DataFrame,
    table: str,
    keys: list,
    conn_kwargs: dict = None,
):
    """Function for SQL's INSERT ON CONFLICT DO NOTHING

    Add a row into specified table if the row with specified keys does not already exist.
    If rows with matching keys exist no change is made.
    Automatically creates unique index if one does not exist for keys provided.

    Args:
        data (Iterable[dict] | pd.DataFrame): data in form of dict, list of dict, or dataframe
        table (str): name of database table
        keys (list): Iterable of columns
        conn_kwargs (dict, optional): Specify/overide conn kwargs. See full list of options,
        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS.
        Defaults to None, recommend importing via .env file.
    """

    # Inspect data and return columns and rows
    columns, rows, uniform = util.data_transform(data)

    # Initialize conn_kwargs to empty dict if no arguments passed
    # Merge args into conn_final
    if conn_kwargs is None:
        conn_kwargs = {}

    # Final conn parameters to pass to connect()
    # Set return default type to dictionary, can be overwritten with kwargs
    conn_final = {**conn_import, **conn_kwargs}

    # Connect to an existing database
    with psycopg.connect(**conn_final) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # =================== Ignore_Insert Qry ==================
            # INSERT INTO table (name, email)
            # VALUES('Dave','dave@yahoo.com')
            # ON CONFLICT (name)
            # DO NOTHING;

            try:
                # uniform column names thru data submitted
                if uniform == 1:
                    # get sql qry based on passed parameters
                    qry = snippet.insert_ignore_snip(
                        table=table, columns=columns, keys=keys
                    )
                    # print(qry.as_string(conn))
                    cur.executemany(query=qry, params_seq=rows)

                else:
                    for row in rows:
                        # get sql qry based on passed parameters for each row
                        qry = snippet.insert_ignore_snip(
                            table=table, columns=tuple(row), keys=keys
                        )
                        # print(qry.as_string(conn))
                        cur.execute(query=qry, params=row)

            # Catch no unique constriant error
            except errors.InvalidColumnReference as e:
                print(">>> Error: ", e)
                print("> Rolling back, attempt creation of new constriant...")
                conn.rollback()

                try:
                    # Create new unique index & try insert_ignore again
                    uix_sql = snippet.create_unique_index(table=table, keys=keys)
                    # print(uix_sql.as_string(conn))
                    cur.execute(query=uix_sql)

                    if uniform == 1:
                        qry = snippet.insert_ignore_snip(
                            table=table, columns=columns, keys=keys
                        )
                        # Now execute previous insert_ignore statement
                        cur.executemany(query=qry, params_seq=rows)

                    else:
                        for row in rows:
                            qry = snippet.insert_ignore_snip(
                                table=table, columns=tuple(row), keys=keys
                            )
                            # print(qry.as_string(conn))
                            cur.execute(query=qry, params=row)

                except Exception as indx_error:
                    print(">>> Error: ", indx_error)
                    quit()

            # Handle all other exceptions, not InvalidColumn Reference
            except Exception as ee:
                print("Exception: ", ee.__init__)
                quit()

            # Make the changes to the database persistent
            conn.commit()


def upsert(
    data: Iterable[dict] | pd.DataFrame,
    table: str,
    keys: list,
    conn_kwargs: dict = None,
):
    """Function for SQL's INSERT ON CONFLICT DO UPDATE SET

    Add a row into specified table if the row with specified keys does not already exist.
    If rows with matching keys exist, update row values.
    Automatically creates unique index if one does not exist for keys provided.

    Args:
        data (Iterable[dict] | pd.DataFrame): data in form of dict, list of dict, or dataframe
        table (str): name of database table
        keys (list): Iterable of columns
        conn_kwargs (dict, optional): Specify/overide conn kwargs. See full list of options,
        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS.
        Defaults to None, recommend importing via .env file.
    """

    # Inspect data and return columns and rows
    columns, rows, uniform = util.data_transform(data)

    # Initialize conn_kwargs to empty dict if no arguments passed
    # Merge args into conn_final
    if conn_kwargs is None:
        conn_kwargs = {}

    # Final conn parameters to pass to connect()
    # Set return default type to dictionary, can be overwritten with kwargs
    conn_final = {**conn_import, **conn_kwargs}

    # Connect to an existing database
    with psycopg.connect(**conn_final) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # =================== Upsert Qry ==================
            # INSERT INTO table (name, email)
            # VALUES('Dave','dave@yahoo.com')
            # ON CONFLICT (name)
            # DO UPDATE SET email=excluded.email
            # WHERE ...;

            try:
                if uniform == 1:
                    qry = snippet.upsert_snip(table=table, columns=columns, keys=keys)
                    # print(qry.as_string(conn))
                    cur.executemany(query=qry, params_seq=rows)

                else:
                    for row in rows:
                        # Note tupe(row) returns column keys for each record
                        qry = snippet.upsert_snip(
                            table=table, columns=tuple(row), keys=keys
                        )
                        # print(qry.as_string(conn))
                        cur.execute(query=qry, params=row)

            # Catch no unique index error
            except errors.InvalidColumnReference as e:
                print(">>> Error: ", e)
                print(f"> Creating unique index for {keys}...")
                # !important, cannot attempt other operations after error unless rollback()
                conn.rollback()

                try:
                    # Create unique index & try upsert again
                    uix_sql = snippet.create_unique_index(table=table, keys=keys)
                    print(uix_sql.as_string(conn))
                    cur.execute(query=uix_sql)

                    if uniform == 1:
                        qry = snippet.upsert_snip(
                            table=table, columns=columns, keys=keys
                        )
                        # print(qry.as_string(conn))
                        cur.executemany(query=qry, params_seq=rows)

                    else:
                        for row in rows:
                            # Note tupe(row) returns column keys for each record
                            qry = snippet.upsert_snip(
                                table=table, columns=tuple(row), keys=keys
                            )
                            # print(qry.as_string(conn))
                            cur.execute(query=qry, params=row)

                except Exception as indx_error:
                    print(">>> Error: ", indx_error)
                    quit()

            # Handle all other exceptions
            except Exception as ee:
                print("Exception: ", ee.__init__)
                quit()

            # Make the changes to the database persistent
            conn.commit()


"""
# TODO: **upsert without creating auto-index or constriants
**Add as option to exisiting upsert(auto_uix=False)
def upsert_wo_idx():
    Sudo code
    This function would be run inside a for loop within a transaction
    every iteration would result in a update or an insert

    try:
        update() on keys
        if update() return value is 0
        then insert()
    this code should be much slower but not require creating
    unique constriants which may be hard to manage especially
    for novice users
"""

# ================================= UPDATE Function ================================
def update(
    data: list[dict] | pd.DataFrame,
    table: str,
    keys: Iterable,
    conn_kwargs: dict = None,
):
    """Function for SQL's UPDATE

    If rows with matching keys exist, update row values.
    The columns that do not appear in the 'data' retain their original values.
    Make sure data has keys specified in function.

    Args:
        data (list[dict] | pd.DataFrame): data in form of dict, list of dict, or dataframe
        table (str): name of database table
        keys (Iterable): Iterable of column names synonymous with sql WHERE
        conn_kwargs (dict, optional): Specify/overide conn kwargs. See full list of options,
        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS.
        Defaults to None, recommend importing via .env file.
    """

    # Inspect data and return columns and rows
    columns, rows, uniform = util.data_transform(data)

    # Initialize conn_kwargs to empty dict if no arguments passed
    # Merge args into conn_final
    if conn_kwargs is None:
        conn_kwargs = {}

    # Final conn parameters to pass to connect()
    # Set return default type to dictionary, can be overwritten with kwargs
    conn_final = {**conn_import, **conn_kwargs}

    # Connect to an existing database
    with psycopg.connect(**conn_final) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # =================== Update Qry ===================
            # UPDATE table_name
            # SET column1 = value1,
            #     column2 = value2,
            #     ...
            # TODO: Where clause is optional, add code if None update all
            # WHERE column = value, ...
            # RETURNING * | output_expression AS output_name;

            # Function to compose col=value sql str
            def column_value_str(column_names: Iterable):
                """Create psycopg composable sql string for
                variable number of columns/value pairs
                ie column=value scenerios, col=%(col)s

                Args:
                    column_names (Iterable): column names
                """
                # function used to map to column names
                def set_sql(col):
                    return sql.SQL("{}={}").format(
                        sql.Identifier(col),
                        sql.Placeholder(col),
                    )

                return map(set_sql, column_names)

            if uniform == 1:
                # print("> Uniform Data..")
                qry = sql.SQL("UPDATE {} SET {} WHERE {}").format(
                    sql.Identifier(table),
                    sql.SQL(", ").join(column_value_str(columns)),
                    sql.SQL(", ").join(column_value_str(keys)),
                )
                # print(qry.as_string(conn))

                cur.executemany(query=qry, params_seq=rows)
            else:
                # print(">> Non-Uniform Data...")
                for row in rows:
                    qry = sql.SQL("UPDATE {} SET {} WHERE {}").format(
                        sql.Identifier(table),
                        sql.SQL(", ").join(column_value_str(tuple(row))),
                        sql.SQL(", ").join(column_value_str(keys)),
                    )

                    cur.execute(query=qry, params=row)

            # Make the changes to the database persistent
            conn.commit()


def create_table(table: str, columns: dict, conn_kwargs: dict = None):
    """Function creating table.

    Args:
        table (str): name of new table
        columns (dict): dictionary of column name, datatype, contraints. See example below
        conn_kwargs (dict, optional): Specify/overide conn kwargs. See full list of options,
        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS.
        Defaults to None, recommend importing via .env file.

    Example:
        cols = dict(id="serial", name="varchar(75) unique not null", age="int")
        create_table(table="mytable", columns=cols)

    Returns:
        _type_: None
    """

    # Initialize conn_kwargs to empty dict if no arguments passed
    # Merge args into conn_final
    if conn_kwargs is None:
        conn_kwargs = {}

    # Final connection args to pass to connect()
    # Set default return type (row factory) to dictionary, can be overwritten with kwargs
    conn_final = {**conn_import, **conn_kwargs}

    # Connect to an existing database
    with psycopg.connect(**conn_final) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # TODO: Add optional table constriants to function
            # =================== Create Table Qry ===================
            # CREATE TABLE [IF NOT EXISTS] table_name (
            # column1 datatype(length) column_contraint,
            # column2 datatype(length) column_contraint,
            # column3 datatype(length) column_contraint,
            # table_constraints
            # );

            # Function to compose 'colname datatype constriant' sql str
            def define_column(column_info: dict):
                """Create psycopg composable sql string for
                defining columns within postgres table
                ie column_name datatype(length) column_constriant

                Args:
                    column_pairs (Iterable): column names
                """
                # function used to map to column names
                def col_sql(col, value):
                    # return sql.SQL(f'"{col}" {value.upper()}')
                    return sql.SQL("{} {}").format(
                        sql.Identifier(col), sql.SQL(value.upper())
                    )

                return [col_sql(k, v) for k, v in column_info.items()]

            qry = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
                sql.Identifier(table),
                sql.SQL(", ").join(define_column(columns)),
            )
            # print(qry.as_string(conn))

            cur.execute(query=qry)

            # Make the changes to the database persistent
            conn.commit()


def copy_from_csv(
    table: str,
    csv_file: str,
    header: bool = False,
    block_size=50_000,
    conn_kwargs: dict = None,
):
    # TODO: Account for using other data from Iterable of sequence like list(tuples)
    # TODO: Can i return the number of copied rows per postgres standard
    # TODO: Auto create table based on csv, use pandas(chunk), translate data types
    """Copy .csv data to table using postgres copy protocol.

    Args:
        table (str): table name to run copy command on
        csv_file (str): csv file path
        header (bool): True indicates file has header and will ignore it.
        conn_kwargs (dict, optional): Specify/overide conn kwargs. See full list of options,
        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS.
        Defaults to None, recommend importing via .env file.

    Returns:
        _type_: None
    """

    # Initialize conn_kwargs to empty dict if no arguments passed
    # Merge args into conn_final
    if conn_kwargs is None:
        conn_kwargs = {}

    # Final connection args to pass to connect()
    # Set default return type (row factory) to dictionary, can be overwritten with kwargs
    conn_final = {**conn_import, **conn_kwargs}

    # Connect to an existing database
    with psycopg.connect(**conn_final) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            #! SPECIFIC COLUMNS NOT WORKING; Open ticket with pyscopg?
            # =================== Copy Qry ===================
            # "COPY cust (name, age) FROM STDIN WITH (FORMAT csv)"

            # If csv has header
            if header:
                copy_sql = sql.SQL(
                    "COPY {} FROM STDIN WITH (FORMAT csv, HEADER TRUE)"
                ).format(sql.Identifier(table))
            else:
                copy_sql = sql.SQL("COPY {} FROM STDIN WITH (FORMAT csv)").format(
                    sql.Identifier(table)
                )

                # used for write_row(); list of tuples
                # copy_sql = sql.SQL("COPY {} FROM STDIN").format(sql.Identifier(table))

            with open(csv_file, "r") as f:
                # see postgres copy options
                # https://www.postgresql.org/docs/current/sql-copy.html

                with cur.copy(copy_sql) as copy:

                    # Using blocks/chunks
                    while data := f.read(block_size):
                        copy.write(data)

                    # # Use write_row() for list(tuples) or iterable of sequences
                    # #! Do not specify COPY options such as FORMAT CSV, DELIMITER, NULL
                    # t = [("bill", 50, "here"), ("ronnie", 50, "there")]
                    # for ff in t:
                    #     copy.write_row(ff)


# ================================= Delete_where Function ================================
def delete(table: str, where: dict, conn_kwargs: dict = None):
    """Function for SQL's Delete.

    Delete rows from the specified table that match 'where' condition, column=value dictionary.
    Function can accept sql function on the column_name.
    Note: Use 'clear_table()' if want to delete all records in table.

    Args:
        table (str): name of database table
        where (dict): column=value dictionary which specifies rows to be removed.
        ex. where=dict(name='Matthew', email='fake@email.com')
        ex. w/sql function where={'customer': 'Ethan', 'MONTH(timestamp_column)': '2'}
        conn_kwargs (dict, optional): Specify/overide conn kwargs. See full list of options,
        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS.
        Defaults to None, recommend importing via .env file.
    """

    # Initialize conn_kwargs to empty dict if no arguments passed
    # Merge args into conn_final
    if conn_kwargs is None:
        conn_kwargs = {}

    # Final conn parameters to pass to connect()
    # Set return default type to dictionary, can be overwritten with kwargs
    conn_final = {**conn_import, **conn_kwargs}

    # Connect to an existing database
    with psycopg.connect(**conn_final) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # =================== Delete Qry ===================
            # DELETE FROM table_name
            # WHERE condition---> id = 7 and badge in (2,4)
            # RETURNING (select_list | *);

            qry = snippet.delete_snip(table=table, where=where)
            # print(qry.as_string(conn))

            cur.execute(query=qry)

            # Make the changes to the database persistent
            conn.commit()


# ================================= Clear_table Function ================================
def clear_table(table: str, conn_kwargs: dict = None):
    """!!Caution!! Function for SQL's Delete used to delete 'ALL' records in specified table.
    
    Args:
        table (str): name of database table
        conn_kwargs (dict, optional): Specify/overide conn kwargs. See full list of options,
        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS.
        Defaults to None, recommend importing via .env file.
    """

    # Initialize conn_kwargs to empty dict if no arguments passed
    # Merge args into conn_final
    if conn_kwargs is None:
        conn_kwargs = {}

    # Final conn parameters to pass to connect()
    # Set return default type to dictionary, can be overwritten with kwargs
    conn_final = {**conn_import, **conn_kwargs}

    # Connect to an existing database
    with psycopg.connect(**conn_final) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # =================== Delete ALL Records Qry ===================
            # DELETE FROM table_name;

            qry = sql.SQL("DELETE FROM {};").format(sql.Identifier(table))
            # print(qry.as_string(conn))

            cur.execute(query=qry)

            # Make the changes to the database persistent
            conn.commit()
