import random
import string
import datamasker_algs
import datamasker_l10n

from faker import Faker

fake = Faker()


def get_random_string(length, source_value):
	s = string.ascii_lowercase + string.digits
	return ''.join(random.sample(s, int(length)))


def get_faker_string(fakertype, source_value):
	# https://github.com/joke2k/faker
	return fake.__getattribute__(fakertype)()


def get_asterix_string(mask, source_value):
	left_count = int(mask.split("*")[0])
	right_count = int(mask.split("*")[1])
	asterix_count = len(source_value) - left_count - right_count
	if asterix_count > 0:
		target_value = source_value[:left_count] + asterix_count * datamasker_l10n.asterix + source_value[(
			left_count + asterix_count):]
	else:
		target_value = source_value
	return target_value


def get_random_data_from_dict(dict_values, source_value):
	rand_id = random.randint(0, len(dict_values) - 1)
	target_value = dict_values[rand_id][1]
	del (dict_values[rand_id])
	return target_value


def ask_for_confirmation(setting):
	if setting.alwaysyes:
		return True
	yes = (['yes', 'y', ''])
	no = (['no', 'n'])
	choice = input().lower()
	if choice in yes:
		return True
	elif choice in no:
		return False


def close(exitcode=0, message=""):
	if message != "":
		print(message)
	else:
		print("Exit")
	exit(exitcode)


def get_db_connection(setting):
	if setting.dbtype == "sqlite":
		import sqlite3

		conn = sqlite3.connect(setting.dbname)
	elif setting.dbtype == "mysql":
		import pymysql

		conn = pymysql.connect(host=setting.host, port=int(setting.port), user=setting.user, passwd=setting.password,
							   db=setting.dbname)
	elif setting.dbtype == "postgresql":
		import psycopg2

		conn = psycopg2.connect(host=setting.host, port=int(setting.port), user=setting.user, password=setting.password,
								dbname=setting.dbname)
	elif setting.dbtype == "odbc":
		close(1, datamasker_l10n.not_implemented)
	else:
		close(1, datamasker_l10n.database_type_not_found.format(setting.dbtype))
	return conn


def verbose(msg):
	print(msg)