import json
import argparse
import sys


def clean(obj):
    if isinstance(obj, dict):
        for i in obj.keys():
            obj[i] = clean(obj[i])
        return obj
    elif isinstance(obj, list):
        if len(obj) > 0 and not isinstance(obj[0], str):
            return [clean(obj[0])]
        else:
            return []
    else:
        return ""


def clean_output_schema(info_file_json):
    for op in info_file_json.get("operations", []):
        if "output_schema" in op:
            op['output_schema'] = clean(op["output_schema"])
    return info_file_json


def read_info_json_file(connector_info):
    try:
        with open(connector_info, 'r') as data:
            json_data = json.load(data)
        return json_data
    except Exception as err:
        print("read_info_json_file: " + str(err))


def write_info_json_file(connector_info, info_file_json):
    try:
        with open(connector_info, 'w') as file:
            json.dump(info_file_json, file, indent=2)
    except Exception as e:
        print(f"Error in writing json file: {e}")


def read_input():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--connector-info", help="This is connector json file path")
        args = parser.parse_args()
        if len(sys.argv) <= 1:
            print("Please provide input --connector-info")
            exit(0)
        return args
    except Exception as err:
        print("read_input: " + str(err))


def main():
    args = read_input()
    info_file_json = read_info_json_file(args.connector_info)
    info_file_json = clean_output_schema(info_file_json)
    write_info_json_file(args.connector_info, info_file_json)


if __name__ == '__main__':
    main()
