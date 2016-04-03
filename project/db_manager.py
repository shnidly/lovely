import json


def gen_new_user(username, password, email):
    return {
        'username': username,
        'password': password,
        'email': email,
        'profile': {
            'photo-id': 'default.jpg'
        },
    }


def gen_new_contact(owner, name, phone_num, time_zone):
    return {
        'owner': owner,
        'name': name,
        'time': {
            'last-time-since-contact': 0
        },
        'holidays': {},
        'profile': {
            'phone-number': phone_num,
            'time-zone': time_zone
        }
    }


def load(data):
    return json.loads(data)
