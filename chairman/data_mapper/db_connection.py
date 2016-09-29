import psycopg2


def print_sql(sql):
    print('\033[1;33m' + str(sql) + '\033[1;m')


def print_sql_result(list):
    print('\033[1;35m' + str(list) + '\033[1;m')


def print_exception(e):
    print('\033[1;31m' + str(e) + '\033[1;m')


def printt(text):
    print('\033[1;34m' + str(text) + '\033[1;m')


class DB:
    db_settings = {
        'host': 'localhost',
        'dbname': 'data_mapper_test',
        'user': 'postgres',
        'password': 'creeper'
    }

    @classmethod
    def connection(cls):
        conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(cls.db_settings['host'],
                                                                             cls.db_settings['dbname'],
                                                                             cls.db_settings['user'],
                                                                             cls.db_settings['password'])
        conn = psycopg2.connect(conn_string)
        return conn

    @classmethod
    def execute_sql(cls, sql):
        conn = cls.connection()
        cursor = conn.cursor()
        print_sql(sql)
        try:
            cursor.execute(sql)
        except BaseException as e:
            print_exception(e)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def execute_sql_with_return(cls, sql):
        conn = cls.connection()
        cursor = conn.cursor()
        print_sql(sql)
        try:
            cursor.execute(sql)
        except psycopg2.DatabaseError as e:
            print_exception(e)
        if 'RETURNING' in sql:
            conn.commit()
            return cursor.fetchall()[0][0]
        records = list(cursor.fetchall())
        print_sql_result(records)
        atts = [item[0] for item in cursor.description]
        records.insert(0, atts)
        return records