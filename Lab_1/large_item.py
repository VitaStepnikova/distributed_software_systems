import json

large_item = {
    "id": 3,
    "name": "Test 3 Item",
    "description": "This is a detailed description of Test 3 Item. " * 1000,
    "tags": ["electronics", "furniture", "gadgets", "home", "office"],
    "metadata": {
        "weight": "2kg",
        "dimensions": "30x20x10 cm",
        "manufacturer": "Test Manufacturer",
        "warranty": "2 years",
        "origin": "Germany"
    },
    "history": [
        {"date": "2025-01-01", "event": "Created"},
        {"date": "2025-02-15", "event": "Updated"},
        {"date": "2025-03-20", "event": "Sold"}
    ]
}

with open('items.json', 'w') as f:
    json.dump([large_item], f, indent=4)

print("Item saved successfully!")
