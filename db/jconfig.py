import json


class AdminPanel:
    def __init__(self):
        self.chat_ids = {}
        self.last_user_id = 1

    def generate_user_id(self):
        new_user_id = self.last_user_id
        self.last_user_id += 1
        return new_user_id

    def add_chat_id(self, chat_id):
        user_id = self.generate_user_id()
        self.chat_ids[str(user_id)] = chat_id

    def add_chat_id_with_user_id(self, user_id, chat_id):
        self.chat_ids[str(user_id)] = chat_id

    def save_to_json(self, filename):
        with open("admins.json", 'w') as json_file:
            json.dump(self.chat_ids, json_file, indent=4)

    def load_from_json(self, filename):
        try:
            with open("admins.json", 'r') as json_file:
                self.chat_ids = json.load(json_file)
        except FileNotFoundError:
            self.chat_ids = {}


admin_panel = AdminPanel()

admin_panel.save_to_json('admins.json')

admin_panel.load_from_json('admins.json')

print(admin_panel.chat_ids)
