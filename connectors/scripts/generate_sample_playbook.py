""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

#!/usr/bin/env python
import argparse
import configparser
import json
import os.path
import sys
import uuid
from connectors.scripts.utils import is_path_exist, get_dir_name, create_path

config = {}
alert_workflow_step_types_uuid = "f414d039-bb0d-4e59-9c39-a8f1e880b18a"
connector_step_workflow_step_types_uuid = "0bfed618-0316-11e7-93ae-92361f002671"


def read_info_json_file(connector_info):
    try:
        with open(connector_info, 'r') as data:
            json_data = json.load(data)
        return json_data
    except Exception as err:
        print("read_info_json_file: " + str(err))


def create_alert_step(connector_name, function_name):
    try:
        step_template = {}
        step_template["uuid"] = str(uuid.uuid4())
        step_template["@type"] = "WorkflowStep"
        step_template["name"] = config.get('Alert_Step_Info', 'Alert_Step_Name')
        step_template["description"] = eval(config.get('Alert_Step_Info', 'Alert_Step_Description'))
        step_template["status"] = eval(config.get('Alert_Step_Info', 'Alert_Step_Status'))
        arguments_data = {}
        arguments_data["route"] = str(uuid.uuid4())
        arguments_data["title"] = connector_name + ": " + function_name
        arguments_data["resources"] = eval(config.get('Alert_Step_Info', 'Alert_Step_Source'))
        arguments_data["inputVariables"] = eval(config.get('Alert_Step_Info', 'Alert_Step_Arguments_InputVariables'))
        arguments_data["step_variables"] = eval(config.get('Alert_Step_Info', 'Alert_Step_Arguments_step_variables'))
        arguments_data["singleRecordExecution"] = eval(
            config.get('Alert_Step_Info', 'Alert_Step_Arguments_singleRecordExecution'))
        arguments_data["noRecordExecution"] = eval(
            config.get('Alert_Step_Info', 'Alert_Step_Arguments_noRecordExecution'))
        arguments_data["executeButtonText"] = eval(
            config.get('Alert_Step_Info', 'Alert_Step_Arguments_executeButtonText'))
        step_template["arguments"] = arguments_data
        step_template["left"] = config.get('Alert_Step_Info', 'Alert_Step_Left')
        step_template["top"] = config.get('Alert_Step_Info', 'Alert_Step_top')
        step_template["stepType"] = "/api/3/workflow_step_types/" + alert_workflow_step_types_uuid
        return step_template
    except Exception as err:
        print("create_alert_step: " + str(err))


def get_parameters(parameters):
    try:
        params = {}
        for p in parameters:
            try:
                params[p["name"]] = p["value"]
            except:
                pass
        return params if params != {} else []
    except Exception as err:
        print("get_parameters: " + str(err))


def create_connector_action_step(connector_name, connector_label, function_title, connector_version, function_operation,
                                 parameters):
    try:
        step_template = {}
        step_template["uuid"] = str(uuid.uuid4())
        step_template["@type"] = "WorkflowStep"
        step_template["name"] = function_title
        step_template["description"] = eval(config.get('Connector_Step_Info', 'Connector_Step_Description'))
        step_template["status"] = eval(config.get('Connector_Step_Info', 'Connector_Step_Status'))
        arguments_data = {}
        arguments_data["name"] = connector_label
        arguments_data["config"] = config.get('Connector_Step_Info', 'Connector_Step_Arguments_config')
        arguments_data["params"] = get_parameters(parameters)
        arguments_data["version"] = connector_version
        arguments_data["connector"] = connector_name
        arguments_data["operation"] = function_operation
        arguments_data["operationTitle"] = function_title
        arguments_data["step_variables"] = eval(
            config.get('Connector_Step_Info', 'Connector_Step_Arguments_step_variables'))
        step_template["arguments"] = arguments_data
        step_template["left"] = config.get('Connector_Step_Info', 'Connector_Step_Left')
        step_template["top"] = config.get('Connector_Step_Info', 'Connector_Step_top')
        step_template["stepType"] = "/api/3/workflow_step_types/" + connector_step_workflow_step_types_uuid
        return step_template
    except Exception as err:
        print("create_connector_action_step: " + str(err))


def create_routes(function_title, alert_step_uuid, connector_function_step_uuid):
    try:
        routes_template = {}
        routes_template["@type"] = "WorkflowRoute"
        routes_template["uuid"] = str(uuid.uuid4())
        routes_template["label"] = eval(config.get('Routes_Info', 'Routes_Label'))
        routes_template["isExecuted"] = config.getboolean('Routes_Info', 'Routes_isExecuted')
        routes_template["name"] = config.get('Alert_Step_Info', 'Alert_Step_Name') + "-> " + function_title
        routes_template["sourceStep"] = "/api/3/workflow_steps/" + alert_step_uuid
        routes_template["targetStep"] = "/api/3/workflow_steps/" + connector_function_step_uuid
        return routes_template
    except Exception as err:
        print("create_routes: " + str(err))


