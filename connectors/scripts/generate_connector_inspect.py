""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

import argparse
import os, requests
import json, logging, shutil

from connectors.scripts.utils import is_path_exist, create_path, get_dir_name
from os.path import join
from pathlib import Path
from json2html import *

from logging.handlers import RotatingFileHandler
from camelcase import CamelCase
from PIL import Image

LOG_FILE_PATH = join(os.path.dirname(os.path.abspath(__file__)), 'unit_test.log')
output_dir = join(os.path.dirname(os.path.abspath(__file__)), 'sanity_output')
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=10)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel('INFO')
cs = CamelCase(' is ', ' for ', ' to ', ' of ', ' from ', 'URL', 'an', 'a', 'in')


class ConnectorInspect:
    def __init__(self, connector_info: str, output_path: str) -> None:
        self.connector_info: str = connector_info
        self.output_path: str = output_path
        self.validate_input_field()
        self.generate_connector_review()

    def validate_input_field(self) -> None:
        if not is_path_exist(self.connector_info):
            raise Exception(f"Connector path is not valid. Path: {self.connector_info}")
        if self.output_path is None:
            self.output_path = get_dir_name(self.connector_info)
        if not is_path_exist(self.output_path):
            create_path(self.output_path)

    def generate_connector_review(self):
        connector_info_path = self.connector_info
        playbook_path = get_dir_name(self.connector_info) + "/playbooks/playbooks.json"
        run_sanity(connector_info_path, playbook_path, self.output_path)


def _get_json_data(json_file_path):
    if Path(json_file_path).is_file():
        json_data = json.loads(open(json_file_path).read())
        return json_data


def check_description(info_json_data):
    try:
        result = {'Test Case': '', 'Result': '', 'Status': 'Pass'}
        output = []
        for operation in info_json_data.get('operations'):
            description = operation.get('description')
            if not description:
                result['Status'] = f'<p style="color:red"> Fail </p>'
                output.append({'Action Name': f'<p style="color:red"> {operation.get("title")} </p>',
                               "Description": f'<p style="color:red"> {description} </p>',
                               'Description Available': f'<p style="color:red"> {False} </p>'})
            else:
                output.append({'Action Name': f'<p style="color:green"> {operation.get("title")} </p>',
                               "Description": f'<p style="color:green"> {description} </p>',
                               'Description Available': f'<p style="color:green"> {True} </p>'})
        result['Result'] = output
        result['Test Case'] = 'Check Description is non empty'
        return result

    except Exception as err:
        logger.info("check_description:{}".format(err))


def check_conn_descripton_non_camel(info_json_data):
    try:
        result = {'Test Case': 'Action Description Non Camel Case', 'Result': '', 'Status': 'Pass'}
        output = []
        for operation in info_json_data.get('operations'):
            desc = operation.get('description')
            cs_string = ""
            if desc:
                cs_string = cs.hump(desc)
                if cs_string != desc:
                    output.append({'Action Name': f'<p style="color:green"> {operation.get("title")} </p>',
                                   "Description": f'<p style="color:green"> {desc} </p>',
                                   'Camel Case': f'<p style="color:green"> {True} </p>'})
            else:
                result['Status'] = f'<p style="color:red"> Fail </p>'
                output.append({'Action Name': f'<p style="color:red"> {operation.get("title")} </p>',
                               "Description": f'<p style="color:red"> {desc} </p>',
                               'Camel Case': f'<p style="color:red"> {False} </p>'})

        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_conn_descripton_non_camel:{}".format(err))


def check_pb_descripton_non_camel(pb_json_data):
    try:
        logger.warning("check_pb_descripton_non_camel")
        result = {'Test Case': 'PlayBook Description Non Camel Case', 'Result': '', 'Status': 'Pass'}
        output = []
        wf = pb_json_data.get('data')[0]
        logger.warning("pb_json_data:{}".format(wf))
        workflows_from_file = wf.get('workflows')
        for workflows in workflows_from_file:
            logger.warning("List of WF:{}".format(workflows))
            name = workflows.get('name')
            desc = workflows.get('description')
            logger.warning("name:{0}desc:{1}".format(name, desc))
            cs_string = ""
            if desc:
                cs_string = cs.hump(desc)
            logger.warning("AFTER CAMEL CASE CHECK")
            if cs_string != desc:
                output.append({'PlayBooks Name': f'<p style="color:green"> {name} </p>',
                               "Description": f'<p style="color:green"> {desc} </p>',
                               'Camel Case': f'<p style="color:green"> {True} </p>'})
            else:
                result['Status'] = f'<p style="color:red"> Fail </p>'
                output.append(
                    {'PlayBooks Name': f'<p style="color:red"> {name} </p>',
                     "Description": f'<p style="color:red"> {desc} </p>',
                     'Camel Case': f'<p style="color:red"> {False} </p>'})
        logger.warning("BEFORE APPENDING")
        result['Result'] = output
        logger.warning("AFTER APPENDING")
        return result
    except Exception as err:
        logger.info("check_pb_descripton_non_camel:{}".format(err))


