### FortiSOAR Connector Engine

This library bundles multiple utilities to assist FortiSOAR integrations developments. This package include default import for 
connectors and some helpful scripts like: Execute any actions, Generate sample playbooks, Generate sample docs,
Generate connector review and so on.

#### Installation
    > git clone https://github.com/fortinet-fortisoar/fortisoar-connector-engine
    > cd ./fortisoar-connector-engine
    > source <env_path>/env/bin/activate (Optional but recommended)
    > pip3 install ./build/fortisoar_connector_engine-1.0.0-py3-none-any.whl

#### Usage:
1. Execute a connector action
    > python3 -m connectors.scripts.execute_operation --connector-path <connector_parent_path> --connector-name <connector_name> --config-name <config_name> --operation-name <operation_name> --local-data-path <local_data_path>
    
2. Generate Sample Playbooks
    > python3 -m connectors.scripts.generate_sample_playbook --connector-info <connector_info_path> --output-path <output_path> --config-path <playbook_config_path>

3. Generate Sample Document
   > python3 -m connectors.scripts.generate_document --connector-info <connector_info_path> --output-path <output_path>

4. Generate Connector Review
   > python3 -m connectors.scripts.generate_connector_review --connector-info <connector_info_path> --output-path <output_path>

Where:

--connector-path: Parent folder path of the connector.

--connector-name: Name of connector whose actions you want to execute.

--config-name: Name of the config that you want to use while running an action.

--operation-name: Name of the operation that you want to execute.

--local-data-path: Absolute path where connector local data exist.

--connector-info: Absolute path of the connector "info.json".

--output-path: Path where you want to store the result.



