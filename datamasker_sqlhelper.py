# sqlite, mysql
default_update_template = "Update {0} set {1} = '{4}' where {2} = {3}"
default_select_field_template = "Select {1} from {0}"
default_select_2fields_template = "Select {2}, {1}  from {0}"
default_select_all_template = "Select * From {0}"

# postgresql
postgresql_update_template = 'Update "{0}" set "{1}" = \'{4}\' where "{2}" = {3}'
postgresql_select_field_template = 'Select "{1}" from "{0}"'
postgresql_select_2fields_template = 'Select "{2}", "{1}"  from "{0}"'
postgresql_select_all_template = 'Select * From "{0}"'


def get_select_all_template(setting):
	if setting.dbtype == "postgresql":
		sql_template = postgresql_select_all_template
	else:
		sql_template = default_select_all_template
	return sql_template.format(setting.tablename)


def get_update_template(setting, currentid, targetvalue):
	if setting.dbtype == "postgresql":
		sql_template = postgresql_update_template
	else:
		sql_template = default_update_template
	return sql_template.format(setting.tablename, setting.fieldname, setting.fieldidname, currentid, targetvalue)


def get_select_idfield_template(setting):
	if setting.dbtype == "postgresql":
		sql_template = postgresql_select_field_template
	else:
		sql_template = default_select_field_template
	return sql_template.format(setting.tablename, setting.fieldidname)


def get_select_2fields_template(setting):
	if setting.dbtype == "postgresql":
		sql_template = postgresql_select_2fields_template
	else:
		sql_template = default_select_2fields_template
	return sql_template.format(setting.tablename, setting.fieldname, setting.fieldidname)