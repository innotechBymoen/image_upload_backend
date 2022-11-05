import dbcreds
import mariadb


def connect_db():
    try:
        conn = mariadb.connect(password=dbcreds.password, user=dbcreds.user,
                               host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        return cursor
    except mariadb.OperationalError as error:
        print("Operational ERROR:", error)
    except Exception as error:
        print("Unknown ERROR:", error)


def execute_statement(cursor, statement, list_of_args=[]):
    try:
        cursor.execute(statement, list_of_args)
        result = cursor.fetchall()
        return result
    except mariadb.ProgrammingError as error:
        print("Programming ERROR: ", error)
        return str(error)
    except mariadb.IntegrityError as error:
        print("Integrity ERROR: ", error)
        return str(error)
    except mariadb.DatabaseError as error:
        print("Data ERROR: ", error)
        return str(error)
    except Exception as error:
        print("Unexpected ERROR: ", error)
        return str(error)


def close_connect(cursor):
    try:
        conn = cursor.connection
        cursor.close()
        conn.close()
    except mariadb.OperationalError as error:
        print("Operational ERROR: ", error)
    except mariadb.InternalError as error:
        print("Internal ERROR: ", error)
    except Exception as error:
        print("Unexpected ERROR: ", error)


def run_statement(statement, list_of_args=[]):
    cursor = connect_db()
    if (cursor == None):
        return "Connection Error"
    results = execute_statement(cursor, statement, list_of_args)
    results = make_dictionary(results, cursor)
    close_connect(cursor)
    return results

def make_dictionary(results, cursor):
    columns = [ i[0] for i in cursor.description ]
    new_results = []
    for row in results:
        new_results.append(dict(zip(columns, row)))
    return new_results