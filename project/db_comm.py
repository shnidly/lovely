import firebase


class Contact:
    def __init__(self, name, frequency, last_contacted, phone_number, birthday, timezone, photo_id=None):
        self.name = name
        self.frequency = frequency
        self.last_contacted = last_contacted
        self.phone_number = phone_number
        self.birthday = birthday
        self.timezone = timezone
        self.photo_id = photo_id

    def create(self):
        data = {
            "name": self.name,
            "frequency": self.frequency,
            "last_contacted": self.last_contacted,
            "phone_number": self.phone_number,
            "birthday": self.birthday,
            "timezone": self.timezone,
            "photo_id": self.photo_id

        }

        return data


def get_contact_from_name(name):
    database = firebase.FirebaseApplication('https://crackling-torch-603.firebaseio.com/', None)
    results = database.get('/contacts', None).values()
    my_result_list = [result for result in results if result["name"] == name]
    if len(my_result_list) > 1:
        raise Exception("Has duplicates")
    if len(my_result_list) == 0:
        return None
    else:
        my_result = my_result_list

    return my_result
