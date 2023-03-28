class NotificationsNotCreated(Exception):
    pass


class NotificationNotSent(Exception):
    pass


class UserIsOptedOut(NotificationNotSent):
    def __init__(self):
        super().__init__("User is opted out")
