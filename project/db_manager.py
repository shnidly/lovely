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


def gen_new_contact(name, phone_num, time_zone, next_time_to_contact):
    return {
        'name': name,
        'time': {
            'last-time-since-contact': 0,
            'next-time-to-contact': next_time_to_contact
        },
        'holidays': {},
        'profile': {
            'phone-number': phone_num,
            'time-zone': time_zone
        }
    }


def load(data):
    return json.loads(data)
