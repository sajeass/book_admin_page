import pymysql,time
from src.common.teams import send_teams_message


class Database(object):
    '''
    db_conn :  db 최초 연결
    db_alive : db 생존 여부 확인 
    db_select : select 구문 실행
    db_insert : insert 구문 실행
    db_delete : delete 구문 실행
    '''

    def __init__(self,schema='aboutb_test'):
        self.schema=schema
        self.db_conn()

    def db_conn(self):
        try:
            self.conn= pymysql.connect(host='ba94df10.cluster-cngy05u8ndbr.ap-northeast-2.rds.amazonaws.com',
            user='aboutb',
            password='Tqordjr6423$',
            db=self.schema,
            charset='utf8',
            cursorclass=pymysql.cursors.SSCursor,connect_timeout=10)

            self.conn.ping() # autoreconnect is true by default
            print('db_connect success')
            return self.conn

        except pymysql.OperationalError:
            print('db_connect failed')
            time.sleep(5)
            return self.db_conn()

    def db_alive(self):
        try:
            self.conn.ping() # autoreconnect is true by default
            return self.conn
        except pymysql.OperationalError:
            print('db_dead')
            time.sleep(5)
            return self.db_alive()

    def insert(self,query,element=()):
        # print(query,element)
        self.db_alive() # db alive check
        with self.conn.cursor(pymysql.cursors.SSCursor) as cursorSS: 
            cursorSS.execute(query,element)
            self.conn.commit()

    def insert_many(self,query,element=()):
        self.db_alive() # db alive check
        with self.conn.cursor(pymysql.cursors.SSCursor) as cursorSS: 
            cursorSS.executemany(query,element)
            self.conn.commit()

    def delete(self,query,element=()):
        self.db_alive() # db alive check
        with self.conn.cursor(pymysql.cursors.SSCursor) as cursorSS: 
            cursorSS.execute(query,element)
            self.conn.commit()
            
    def select_one(self,query,element=()):
        # print(query,element)
        self.db_alive() # db alive check
        with self.conn.cursor(pymysql.cursors.SSCursor) as cursorSS: 
            cursorSS.execute(query,element)
            fetchone=cursorSS.fetchone()
        return fetchone

    def select_all(self,query,element=()):
        # print(query,element)
        self.db_alive() # db alive check
        with self.conn.cursor(pymysql.cursors.SSCursor) as cursorSS: 
            cursorSS.execute(query,element)
            fetchall = cursorSS.fetchall() # return : fetchall result
        return fetchall

    def close(self):
        print('db close')
        try:
            self.conn.close()
        except pymysql.Error:
            print('db already close')
        
    def error_log(self,code,error_type,traceback):
        send_teams_message("personal",f"오류발생 code {code}: error_type: {error_type} , traceback :{traceback}")
        query = "INSERT INTO y_error_c (code,error_type,traceback) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE code=%s,error_type=%s,traceback=%s"
        element = (code,error_type,traceback)*2
        with self.conn.cursor(pymysql.cursors.SSCursor) as cursorSS: 
            cursorSS.execute(query,element)
            self.conn.commit()

    def gongmae_error_log(self,g_code,error_type,traceback):
        query = "INSERT INTO y_error_gongmae_c (g_code,error_type,traceback) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE g_code=%s,error_type=%s,traceback=%s"
        element = (g_code,error_type,traceback)*2
        with self.conn.cursor(pymysql.cursors.SSCursor) as cursorSS: 
            cursorSS.execute(query,element)
            self.conn.commit()
