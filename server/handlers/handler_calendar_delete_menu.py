import utils.db_utils as db_utils
import utils.yaml_schema_parser as yaml_schema_parser


def main(body):
    db_utils.delete_menu_from_calendar(body['user_id'], body['date'], body['menu_id'])

    return yaml_schema_parser.parse_json_to_handler_response({}, '/calendar/delete_menu', 'post')
