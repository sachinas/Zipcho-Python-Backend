'''from mysql.connector import Error
from mysql.connector import pooling


def connection_to_mysql(sqlQuery) : 
    try:
        connection_pool = pooling.MySQLConnectionPool(pool_name="zipchoConnection_pool",
                                                    pool_size=5,
                                                    pool_reset_session=True,
                                                    host='zipcho.coqbh3cnp3jy.ap-south-1.rds.amazonaws.com',
                                                    database='zipchoDevDB',
                                                    user='admin',
                                                    password='Zipcho9798')

        print("Printing connection pool properties ")
        print("Connection Pool Name - ", connection_pool.pool_name)
        print("Connection Pool Size - ", connection_pool.pool_size)

        # Get connection object from a pool
        connection_object = connection_pool.get_connection()

        if connection_object.is_connected():
            db_Info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_Info)

            cursor = connection_object.cursor()
            cursor.execute(sqlQuery)
            record = cursor.fetchone()
            print("Your connected to - ", record)

    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            print("MySQL connection is closed")'''