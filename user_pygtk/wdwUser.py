""" Owner : Naveen Premchand
    Creation date : 01.01.2015
    Purpose : Main file for user
"""

import gtk
import gtk.glade
import os
import copy
import userDB
import userLG
from Crypto.Cipher import AES
import base64
import os

from database import ins_database

class InputError(Exception):
    pass


# Local level encryption
dct_pass_conv = {'small': 'abcdefghijklmnopqrstuvwxyz',
			 'nums': '0123456789',
			 'big': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
			 'special': '^!\$%&/()=?{[]}+~#-_.:;<>@'
			}


lst_special_password = ','.join(dct_pass_conv['special']).split(',')

lst_lower_characters = [chr(num) for num in range(97,123)]
lst_upper_characters = [chr(num) for num in range(65,91)]
dct_small_characters = {}.fromkeys(lst_lower_characters)
dct_upper_characters = {}.fromkeys(lst_upper_characters)
dct_special_characters = {}.fromkeys(lst_special_password)


lst_big_characters_conv = dct_pass_conv['nums']+dct_pass_conv['small'][:16]

dct_small_conv_text =  {}
dct_upper_conv_text =  {}
dct_small_conv_special =  {}
dct_upper_conv_special =  {}

index_1 = 0
for str_characters in dct_small_characters:
	dct_small_conv_text[str_characters] = lst_special_password[index_1]
	dct_small_conv_special[lst_special_password[index_1]] = str_characters
	index_1 += 1
	pass

index_2 = 0
for str_characters in dct_upper_characters:
	dct_upper_conv_text[str_characters] =  lst_big_characters_conv[index_2]
	dct_upper_conv_special[lst_big_characters_conv[index_2]] = str_characters
	index_2 += 1
	pass


