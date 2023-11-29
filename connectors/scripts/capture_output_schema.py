import argparse
from connectors.scripts.execute_operation import ExecuteOperation
from connectors.scripts.clean_output_schema import clean
from connectors.scripts.utils import read_local_data, write_local_data
import json


def update_output_schema(local_data_path: str, connector_name: str, operation_name: str, output_schema: str) -> None:
    local_data = read_local_data(local_data_path)
    if connector_name not in local_data:
        local_data[connector_name] = {}
    conn_data = local_data.get(connector_name)
    if "output_schema" not in conn_data:
        conn_data["output_schema"] = {}

    output_schema_data = conn_data.get("output_schema")
    output_schema_data[operation_name] = output_schema
    write_local_data(local_data_path, local_data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-path", type=str, required=True, help="Complete connector path")
    parser.add_argument("--connector-name", type=str, required=True, help="Connector name")
    parser.add_argument("--config-name", type=str, required=True, help="Configuration name")
    parser.add_argument("--operation-name", type=str, required=True, help="Operation name")
    parser.add_argument("--local-data-path", type=str, required=True, help="Local data path")
    parser.add_argument("--connector-data", type=str, required=True, help="Connector data")

    args = parser.parse_args()
    exec_action = ExecuteOperation(args.connector_path, args.connector_name, args.config_name,
                                   args.operation_name, args.connector_data)
    result = exec_action.execute()
    result = clean(result)
    update_output_schema(args.local_data_path, args.connector_name, args.operation_name, result)
    print(result)


if __name__ == "__main__":
    main()