def create_workflow(collection_UUID, info_file_json):
    try:
        all_functions = info_file_json["operations"]
        all_playbooks_list = []
        for function in all_functions:
            try:
                # Skip to add playbook if action visible is false or if enabled is false.
                if function.get("visible", True) == False or function.get("enabled", True) == False:
                    continue
            except:
                pass
            playbook_template = {}
            playbook_template["@type"] = "Workflow"
            playbook_template["uuid"] = str(uuid.uuid4())

            # This function create alert step.
            alert_step = create_alert_step(info_file_json["label"], function["title"])
            # This function create connector step.
            connector_function_step = create_connector_action_step(info_file_json["name"], info_file_json["label"],
                                                                   function["title"], info_file_json["version"],
                                                                   function["operation"], function["parameters"])
            playbook_template["collection"] = "/api/3/workflow_collections/" + collection_UUID
            playbook_template["triggerLimit"] = eval(config.get('Workflow_Info', 'Workflow_TriggerLimit'))  # None
            playbook_template["description"] = function["description"]
            playbook_template["name"] = function["title"]
            playbook_template["tag"] = "#" + info_file_json["label"]
            playbook_template["recordTags"] = get_tags(info_file_json)
            playbook_template["isActive"] = config.getboolean('Workflow_Info', 'Workflow_isActive')  # False
            playbook_template["debug"] = config.getboolean('Workflow_Info', 'Workflow_Debug')  # False
            playbook_template["singleRecordExecution"] = config.getboolean('Workflow_Info',
                                                                           'Workflow_singleRecordExecution')  # False
            playbook_template["parameters"] = []
            playbook_template["synchronous"] = config.getboolean('Workflow_Info', 'Workflow_synchronous')  # False
            playbook_template["triggerStep"] = "/api/3/workflow_steps/" + alert_step["uuid"]
            playbook_template["steps"] = [alert_step, connector_function_step]
            playbook_template["routes"] = [
                create_routes(function["title"], alert_step["uuid"], connector_function_step["uuid"])]
            all_playbooks_list.append(playbook_template)
        return all_playbooks_list
    except Exception as err:
        print("create_workflow: " + str(err))


def get_tags(info_file_json):
    recordTags = eval(config.get('Alert_Step_Info', 'Alert_Step_Tags'))
    if not recordTags:
        name = info_file_json.get("name", "")
        if name:
            recordTags = [name]
        else:
            raise Exception("connector name not found.")
    return recordTags


def create_collection(info_file_json):
    try:
        new_playbook_collection = {}
        collection_data = {}
        collection_data["uuid"] = str(uuid.uuid4())
        collection_data["@type"] = "WorkflowCollection"

        collection_data["name"] = "Sample - {Dummy_Connector} - {connector_version}".format(
            Dummy_Connector=info_file_json["label"], connector_version=info_file_json["version"])
        collection_data["description"] = info_file_json["description"]
        collection_data["visible"] = eval(config.get('Collection_Info', 'Collection_Visible'))
        collection_data["image"] = eval(config.get('Collection_Info', 'Collection_Image'))

        collection_data["recordTags"] = get_tags(info_file_json)

        # This function create playbook workflows.
        collection_data["workflows"] = create_workflow(collection_data["uuid"], info_file_json)
        new_playbook_collection["type"] = "workflow_collections"
        new_playbook_collection["data"] = [collection_data]
        return new_playbook_collection
    except Exception as err:
        print("create_collection: " + str(err))


def read_input():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--connector-info", required=True, help="This is connector json file path")
        parser.add_argument("--output-path", help="This is output file path", default=None)
        parser.add_argument("--config-path", help="This is config file path", default=None)
        args = parser.parse_args()
        if len(sys.argv) <= 1:
            print("Please provide input --connector-info")
            exit(0)
        return args
    except Exception as err:
        print("read_input: " + str(err))


def read_config_file(config_path):
    try:
        config = configparser.RawConfigParser()
        config.read(config_path)
        return config
    except Exception as err:
        print("read_config_file: " + str(err))


def validate_input(args: argparse.Namespace) -> None:
    if not is_path_exist(args.connector_info):
        raise Exception(f"Connector info path does not exist. Path: {args.connector_info}")
    if args.output_path is None:
        args.output_path = os.path.join(get_dir_name(args.connector_info), "playbooks")
    if args.config_path is None:
        args.config_path = os.path.join(os.path.dirname(__file__), "config", "playbook_config.ini")
    if not is_path_exist(args.output_path):
        create_path(args.output_path)


def main():
    try:
        args = read_input()
        validate_input(args)
        global config
        config = read_config_file(args.config_path)
        # This function read connector info.json file for get function details.
        info_file_json = read_info_json_file(args.connector_info)

        # This function create new collection for given connector.
        new_playbook_collection = create_collection(info_file_json)

        # Dump generated collection into JSON file.
        with open("{path}/playbooks.json".format(Dummy_Connector=info_file_json["label"],
                                                 connector_version=info_file_json["version"], path=args.output_path),
                  'w') as outfile:
            json.dump(new_playbook_collection, outfile, indent=2)
    except Exception as err:
        print(str(err))


if __name__ == "__main__":
    main()
