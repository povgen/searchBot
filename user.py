import json

from helper import r


def add_to_registered_users_list(user_id):
    registered_users = r.get('registered_users')

    if registered_users is None:
        registered_users = [user_id]
    else:
        registered_users = json.JSONDecoder().decode(registered_users)
        if user_id in registered_users:
            return
        registered_users.append(user_id)

    r.set('registered_users', json.JSONEncoder().encode(registered_users))


class User:
    user_id: int
    request_params: dict
    offset: int
    count_of_requests: int = 0
    user_info: dict

    def __init__(self, user_id):
        user_data = r.get(user_id)

        if user_data is None:
            user_data = {
                'user_id': user_id,
                'request_params': {
                    'page': 1,
                    'order': 'relevance'
                },
                'offset': 0,
            }
            add_to_registered_users_list(user_id)

        else:
            user_data = json.JSONDecoder().decode(user_data)

        self.__dict__.update(user_data)

    def to_increment_count_of_requests(self):
        self.count_of_requests += 1

    def save(self):
        r.set(self.user_id, json.JSONEncoder().encode(self.__dict__))
