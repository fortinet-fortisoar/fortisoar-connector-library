### FortiSOAR Connector Engine

This library bundles multiple utilities to assist FortiSOAR integrations developments. This package include default import for 
connectors and some helpful scripts like: Execute any actions, Generate sample playbooks, Generate sample docs,
Generate connector review and so on.

#### Installation
    > git clone https://github.com/fortinet-fortisoar/fortisoar-connector-engine
    > cd ./fortisoar-connector-engine
    > source <env_path>/env/bin/activate (Optional but recommended)
    > python3 ./setup.py bdist_wheel
    > pip3 install ./build/fortisoar_connector_engine-1.0.0-py3-none-any.whl

#### Usage:
1. Execute a connector action
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

--connector-path: Specify parent folder absolute path of the connector.

--connector-name: Specify the name of the connector whose actions you want to execute.

--config-name: Specify the name of the config that you want to use while running an action.

--operation-name: Specify the name of the operation that you want to execute.

--local-data-path: Specify the absolute path where connector local data exist.

--connector-info: Specify absolute path of the connector "info.json".

--output-path: Specify absolute path where you want to store the result.



