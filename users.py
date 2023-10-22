import json

class User:
    def __init__(self, username, address, description, email):
        self.username = username
        self.email = email
        self.description = description
        self.address = address

    def to_json(self):
        user_dict = {
            'username': self.username,
            'email': self.email,
            'description': self.description,
            'address': self.address
        }
        return json.dumps(user_dict)