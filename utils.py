import json


async def link_in_json(link, user_id):
    with open('data.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        if link in file_data['items']:
            return True
        else:
            return False


async def add_link_json(link, user_id):
    with open('data.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        file_data['items'].append(link)
        file.seek(0)
        json.dump(file_data, file, ensure_ascii=False, indent=4)
