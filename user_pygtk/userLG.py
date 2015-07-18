""" Owner : Naveen Premchand
    Creation date : 01.01.2015
    Purpose : LG file for user
"""
import userDB

class UserBase(object):
    def __init__(self, *args):
        self.int_user_id = None
        self.str_user_name = ''
        self.str_created_by = ''
        self.str_modified_by = ''
        self.str_document_status = 'N'
        self.tim_created = ''
        self.bln_blocked = False
        self.str_role = ''
        pass


class UserLG:

    def __init__(self, *args):
        self.create_instances()
        pass

    def create_instances(self, *args):
        self.ins_user_db = userDB.UserDB()
        pass


    def get_user_data(self):
        lst_user_group_data = []

        rst = self.ins_user_db.get_all_user_data()
        for record in rst:
    
            ins_user_group_base = UserBase()
            ins_user_group_base.int_user_id = record['pk_bint_user_id']
            ins_user_group_base.str_user_name = record['vchr_user_name']
            ins_user_group_base.str_password = record['vchr_password']
            ins_user_group_base.str_role = record['vchr_user_group_name']
            ins_user_group_base.bln_blocked = record['bln_blocked']
            lst_user_group_data.append(ins_user_group_base)
            pass
        
        return lst_user_group_data

    def insert_user_data(self, ins_user_base):
        int_user_id = self.ins_user_db.insert_user_data(ins_user_base)
        return int_user_id

    def update_user_data(self, ins_user_base):
        self.ins_user_db.update_user_data(ins_user_base)
        pass

    def delete_user_data(self, int_user_id):
        self.ins_user_db.delete_user_data(int_user_id)
        pass
