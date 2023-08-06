from typing import Tuple, List
from meapi.exceptions import MeException

notification_categories = {
    'names': ['JOINED_ME', 'CONTACT_ADD', 'UPDATED_CONTACT', 'DELETED_CONTACT', 'NEW_NAME_REQUEST',
              'NEW_NAME_REQUEST_APPROVED'],
    'system': ['NAME_SUGGESTION_UPDATED', 'SPAM_SUGGESTION_APPROVED', 'TURN_ON_MUTUAL', 'NONE'],
    'comments': ['NEW_COMMENT', 'PUBLISHED_COMMENT', 'PUBLISHED_COMMENT', 'TURN_ON_COMMENTS'],
    'who_watch': ['WEEKLY_VISITS'],
    'birthday': ['BIRTHDAY'],
    'location': ['TURN_ON_LOCATION', 'SHARE_LOCATION'],
    'who_deleted': ['WEEKLY_DELETED']
}


class Notifications:
    def unread_notification_count(self) -> int:
        return self.make_request('get', '/notification/notification/count/')['count']

    def get_notifications(self,
                          page_number: int = 1,
                          results_limit: int = 20,
                          names_filter: bool = False,
                          system_filter: bool = False,
                          comments_filter: bool = False,
                          who_watch_filter: bool = False,
                          who_deleted_filter: bool = False,
                          birthday_filter: bool = False,
                          location_filter: bool = False) -> dict:
        """
        Get app notifications: new names, birthdays, comments, watches, deletes, location shares and system notifications.
        :param page_number: get_notifications['count'] / page_size = pages
        :param results_limit: limit of notifications
        :param names_filter: new or name changes
        :param system_filter: system notifications
        :param comments_filter: comments notifications
        :param who_watch_filter: who watched your profile
        :param who_deleted_filter: who deleted you from his contacts
        :param birthday_filter: contacts birthdays
        :param location_filter: shared locations
        :return: dict with notifications
        """
        args = locals()
        filters = []
        for fil, val in args.items():
            if fil.endswith("filter") and val:
                filters = [*filters, *notification_categories[fil.replace("_filter", "")]]
        params = f"?page={page_number}&page_size={results_limit}&status=distributed"
        if filters:
            params += f"&categories=%5B{'%2C%20'.join(filters)}%5D"
        return self.make_request('get', '/notification/notification/items/' + params)

    def read_notification(self, notification_id: int) -> bool:
        body = {"notification_id": int(notification_id)}
        return self.make_request('post', '/notification/notification/read/', body)['is_read']

    def change_notification_settings(self,
                                     who_deleted_notification_enabled: bool = None,
                                     who_watched_notification_enabled: bool = None,
                                     distance_notification_enabled: bool = None,
                                     system_notification_enabled: bool = None,
                                     birthday_notification_enabled: bool = None,
                                     comments_notification_enabled: bool = None,
                                     names_notification_enabled: bool = None,
                                     notifications_enabled: bool = None) -> Tuple[bool, List[str]]:
        """
        Set new settings for notifications
        :param who_deleted_notification_enabled:
        :param who_watched_notification_enabled:
        :param distance_notification_enabled:
        :param system_notification_enabled:
        :param birthday_notification_enabled:
        :param comments_notification_enabled:
        :param names_notification_enabled:
        :param notifications_enabled:
        :return: (is success, list of failed)
        """
        args = locals()
        body = {}
        for setting, value in args.items():
            if value is not None and setting != 'self':
                body[setting] = value
        if not body:
            raise MeException("You need to provide at least one setting!")

        results = self.make_request('patch', '/main/settings/', body)
        failed = []
        for setting in body.keys():
            if results[setting] != body[setting]:
                failed.append(setting)
        return not bool(failed), failed