def check_pb_coll_description_non_camel(pb_json_data):
    try:
        logger.warning("inside check_pb_coll_description_non_camel:{}".format(pb_json_data))
        result = {'Test Case': 'PlayBook Collection Description Non Camel Case', 'Result': '', 'Status': 'Pass'}
        output = []
        desc = pb_json_data.get('data')[0].get('description')
        cs_string = ""
        if desc:
            cs_string = cs.hump(desc)
        if cs_string != desc:
            output.append({"PlayBooks Collection Description": f'<p style="color:green"> {desc} </p>',
                           'Non Camel Case': f'<p style="color:green"> {True} </p>'})
        else:
            result['Status'] = f'<p style="color:red"> Fail </p>'
            output.append({"PlayBooks Collection Description": f'<p style="color:red"> {desc} </p>',
                           'Camel Case': f'<p style="color:red"> {False} </p>'})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_pb_coll_description_non_camel:{}".format(err))


def check_function_name(info_json_data):
    try:
        result = {'Test Case': 'Action Name is in Camel Case', 'Result': '', 'Status': 'Pass'}
        output = []
        for operation in info_json_data.get('operations'):
            function_name = operation.get('title')
            cs_string = cs.hump(function_name)
            if cs_string == function_name:
                output.append({"Action Name": f'<p style="color:green"> {operation.get("title")} </p>',
                               'Camel Case': f'<p style="color:green"> {True} </p>'})
            else:
                result['Status'] = f'<p style="color:red"> Fail </p>'
                output.append({"Action Name": f'<p style="color:red"> {operation.get("title")} </p>',
                               'Camel Case': f'<p style="color:red"> {False} </p>'})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_function_name:{}".format(err))


def check_pb_disabled(pb_json_data):
    try:
        result = {'Test Case': 'Playbooks are Inactive', 'Result': '', 'Status': 'Pass'}
        output = []
        for workflows in pb_json_data.get('data')[0].get('workflows'):
            name = workflows.get('name')
            active = workflows.get('isActive')
            if not active:
                output.append({"PlayBooks Name": f'<p style="color:green"> {name} </p>',
                               'InActive': f'<p style="color:green"> {True} </p>'})
            else:
                result['Status'] = f'<p style="color:red"> Fail </p>'
                output.append({"PlayBooks Name": f'<p style="color:red"> {name} </p>',
                               'InActive': f'<p style="color:red"> {False} </p>'})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_pb_disabled:{}".format(err))


def check_pb_step_names(pb_json_data):
    try:
        result = {'Test Case': 'Playbook Names in Camel Case', 'Result': '', 'Status': 'Pass'}
        output = []
        for workflows in pb_json_data.get('data')[0].get('workflows'):
            name = workflows.get('name')
            cs_string = cs.hump(name)
            if cs_string == name:
                output.append({"PlayBooks Name": f'<p style="color:green"> {name} </p>',
                               'Camel Case': f'<p style="color:green"> {True} </p>'})
            else:
                result['Status'] = f'<p style="color:red"> Fail </p>'
                output.append({"PlayBooks Name": f'<p style="color:red"> {name} </p>',
                               'Camel Case': f'<p style="color:red"> {False} </p>'})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_pb_step_names:{}".format(err))


def check_pb_name(pb_json_data):
    try:
        result = {'Test Case': 'Playbook Collection Name in Camel Case', 'Result': '', 'Status': 'Pass'}
        output = []
        pb_name = pb_json_data.get('data')[0].get('name')
        cs_string = cs.hump(pb_name)
        if cs_string == pb_name:
            output.append({"PlayBook Collection Name": f'<p style="color:green"> {pb_name} </p>',
                           'Camel Case': f'<p style="color:green"> {True} </p>'})
        else:
            result['Status'] = f'<p style="color:red"> Fail </p>'
            output.append({"PlayBook Collection Name": f'<p style="color:red"> {pb_name} </p>',
                           'Camel Case': f'<p style="color:red"> {False} </p>'})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_pb_name:{}".format(err))


