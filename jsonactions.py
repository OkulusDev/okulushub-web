import json


def write(filename, flag, data):
	with open(filename, flag) as file:
		json.dump(data, file)


def get_json(filename):
	with open(filename, 'r') as file:
		return json.loads(file.read())
