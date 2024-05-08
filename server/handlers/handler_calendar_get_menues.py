import db_utils
import utils.yaml_schema_parser as yaml_schema_parser


def main(args):
    menues = db_utils.get_menues_from_calendar(args['user_id'], args['date_start'], args['date_end'])
    result = []
    for menu in menues:
        menu_full = db_utils.get_menu(menu[1])
        result.append({
            "date": menu[0],
            "menu": menu_full.to_json(),
        })

    return yaml_schema_parser.parse_json_to_handler_response(result, '/calendar/get_menues', 'get')
