import mariadb
import dbcreds

def convert_data(cursor, results):
    column_names = [i[0] for i in cursor.description]
    new_results = []
    for row in results:
        new_results.append(dict(zip(column_names, row)))
    return new_results

def run_procedure(sql, args):
    try:
        results = None
        conn = mariadb.connect(**dbcreds.conn_params)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        results = cursor.fetchall()
        results = convert_data(cursor, results)
    except mariadb.ProgrammingError as error:
        print("There is an issue with the DB code: ", error)
        results = error
    except mariadb.OperationalError as error:
        print("There is an issue connection to the DB: ", error)
        results = error
    except Exception as error:
        print("There was an unknown error: ", error)
        results = error
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.close()
        return results