### FortiSOAR Connector Engine

This library bundles multiple utilities to aid FortiSOAR integration developments. 
This package includes default import of connectors and scripts that enable you to perform 
tasks such as "executing actions", "generating sample playbooks", "generating sample docs",
"generating connector inspect" and other operations. 

#### Installation
    > git clone https://github.com/fortinet-fortisoar/fortisoar-connector-engine
    > cd ./fortisoar-connector-engine
    > source <env_path>/env/bin/activate (Optional but recommended)
    > python3 ./setup.py bdist_wheel
    > pip3 install ./build/fortisoar_connector_engine-1.0.0-py3-none-any.whl

#### Usage: 

The following is a list of commands that you can use to perform different actions: 

1. Execute a Connector Action
    > python3 -m connectors.scripts.execute_operation --connector-path <connector_parent_path> --connector-name <connector_name> --config-name <config_name> --operation-name <operation_name> --local-data-path <local_data_path>
    
2. Generate Sample Playbooks
    > python3 -m connectors.scripts.generate_sample_playbook --connector-info <connector_info_path> --output-path <output_path> --config-path <playbook_config_path>

3. Generate Sample Document
   > python3 -m connectors.scripts.generate_document --connector-info <connector_info_path> --output-path <output_path>

4. Generate Connector Inspect
   > python3 -m connectors.scripts.generate_connector_inspect --connector-info <connector_info_path> --output-path <output_path>

5. Clean Output Schema
   > python3 -m connectors.scripts.clean_output_schema --connector-info <connector_info_path>

Where:

--connector-path: Specify the absolute path of the connectors’ parent folder.

--connector-name: Specify the name of the connector whose actions you want to execute. 

--config-name: Specify the name of the configuration you want to use to run an action.

--operation-name: Specify the name of the operation you want to execute.

--local-data-path: Specify the absolute path of the connector’s local data.

--connector-info: Specify the absolute path of the connector’s “info.json”. 

--output-path: Specify the absolute path to store the result of the connector’s action.