def check_image_size(connector_path, info_json_data):
    try:
        result = {'Test Case': 'Check Image Sizes', 'Result': '', 'Status': 'Pass'}
        output = []
        im_small = Image.open(connector_path + '/images/' + info_json_data.get('icon_small_name'))
        im_large = Image.open(connector_path + '/images/' + info_json_data.get('icon_large_name'))
        s_width, s_height = im_small.size
        l_width, l_height = im_large.size
        small_status = large_status = False
        if s_height == s_width == 32:
            small_status = True
        if l_height == l_width == 80:
            large_status = True
        output.append({'image': info_json_data.get('icon_small_name'), 'Correct size': small_status})
        output.append({'image': info_json_data.get('icon_large_name'), 'Correct size': large_status})
        result['Result'] = output
        shutil.copy(connector_path + '/images/' + info_json_data.get('icon_small_name'), output_dir)
        shutil.copy(connector_path + '/images/' + info_json_data.get('icon_large_name'), output_dir)
        return result
    except Exception as err:
        logger.info("check_image_size:{}".format(err))


def check_help_doc(info_json_data):
    try:
        result = {'Test Case': 'Check Online Help Doc Present', 'Result': '', 'Status': 'Pass'}
        url = info_json_data.get('help_online', "")
        output = []
        if not url:
            result['Status'] = f'<p style="color:red"> Fail </p>'
            output.append({"Help Doc Link": f'<p style="color:red"> {url} </p>',
                           'Doc Link Present': f'<p style="color:red"> {False} </p>'})
        else:
            response = requests.request("GET", url)
            if response.ok:
                output.append({"Help Doc Link": f'<p style="color:green"> {url} </p>',
                               'Doc Link Present': f'<p style="color:green"> {True} </p>'})
            else:
                result['Status'] = f'<p style="color:red"> Fail </p>'
                output.append({"Help Doc Link": f'<p style="color:red"> {url} </p>',
                               'Doc Link Present': f'<p style="color:red"> {False} </p>'})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_help_doc:{}".format(err))

def check_tags(pb_json_data):
    try:
        result = {'Test Case': 'PlayBook Tag', 'Result': '', 'Status': 'Pass'}
        output = []
        for workflows in pb_json_data.get('data')[0].get('workflows'):
            tag = workflows.get('tag')
            name = workflows.get('name')
            if tag:
                output.append({"PlayBooks Name": f'<p style="color:green"> {name} </p>',
                               'Tag Present': f'<p style="color:green"> {True} </p>'})
            else:
                result['Status'] = f'<p style="color:red"> Fail </p>'
                output.append({"PlayBooks Name": f'<p style="color:red"> {name} </p>',
                               'Tag Present': f'<p style="color:red"> {False} </p>'})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_pb_tags:{}".format(err))


def check_debug_mode_off(pb_json_data):
    try:
        result = {'Test Case': 'PlayBook Debug Mode', 'Result': '', 'Status': 'Pass'}
        output = []
        for workflows in pb_json_data.get('data')[0].get('workflows'):
            debug = workflows.get('debug')
            name = workflows.get('name')
            if not debug:
                output.append({"PlayBooks Name": f'<p style="color:green"> {name} </p>',
                               'Debug Off': f'<p style="color:green"> {True} </p>'})
            else:
                result['Status'] = f'<p style="color:red"> Fail </p>'
                output.append({"PlayBooks Name": f'<p style="color:red"> {name} </p>',
                               'Debug Off': f'<p style="color:red"> {False} </p>'})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_debug_mode_off:{}".format(err))


def check_publisher_and_cs_approved(info_json_data):
    try:
        result = {'Test Case': 'Connector Publisher and CS Approved', 'Result': '', 'Status': 'Pass'}
        output = []
        cs_approved = info_json_data.get('cs_approved')
        publisher = info_json_data.get('publisher')
        if (publisher == 'Community' and cs_approved == False):
            output.append({'Is CS Approved': cs_approved, 'Publisher': publisher})
        elif (publisher == 'Fortinet' and cs_approved == True):
            output.append({'Is CS Approved': cs_approved, 'Publisher': publisher})
        else:
            result['Status'] = f'<p style="color:red"> Fail </p>'
            output.append({'Is CS Approved': cs_approved, 'Publisher': publisher})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_publisher_and_cs_approved:{}".format(err))


def check_atleast_one_action_present(info_json_data):
    try:
        result = {'Test Case': 'Atleast One Action Present', 'Result': '', 'Status': 'Pass'}
        output = []
        operations = info_json_data.get('operations')

        if not bool(operations[0]):
            result['Status'] = f'<p style="color:red"> Fail </p>'
            output.append({"One Action Present": f'<p style="color:red"> {operations[0].get("title")} </p>',
                           'Action Available': f'<p style="color:red"> {False} </p>'})
        else:
            output.append({"One Action Present": f'<p style="color:green"> {operations[0].get("title")} </p>',
                           'Action Available': f'<p style="color:green"> {True} </p>'})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_atleast_one_action_present:{}".format(err))


