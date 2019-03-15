class AccountsUtils:
    """
    Utility methods related to Accounts Application
    """

    @staticmethod
    def get_user_full_name(user):
        if isinstance(user, list):
            user_name_list = ''
            for i, _ in enumerate(user):
                if i != 0:
                    user_name_list += ' / '
                if _.first_name or _.last_name:
                    user_name_list += "{} {}".format(_.first_name, _.last_name)
                    user_name_list += "{}".format(_.username.split('@')[0])
            return user_name_list
        if user.first_name or user.last_name:
            return "{} {}".format(user.first_name, user.last_name)
        return "{}".format(user.username.split('@')[0])

    @staticmethod
    def get_readable_user_type(type):
        return type.replace('_', ' ').lower().capitalize()
