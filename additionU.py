import json

file_path = 'schedule.json'
new_data = {
    "chat_id": ["Engineer"]
}

try:
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)
except FileNotFoundError:
    existing_data = []

existing_data.append(new_data)

with open(file_path, 'w') as json_file:
    json.dump(existing_data, json_file)

print("New data has been appended to schedule.json")



# import json
#
# with open('schedule.json', 'r') as json_file:
#     data_read = json.load(json_file)
#
# print("Data read from schedule.json:", data_read)