def check_requirements_txt_non_restrict(requirement_path):
    try:
        result = {'Test Case': 'Check Requirements File', 'Result': '', 'Status': 'Pass'}
        output = []
        with open(requirement_path) as f:
            requirement_file_data = [line.rstrip() for line in f]

            for package in requirement_file_data:
                if '==' in package:
                    result['Status'] = f'<p style="color:red"> Fail </p>'
                    output.append({"Requirement Txt Package": f'<p style="color:red"> {package} </p>',
                                   'Version Available': f'<p style="color:red"> {True} </p>'})
                else:
                    output.append({"Requirement Txt Package": f'<p style="color:green"> {package} </p>',
                                   'Version Available': f'<p style="color:green"> {False} </p>'})
        result['Result'] = output
        return result
    except Exception as err:
        logger.info("check_requirements_txt_non_restrict:{}".format(err))


def convert_json2html(input, connector_name, connector_version, output_path):
    try:
        process = input
        res = json2html.convert(json=input)
        html_file = open(output_path + '/' + connector_name + '-validation-report.html', 'w+')
        html_file.write(
            "<html><h1>Connector Validation Test Case Report: {name} v{version}</h1></html>".format(name=connector_name,
                                                                                                    version=connector_version))

        failed_status = []
        for case in process:
            if case:
                if case['Status'] == f'<p style="color:red"> Fail </p>':
                    failed_status.append(case)

        html_file.write("<html><br><h3>Failed Test Cases: </h3></br></html>")
        result = json2html.convert(json=failed_status)
        result = result.replace("&lt;", "<")
        result = result.replace("&gt;", ">")
        result = result.replace("&quot;", "\"")
        html_file.write(result)
        html_file.write("<html><br><h3></h3></br></html>")

        html_file.write("<html><br><h2>Test Case Execution Summary: </h2></br></html>")
        res = res.replace("&lt;", "<")
        res = res.replace("&gt;", ">")
        res = res.replace("&quot;", "\"")
        html_file.write(res)

        html_file.close()
    except Exception as err:
        logger.info("convert_json2html:{}".format(err))


def run_sanity(connector_info_path, playbook_path, output_path):
    print('sanity')

    final_result = []
    connector_path = os.path.dirname(connector_info_path)
    if os.path.isdir(connector_path):
        if os.path.isdir(connector_path):
            info_file = connector_path + "/info.json"
            info_json_data = _get_json_data(info_file)

            pb_json_data = _get_json_data(playbook_path)
            connector_name = info_json_data.get('label')
            connector_version = info_json_data.get('version')
            description_result = check_description(info_json_data)
            connector_description_result = check_conn_descripton_non_camel(info_json_data)
            playbook_description_result = check_pb_descripton_non_camel(pb_json_data)
            playbook_collection_description_result = check_pb_coll_description_non_camel(pb_json_data)
            function_name_result = check_function_name(info_json_data)
            playbook_disabled_result = check_pb_disabled(pb_json_data)
            playbook_step_names_result = check_pb_step_names(pb_json_data)
            playbook_name_result = check_pb_name(pb_json_data)
            image_size_result = check_image_size(connector_path, info_json_data)
            help_doc_result = check_help_doc(info_json_data)
            tags_result = check_tags(pb_json_data)
            debug_mode_off_result = check_debug_mode_off(pb_json_data)
            publisher_result = check_publisher_and_cs_approved(info_json_data)
            one_action_present_result = check_atleast_one_action_present(info_json_data)

            final_result.append(description_result)
            final_result.append(connector_description_result)
            final_result.append(playbook_description_result)
            final_result.append(playbook_collection_description_result)
            final_result.append(function_name_result)
            final_result.append(playbook_disabled_result)
            final_result.append(playbook_step_names_result)
            final_result.append(playbook_name_result)
            final_result.append(image_size_result)
            final_result.append(help_doc_result)
            final_result.append(tags_result)
            final_result.append(debug_mode_off_result)
            final_result.append(publisher_result)
            final_result.append(one_action_present_result)
            if os.path.exists(connector_path + '/requirements.txt'):
                requirements_txt_result = check_requirements_txt_non_restrict(connector_path + '/requirements.txt')
                final_result.append(requirements_txt_result)
            convert_json2html(final_result, connector_name, connector_version, output_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-info", type=str, required=True, help="info.json path")
    parser.add_argument("--output-path", type=str, required=False, help="Output path", default=None)

    args = parser.parse_args()

    ConnectorInspect(args.connector_info, args.output_path)


if __name__ == "__main__":
    main()
