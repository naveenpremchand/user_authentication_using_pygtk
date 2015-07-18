""" Owner : Naveen Premchand
    Creation date : 01.01.2015
    Purpose : DB file for user
"""
from database import ins_database

class UserDB:

    def __init__(self, *args):
        self.create_instances()
        pass

    def create_instances(self, *args):
        pass

    def get_all_user_data(self):
        cr = ins_database.cursor()

        cr.execute("""SELECT pk_bint_user_id,
                         vchr_user_name,
                         vchr_password,
                         vchr_user_group_name,
                        bln_blocked
        FROM tbl_user
        WHERE chr_document_status <> 'D'
        ORDER BY pk_bint_user_id """)

        rst = cr.fetchall()
        return rst

    def insert_user_data(self, ins_user_base):
        cr = ins_database.cursor()

        cr.execute("""INSERT INTO tbl_user
                        (vchr_user_name,
                                 vchr_password,
                                 bln_blocked,
                                 vchr_user_group_name,
                                        vchr_created_by,
                                        vchr_modified_by,
                                        tim_created)
        VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                        (ins_user_base.str_user_name,
                        ins_user_base.str_password,
                        ins_user_base.bln_blocked,
                        ins_user_base.str_role	,
                        ins_user_base.str_created_by,
                        ins_user_base.str_modified_by,
                        ins_user_base.tim_created))

        cr.execute(""" SELECT currval(pg_get_serial_sequence('tbl_user','pk_bint_user_id'))
                                                                        AS pk_bint_user_id """)

        record = cr.fetchone()
        return record['pk_bint_user_id']

    def update_user_data(self, ins_user_base):
        cr = ins_database.cursor()
        cr.execute("""UPDATE tbl_user
                        SET vchr_user_name = %s ,
                                        vchr_password = %s,
                                        vchr_user_group_name = %s,
                                        vchr_modified_by = %s,
                                        bln_blocked = %s,
                                        tim_created = %s
                        WHERE pk_bint_user_id = %s""",(ins_user_base.str_user_name,
                                                    ins_user_base.str_password,
                                                    ins_user_base.str_role,
                                                   ins_user_base.str_modified_by,
                                                   ins_user_base.bln_blocked,
                                                   ins_user_base.tim_created,
                                                   ins_user_base.int_user_id))
        pass


    def delete_user_data(self, int_user_id):
        cr = ins_database.cursor()

        cr.execute("""DELETE FROM tbl_user
                    WHERE pk_bint_user_id = %s""",
                                            (int_user_id,))

        pass


   

    def check_user_password(self,int_user_id,str_encrypted_password):
            cr = ins_database.cursor()
            cr.execute("""SELECT pk_bint_user_id
                            FROM tbl_user
                            WHERE pk_bint_user_id = %s AND vchr_password = %s """, (int_user_id,str_encrypted_password))


            record = cr.fetchone()
            return record
            pass
