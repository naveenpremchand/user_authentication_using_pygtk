""" Owner : Naveen Premchand
    Creation date : 01.01.2015
    Purpose : Database connection
"""

import psycopg2
import psycopg2.extras
import os

class Database(object):
    _dct_database = {}
    def __new__(cls,*args):
        if cls not in cls._dct_database:
            dct_conf = {'host':'','database':'','user':'','password':''}
            
            for str_line in file(os.path.join('database','conf')):
                str_line = str_line.strip()
                if str_line and len(str_line.split('=')) >=2:
                    dct_conf[str_line.split('=')[0].strip()] = str_line.split('=')[1].strip()
                    pass
                pass
            
            conn_string = "host= '%(host)s' dbname = '%(database)s' user= '%(user)s' password= '%(password)s' "%dct_conf
	    
            cls.ins_db = psycopg2.connect(conn_string)
                
            cls._dct_database[cls] = object.__new__(cls, *args)
            pass
        
        return cls._dct_database[cls]
        pass

    def cursor(self):
        return self.ins_db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def commit(self):
        self.ins_db.commit()
    
    def rollback(self):
	self.ins_db.rollback()

    def close(self):
	self.ins_db.close()
	pass




