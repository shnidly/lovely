import json
import datetime
import time


def get_millis():
    return int(round(time.time()))


def gen_new_user(username, password, email):
    return {
        'username': username,
        'password': password,
        'email': email,
        'profile': {
            'photo-id': 'default.jpg'
        },
    }


def gen_new_contact(owner, name, phone_num, time_zone, friend_type):
    return {
        'owner': owner,
        'name': name,
        'time': {
            'last-time-since-contact': 0,
            'next-time-to-contact': 604800
        },
        'holidays': '',
        'profile': {
            'birthday': '',
            'phone-number': phone_num,
            'time-zone': time_zone,
            'friend-type': friend_type
        }
    }


def add_new_contact(owner, name, next_time_to_contact, birthday, phone_num, time_zone, friend_type, holidays):
    return {
        'owner': owner,
        'name': name,
        'time': {
            'last-time-since-contact': 0,
            'next-time-to-contact': next_time_to_contact
        },
        'holidays': holidays,
        'profile': {
            'birthday': birthday,
            'phone-number': phone_num,
            'time-zone': time_zone,
            'friend-type': friend_type
        }
    }


def load(data):
    return json.loads(data)


def millis_to_timestamp(millis):
    return datetime.datetime.fromtimestamp(float(millis)).strftime('%Y-%m-%d %H:%M:%S.%f')
