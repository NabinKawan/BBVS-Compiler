import json


def write_json_to_file(file_name: str, data):
    with open(file_name, 'w') as outfile:
        # Write JSON data to file
        json.dump(data, outfile)


def read_json_from_file(file_name: str):
    file_data = None
    with open(fr"C:\Users\acer\PycharmProjects\Compiler\{file_name}") as file:
        file_data = json.load(file)
    return file_data
