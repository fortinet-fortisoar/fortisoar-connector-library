import argparse
from connectors.scripts.utils import is_path_exist, create_path, get_dir_name


class ConnectorReview:
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
        raise Exception("Coming soon")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--connector_info", type=str, required=True, help="info.json path")
    parser.add_argument("--output_path", type=str, required=False, help="Output path", default=None)

    args = parser.parse_args()

    ConnectorReview(args.connector_info, args.output_path)


if __name__ == "__main__":
    main()
