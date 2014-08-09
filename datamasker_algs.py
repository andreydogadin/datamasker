import datamasker_tools
import datamasker_sqlhelper
import datamasker_l10n
import datamasker_algs
import hashlib

supported_algs = ("data_mixer", "randomizer", "faker_generator", "asterix")


def process_masking(connection, setting):
	if setting.algorithm in supported_algs:
		return getattr(datamasker_algs, setting.algorithm)(connection, setting)
	else:
		datamasker_tools.close(1, datamasker_l10n.algorithm_not_found.format(setting.algorithm))
		return 0


def fill_dict_from_db(connection, setting):
	cursor_data = connection.cursor()
	sql = datamasker_sqlhelper.get_select_2fields_template(setting)
	cursor_data.execute(sql)
	dict_value = list(cursor_data.fetchall())
	cursor_data.close()
	return dict_value


def data_mixer(connection, setting):
	setting.extraparam = fill_dict_from_db(connection, setting)
	return data_updater(connection, setting, datamasker_tools.get_random_data_from_dict)


def randomizer(connection, setting):
	return data_updater(connection, setting, datamasker_tools.get_random_string)


def asterix(connection, setting):
	 return data_updater(connection, setting, datamasker_tools.get_asterix_string)


def faker_generator(connection, setting):
	return data_updater(connection, setting, datamasker_tools.get_faker_string)


def data_updater(connection, setting, function):
	cursor = connection.cursor()
	updatecursor = connection.cursor()
	sql = datamasker_sqlhelper.get_select_2fields_template(setting)
	cursor.execute(sql)
	record_count = 0
	for row in cursor.fetchall():
		record_count += 1
		current_id = row[0]
		source_value = row[1]
		target_value = function(setting.extraparam, source_value)
		sql = datamasker_sqlhelper.get_update_template(setting, current_id, target_value)
		updatecursor.execute(sql)
	return record_count


def get_table_hashes(connection, setting):
	cursor = connection.cursor()
	sql = datamasker_sqlhelper.get_select_all_template(setting)
	cursor.execute(sql)

	hashes = list()

	for row in cursor.fetchall():
		string = ', '.join(map(str, row)).encode('utf-8')
		hash_object = hashlib.md5(string)
		hashes.append(hash_object.hexdigest())
	return hashes


def show_table(connection, setting):
	cursor = connection.cursor()
	sql = datamasker_sqlhelper.get_select_all_template(setting)
	cursor.execute(sql)
	for row in cursor.fetchall():
		print(row)