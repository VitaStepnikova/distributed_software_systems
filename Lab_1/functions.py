import json
from ItemClass import Item


def save_items_to_file(items, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([item.to_dict() for item in items], f, indent=4)

def load_items_from_file(filename, item_id=None):
    with open(filename, 'r', encoding='utf-8') as f:
        items_data = json.load(f)
        
        if item_id is not None:
            for item in items_data:
                if item['id'] == item_id:
                    return Item(item['id'], item['name'], item['description'], item['tags'], item['metadata'], item['history'])
            return None  
        
        return [Item(item['id'], item['name'], item['description'], item['tags'], item['metadata'], item['history']) for item in items_data]

