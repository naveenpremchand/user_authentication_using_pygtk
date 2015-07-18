--tbl_user
CREATE TABLE tbl_user(
				pk_bint_user_id BIGSERIAL NOT NULL,
                                vchr_user_group_name VARCHAR(100),
                                vchr_modified_by VARCHAR(35),
                                vchr_created_by VARCHAR(35),
				vchr_user_name VARCHAR(100),
				vchr_password VARCHAR(100),
				bln_blocked BOOLEAN DEFAULT FALSE,
                                tim_created  TIMESTAMP WITH TIME ZONE NULL,
				chr_document_status CHAR(1) NOT NULL DEFAULT 'N',
				PRIMARY KEY(pk_bint_user_id)
				
			);