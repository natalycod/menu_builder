import db_utils
import utils.yaml_schema_parser as yaml_schema_parser


def main(body):
    db_utils.delete_menu_from_calendar(body['user_id'], body['date'])
    db_utils.save_menu_to_calendar(body['user_id'], body['date'], body['menu_id'])
    return yaml_schema_parser.parse_json_to_handler_response({}, '/calendar/save_menu', 'post')
