import datamasker_algs
import datamasker_tools
import datamasker_params
import datamasker_l10n
import datamasker_tests

def do_work(settings):
	for setting in settings:
		if not datamasker_tools.ask_for_confirmation(setting):
			datamasker_tools.close(0, datamasker_l10n.have_a_nice_day_bye)

		datamasker_tools.verbose(datamasker_l10n.info_message.format(setting.algorithm, setting.fieldname, setting.tablename, setting.dbname))
		connection = datamasker_tools.get_db_connection(setting)

		record_count = datamasker_algs.process_masking(connection, setting)
		datamasker_tools.verbose(datamasker_l10n.records_affected.format(record_count))
		datamasker_tools.verbose("\r\n")
		connection.close()
	datamasker_tools.close()

datamasker_tests.do_tests()

settings = datamasker_params.get_settings()
do_work(settings)
