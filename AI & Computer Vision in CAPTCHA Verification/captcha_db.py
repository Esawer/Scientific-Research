import sqlite3

def db_connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("captcha_db")
        try:
            c = conn.cursor()
            r = func(c=c, *args, **kwargs)
            conn.commit()
            return r
        except Exception as e:
            conn.rollback()
            print("error\n", e)
            raise e
        finally:
            conn.close()
    return wrapper

@db_connection
def add_item(c, table_name:str, file_name:str, captcha_code:str, captcha_image):
    c.execute(f"INSERT INTO {table_name} (file_name, captcha_code, captcha_image) VALUES (?, ?, ?)", (file_name, captcha_code, captcha_image))

@db_connection
def delte_all(c, table_name:str):
    c.execute(f"DELETE FROM {table_name}")

@db_connection
def get_all(c, table_name:str):
    return c.execute(f"SELECT file_name, captcha_code FROM {table_name}").fetchall()
    

'''
        kaggle_dataset
            id INTEGER PRIMARY KEY,
            file_name TEXT NOT NULL,
            captcha_code TEXT NOT NULL,
            captcha_image BLOB NOT NULL


        author_implementation
            id INTEGER PRIMARY KEY,
            file_name TEXT NOT NULL,
            captcha_code TEXT NOT NULL,
            captcha_image BLOB NOT NULL

            
        opensource_implementation
            id INTEGER PRIMARY KEY,
            file_name TEXT NOT NULL,
            captcha_code TEXT NOT NULL,
            captcha_image BLOB NOT NULL
        
'''