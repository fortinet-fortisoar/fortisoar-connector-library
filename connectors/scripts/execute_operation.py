""" Copyright start
  MIT License
  Copyright (c) 2024 Fortinet Inc
  Copyright end """

import inspect
import sys
import json
import argparse
import os
import importlib.util
import copy
from connectors.scripts.utils import is_path_exist


class ExecuteOperation:
    def __init__(self, connector_path, connector_name, config_name, operation_name, connector_data, keys_to_mask, local_data_path):
        self.connector_path = connector_path
        self.connector_name = connector_name
        self.config_name = config_name
        self.operation_name = operation_name
        self.connector_data = connector_data
        self.keys_to_mask = keys_to_mask
        self.local_data_path = local_data_path
        self.connector = self.get_connector()
        self.config = None
        self.params = None
        self.validate_input()
        self.load_config_params()

    def validate_input(self) -> None:
        if not is_path_exist(self.connector_path):
            raise Exception(f"Connector path does not exist. Path: {self.connector_path}")

    def load_config_params(self) -> None:
        conn_data = json.loads(self.connector_data)

        all_config = conn_data.get("config", {})
        self.config = all_config.get(self.config_name, {})

        all_params = conn_data.get("params", {})
        self.params = all_params.get(self.operation_name, {})

    def get_connector(self):
        conn_dir = os.path.dirname(self.connector_path)
        sys.path.append(conn_dir)
        try:
            conn_module = f"{self.connector_name}.connector"
            conn_module = importlib.import_module(conn_module)
            for name, obj in inspect.getmembers(conn_module):
                if inspect.isclass(obj) and issubclass(obj, conn_module.Connector) and not inspect.isabstract(obj):
                    return obj
        except Exception as e:
            print(e)
        return None

    def execute(self, print_result):
        try:
            config = self.mask_keys(copy.deepcopy(self.config))
            params = self.mask_keys(copy.deepcopy(self.params))
            initial_message = f"Operation Name: {self.operation_name}\n" \
                              f"Configuration: {config}\n" \
                              f"Parameters: {params}\n"
            print(initial_message)
            info_json_data = self.read_info_json()
            conn_obj = self.connector(info_json=info_json_data)
            self.config.update({"local_database_path": self.local_data_path})
            if self.operation_name == "check_health":
                result = conn_obj.check_health(self.config)
            else:
                result = conn_obj.execute(self.config, self.operation_name, self.params)
            if print_result:
                print(f"Result: {result}")
            return result

        except Exception as e:
            print(e)

    def read_info_json(self):
        try:
            info_json_file_path = self.connector_path + '/info.json'
            with open(info_json_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File '{self.connector_path + '/info.json'}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file '{self.connector_path + '/info.json'}'.")
            return None
        finally:
            file.close()


    def mask_keys(self, json_data):
        for key in json_data.keys():
            if key in self.keys_to_mask:
                json_data[key] = "********"
        return json_data



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-path", type=str, required=True, help="Complete connector path")
    parser.add_argument("--connector-name", type=str, required=True, help="Connector name")
    parser.add_argument("--config-name", type=str, required=True, help="Configuration name")
    parser.add_argument("--operation-name", type=str, required=True, help="Operation name")
    parser.add_argument("--connector-data", type=str, required=True, help="Connector data")
    parser.add_argument("--keys-to-mask", type=str, required=True, help="Connector's keys to mask")
    parser.add_argument("--local-data-path", type=str, required=True, help="Local data path")

    args = parser.parse_args()
    exec_action = ExecuteOperation(args.connector_path, args.connector_name, args.config_name,
                                   args.operation_name, args.connector_data, args.keys_to_mask.split(','), args.local_data_path)
    exec_action.execute(True)


if __name__ == "__main__":
    main()
