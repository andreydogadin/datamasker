import datamasker_tools
import datamasker_params
import configparser
import datamasker_l10n
import datamasker_algs


def get_test_settings():
	config = configparser.ConfigParser()
	config.read("dbs\sqlite_test.ini")
	settings = []
	for section in config.sections():
		dbname = config.get(section, 'dbname')
		tablename = config.get(section, 'tablename')
		fieldidname = config.get(section, 'fieldidname')
		fieldname = config.get(section, 'fieldname')
		algorithm = section
		extraparam = config.get(section, 'extraparam')
		setting = datamasker_params.Setting("sqlite", "", "", "", "", dbname, tablename, fieldidname, fieldname, algorithm, extraparam, "")
		setting.put_defauls()
		settings.append(setting)
	return settings

def get_test_connection(setting):
	return datamasker_tools.get_db_connection(setting)

def test_get_asterix_string():
	assert (datamasker_tools.get_asterix_string("3*3", "123456789") == "123***789")
	assert (datamasker_tools.get_asterix_string("0*3", "123456789") == "******789")
	assert (datamasker_tools.get_asterix_string("3*0", "123456789") == "123******")
	assert (datamasker_tools.get_asterix_string("10*10", "123456789") == "123456789")


def test_algs():
	settings = get_test_settings()
	for setting in settings:

			datamasker_tools.verbose(datamasker_l10n.confirm_message.format(setting.algorithm, setting.fieldname, setting.tablename, setting.dbname))
			connection = get_test_connection(setting)

			datamasker_tools.verbose(datamasker_l10n.before)
			datamasker_algs.show_table(connection, setting)
			hashes_init = datamasker_algs.get_table_hashes(connection, setting)
			hashes2 = datamasker_algs.get_table_hashes(connection, setting)
			assert (set(hashes_init) == set(hashes2))

			datamasker_algs.process_masking(connection, setting)

			hashes_post = datamasker_algs.get_table_hashes(connection, setting)
			assert (set(hashes_init) != set(hashes_post))

			connection.close()

def do_tests():
	test_get_asterix_string()
	test_algs()