class UserGUI:
	def __init__(self,):
		self.create_instances()
		self.get_widgets()
		self.connections()
		self.initialise_user()
		self.initialise_entry_completion()
		pass

	def create_instances(self, *args):
		self.ins_user_db = userDB.UserDB()
		self.ins_user_lg = userLG.UserLG()
		pass

	def get_widgets(self, *args):
                # Getting the widget from glade
		xml = gtk.glade.XML(os.path.join("wdwUser.glade"))

		self.topUser = xml.get_widget("wdwUser")

		self.trvUser = xml.get_widget("trvUser")
		
		self.etrUserName = xml.get_widget("etrUserName")
		self.etrNewPassword = xml.get_widget("etrNewPassword")
		self.etrOldPassword = xml.get_widget("etrOldPassword")
		self.etrConfirmPassword = xml.get_widget("etrConfirmPassword")
		self.cbeUserGroup = xml.get_widget("cbeUserGroup")


		self.btnAdd = xml.get_widget("btnAdd")
		self.btnUpdate = xml.get_widget("btnUpdate")
		self.btnDelete = xml.get_widget("btnDelete")
		self.btnClear = xml.get_widget("btnClear")
		self.btnClose = xml.get_widget("btnClose")
	   
		pass

	def connections(self, *args):
                # Describing the events
		self.topUser.connect("delete_event", self.on_close_button_clicked)

		self.trvUser.connect("row_activated", self.on_user_tree_view_row_activated)
		self.trvUser.connect("cursor_changed", self.on_user_tree_view_cursor_changed)

		self.etrUserName.connect("activate", self.on_user_name_entry_activate)
		self.etrNewPassword.connect("activate", self.on_user_password_entry_activate)
		self.etrOldPassword.connect("activate", self.on_user_old_password_entry_activate)
		self.etrConfirmPassword.connect("activate", self.on_user_confirm_password_entry_activate)
		self.cbeUserGroup.child.connect("activate", self.on_user_group_combo_box_entry_activated)

		self.btnAdd.connect("clicked", self.on_add_button_clicked)
		self.btnUpdate.connect("clicked", self.on_update_button_clicked)
		self.btnDelete.connect("clicked", self.on_delete_button_clicked)
		self.btnClear.connect("clicked", self.on_clear_button_clicked)
		self.btnClose.connect("clicked", self.on_close_button_clicked)
		pass

	def initialise_user(self, *args):
		self.lsr_user = gtk.ListStore(object,
                                                   str,
                                                   str)

		self.trvUser.set_model(self.lsr_user)

		crt = gtk.CellRendererText()
		crt.set_property('xalign',0.00)
		tvc = gtk.TreeViewColumn("User", crt,text= 1)
		tvc.set_alignment(0.5)
		tvc.set_expand(False)
		tvc.set_resizable(True)
		self.trvUser.append_column(tvc)
		tvc.set_min_width(100)

		crt = gtk.CellRendererText()
		crt.set_property('xalign',0.00)
		tvc = gtk.TreeViewColumn("Role", crt,text= 2)
		tvc.set_alignment(0.5)
		tvc.set_expand(False)
		tvc.set_resizable(True)
		self.trvUser.append_column(tvc)
		tvc.set_min_width(100)
		pass

	# Initialise entry completion
        def initialise_entry_completion(self,*args):
		self.lsr_user_group = gtk.ListStore(str)
		self.cbeUserGroup.set_model(self.lsr_user_group)
		cmp_user_group = gtk.EntryCompletion()
		cmp_user_group.set_model(self.lsr_user_group)
		self.cbeUserGroup.child.set_completion(cmp_user_group)
		cmp_user_group.set_text_column(0)
		pass
        # Load user group data for entry completion 
	def load_user_group_data(self, *args):
		self.lsr_user_group.clear()

		lst_user_group = ["ADMIN","ACCOUNTANT","CASHIER"]
                
		for str_group_name in lst_user_group:			
			self.dct_user_group_name[str_group_name] = None
			itr = self.lsr_user_group.append()
			self.lsr_user_group.set(itr,0, str_group_name)
			pass
		pass


	def initialise(self, *args):
		
		self.dct_user_group_name = {}
		self.lsr_user.clear()
		self.on_clear_button_clicked()

		self.etrUserName.grab_focus()
		pass

	# Show user window gui
        def show_window(self, *args):
		self.initialise()
		self.load_user_group_data()
		self.load_user_details()
		self.topUser.show_all()
		self.bln_hide = False
		pass

	def on_close_button_clicked(self, *args):
		self.topUser.hide()
		self.bln_hide = True
		return True

	def on_user_tree_view_row_activated(self, *args):
		itr  = self.trvUser.get_selection().get_selected()[1]
		if not itr:
                    return
		ins_user_base = self.lsr_user.get_value(itr, 0)

		self.set_user_group_data_to_widgets(ins_user_base)

		self.btnAdd.set_sensitive(False)
		self.btnUpdate.set_sensitive(True)
		self.btnDelete.set_sensitive(True)

		self.etrUserName.grab_focus()
		pass

	def set_user_group_data_to_widgets(self,ins_user_base):
		self.etrUserName.set_text(ins_user_base.str_user_name)
		self.cbeUserGroup.child.set_text(ins_user_base.str_role)
		pass

	def on_user_tree_view_cursor_changed(self, *args):
		self.on_clear_button_clicked()
		pass

	def on_user_name_entry_activate(self, *args):
		self.etrOldPassword.grab_focus()
		pass

	def on_user_password_entry_activate(self,*args):
		self.etrConfirmPassword.grab_focus()
		pass

	def on_user_old_password_entry_activate(self,*args):
		self.etrNewPassword.grab_focus()
		pass

	def on_user_confirm_password_entry_activate(self,*args):
		self.cbeUserGroup.grab_focus()
		pass

	def on_user_group_combo_box_entry_activated(self,*args):
                if self.btnAdd.get_sensitive():
                    self.btnAdd.grab_focus()
                    pass
                else:
                    self.btnUpdate.grab_focus()
                    pass
		pass

	def on_add_button_clicked(self, *args):

		ins_user_base = userLG.UserBase()

		ins_user_base = self.get_input_data(ins_user_base)
                
		str_password = self.etrConfirmPassword.get_text()
                
		ins_user_base.str_created_by = 'admin'
		str_password = self.convert_password(str_password)
		ins_user_base.str_password = self.encryption_using_cipher_key(str_password)

		try:
			self.validate_input_data()
		except Exception,msg:
			print msg
			return
	
		itr = self.lsr_user.get_iter_root()
                # Need to check whether user is already added to grid
		while itr:
			ins_added_user_base = self.lsr_user.get_value(itr, 0)
			if ins_added_user_base.str_user_name.strip() == ins_user_base.str_user_name.strip():
				self.trvUser.get_selection().select_iter(itr)
				print 'User added'
				return
			itr = self.lsr_user.iter_next(itr)
			pass

		try:
			int_user_id = self.ins_user_lg.insert_user_data(ins_user_base)
		except:
			ins_database.rollback()
			
		else:
			ins_database.commit()
			ins_user_base.int_user_id = int_user_id
			self.display_user_data_to_grid(ins_user_base)
			self.on_clear_button_clicked()
			pass
		pass

	def get_input_data(self,ins_user_base):
		ins_user_base.str_user_name = self.etrUserName.get_text().strip()
		ins_user_base.str_role = self.cbeUserGroup.child.get_text().strip().upper()
		
		if self.dct_user_group_name.has_key(ins_user_base.str_role):
			ins_user_base.str_user_group_name = ins_user_base.str_role
			pass
		ins_user_base.str_document_status = 'N'
		ins_user_base.tim_created = self.get_current_date_time()
		return ins_user_base

	def validate_input_data(self):
		str_role = self.cbeUserGroup.child.get_text()
		if not self.dct_user_group_name.has_key(str_role):
			raise InputError('Invalid Group Name')
			pass
		str_new_password = self.etrNewPassword.get_text()
		str_confirm_password = self.etrConfirmPassword.get_text()
		if str_new_password <> str_confirm_password:
			raise InputError('Confirm password does not match')

		str_user = self.etrUserName.get_text()
		if not str_user:
			raise InputError('User Name  Cannot be blank')
			pass
		str_password = self.etrConfirmPassword.get_text()
		if not str_password:
			raise InputError('Password Cannot be blank')
		pass
		

	def on_update_button_clicked(self, *args):

		itr  = self.trvUser.get_selection().get_selected()[1]
		if not itr:
                    return
                
		ins_user_base = copy.copy(self.lsr_user.get_value(itr, 0))
		ins_user_base = self.get_input_data(ins_user_base)

		str_old_password = self.etrOldPassword.get_text()
		str_old_converted_password = self.convert_password(str_old_password)
		str_encrypted_password = self.encryption_using_cipher_key(str_old_converted_password)
		rst = self.ins_user_db.check_user_password(ins_user_base.int_user_id,str_encrypted_password)
		if not rst:
			print 'invalid password'
			return
		try:
			self.validate_input_data()
		except Exception,msg:
			print msg
			return

		str_password = self.etrConfirmPassword.get_text()

		str_password = self.convert_password(str_password)
		ins_user_base.str_password = self.encryption_using_cipher_key(str_password)

	
		ins_user_base.str_modified_by = 'lord'


		itr_row = self.lsr_user.get_iter_root()
		while itr_row:
			ins_updating_user_base = self.lsr_user.get_value(itr_row, 0)
			if self.lsr_user.get_path(itr) != self.lsr_user.get_path(itr_row):
				if ins_updating_user_base.str_user_name.strip().upper() == ins_user_base.str_user_name.strip().upper():
					self.trvUser.get_selection().select_iter(itr_row)
					print 'User already exist'
					return
				pass
			itr_row = self.lsr_user.iter_next(itr_row)
			pass

	  
		try:
			self.ins_user_lg.update_user_data(ins_user_base)
		except:
                        raise
			ins_database.rollback()
		else:
			ins_database.commit()
			self.display_user_data_to_grid(ins_user_base, itr)
			self.on_clear_button_clicked()
			pass
		pass

	def on_delete_button_clicked(self, *args):
		itr  = self.trvUser.get_selection().get_selected()[1]
		if not itr:
			return

		ins_user_base = self.lsr_user.get_value(itr, 0)

		try:
			self.ins_user_lg.delete_user_data(ins_user_base.int_user_id)
		except:
                        raise
			ins_database.rollback()
		else:
			ins_database.commit()
			self.lsr_user.remove(itr)
			self.on_clear_button_clicked()
			pass
		pass

	def on_clear_button_clicked(self, *args):
		self.etrUserName.set_text('')
		self.etrConfirmPassword.set_text('')
		self.etrNewPassword.set_text('')
		self.etrOldPassword.set_text('')
		self.cbeUserGroup.child.set_text('')


		self.btnAdd.set_sensitive(True)
		self.btnUpdate.set_sensitive(False)
		self.btnDelete.set_sensitive(False)
		pass


	def load_user_details(self, *args):
		lst_user_data = self.ins_user_lg.get_user_data()
		
		for ins_user_base in lst_user_data:
			
			self.display_user_data_to_grid(ins_user_base)
			pass
		pass

	# Adding to the grid
        def display_user_data_to_grid(self, ins_user_base, itr = None):
		if not itr:
			itr = self.lsr_user.append()
			pass
		self.lsr_user.set(itr, 0, ins_user_base,
                                         1, ins_user_base.str_user_name,
                                         2, ins_user_base.str_role
                                         )
		pass

	# Get the current date time from database to store tim created
        def get_current_date_time(self):
		cr = ins_database.cursor()
		cr.execute("""select now()""")
		tim_date = cr.fetchone()[0]
		cr.close()
		return tim_date

	# Local level encryption
        def convert_password(self,str_password):
		str_new_password = ''
	
		index = 0
		self.lst_un_converted_index = []
		for chr in str_password:
			
			if chr in dct_small_conv_text:
				str_new_password += dct_small_conv_text[chr]
				pass
			elif chr in dct_upper_conv_text:
				str_new_password += dct_upper_conv_text[chr]
				pass
			else:
				self.lst_un_converted_index.append(index)
				str_new_password += chr
				pass
			index += 1
			pass
                    
		str_new_password = 'trusty' +str_new_password 

		return str_new_password

	# Encryption using Crpto using key given
        def encryption_using_cipher_key(self,str_password):
		BLOCK_SIZE = 16
		PADDING = '{'
		pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
		EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
		secret = 'inovaters5643210'
		cipher = AES.new(secret)
		encoded = EncodeAES(cipher, str_password)
	
		return encoded
        # Decryption using Crpto using key given
	def decryption_using_cipher_key(self,encryptedString):
            
		PADDING = '{'
		DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
		encryption = encryptedString
		key ='inovaters5643210'
		cipher = AES.new(key)
		decoded = DecodeAES(cipher, encryption)
                return decoded

	# Restore the original password ie local decryption
        def restore_original_password(self,str_conv_password):
		str_conv_password = str_conv_password[6:]
		str_original_password = ''
		index_2 = 0
		for chr in str_conv_password:
			if index_2 in self.lst_un_converted_index:
				str_original_password += chr
				index_2 += 1
				continue

			if chr in dct_small_conv_special:
				str_original_password += dct_small_conv_special[chr]
				pass
			elif chr in dct_upper_conv_special:
				str_original_password += dct_upper_conv_special[chr]
				pass
			index_2 += 1

	
		return str_original_password

        def main(self):
		gtk.main()

if __name__ == "__main__":    
	ins_login = UserGUI()
	ins_login.show_window()
	ins_login.main()
   
		
