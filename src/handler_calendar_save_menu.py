import db_utils


def main(body):
    db_utils.delete_menu_from_calendar(body['user_id'], body['date'])
    db_utils.save_menu_to_calendar(body['user_id'], body['date'], body['menu_id'])
    return {}
