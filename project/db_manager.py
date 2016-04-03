import json


def gen_new_user(name, phone_num, time_zone):
    return {
                'name': name,
                'time': {
                    'last-time-since-contact': 0,
                    'next-time-to-contact': 0
                },
                'holidays': {},
                'profile': {
                    'phone-number': phone_num,
                    'time-zone': time_zone
                }
            }


def load(data):
    return json.loads(data)
