### FortiSOAR Connector Engine

This package will support in local development of FortiSOAR connectors. This package include default import for 
connectors and some helpful scripts like: Execute any actions, Generate sample playbooks, Generate sample docs,
Generate connector review and so on.

#### Installation
    > git clone https://github.com/fortinet-fortisoar/fortisoar-connector-engine
    > cd ./fortisoar-connector-engine
    > source <env_path>/env/bin/activate (Optional but recommended)
    > pip3 install ./build/fortisoar_connector_engine-1.0.0-py3-none-any.whl

#### Usage:
1. Execute an action/operation
    > python3 -m connectors.scripts.execute_operation --connector_path <connector_parent_path> --connector_name <connector_name> --config_name <config_name> --operation_name <operation name> --local_data_path <local data path>
    
2. Generate Sample Playbooks
    > python3 -m connectors.scripts.generate_sample_playbook --connector_info < complete info.json path > --output_path < output path > --config_path < Playbook generation config.ini path >

3. Generate Sample Document
   > python3 -m connectors.scripts.generate_document --connector_info < info.json path > --output_path < output path >

4. Generate Connector Review
   > python3 -m connectors.scripts.generate_connector_review --connector_info < info.json file path > --output_path < output path > 
   > 

Where:

--connector_path: Parent folder path of the connector.

--connector_name: Name of connector whose actions you want to execute.

--config_name: Name of the config that you want to use while running an action.

--operation_name: Name of the operation that you want to execute.

--local_data_path: Absolute path where connector local data exist.

--connector_info: Absolute path of the connector "info.json".

--output_path: Path where you want to store the result.



