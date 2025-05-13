from flask import Flask, request, jsonify
from ItemClass import Item
from functions import save_items_to_file, load_items_from_file
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# @app.route("/items", methods=["GET"])
# def items_get():
#     items = load_items_from_file('items.json')
#     return jsonify([item.to_dict() for item in items]), 200

@app.route("/items", methods=["GET"])
def items_get():
    items = load_items_from_file('items.json')
    
    # Let's add additional load to each element
    for item in items:
        item.description = "This is a very large description for testing REST vs gRPC performance." * 100
        item.metadata = {"created_at": "2025-05-10", "updated_at": "2025-05-11"}
        item.extra_data = [i for i in range(10000)]  # Add an array of 10000 elements
    
    return jsonify([item.to_dict() for item in items]), 200

@app.route("/items/<int:id>", methods=["GET"])
def items_id_get(id): 
    item = load_items_from_file('items.json', item_id=id) 
    if item:
        return jsonify(item.to_dict()), 200 
    else:
        return jsonify({"error": "Item not found"}), 404  

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    items = load_items_from_file('items.json')
    new_id = max(item.id for item in items) + 1 if items else 1
    new_item = Item(new_id, data['name'])
    items.append(new_item)
    save_items_to_file(items, 'items.json')
    return jsonify(new_item.to_dict()), 201

@app.route("/items/<int:id>", methods=["PUT"])
def update_item(id):
    items = load_items_from_file('items.json')
    item_to_update = next((item for item in items if item.id == id), None)

    if not item_to_update:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    item_to_update.name = data['name']
    save_items_to_file(items, 'items.json')
    return jsonify(item_to_update.to_dict()), 200

@app.route("/items/<int:id>", methods=["DELETE"])
def delete_item(id):
    items = load_items_from_file('items.json')
    item_to_delete = next((item for item in items if item.id == id), None)

    if not item_to_delete:
        return jsonify({"error": "Item not found"}), 404

    items.remove(item_to_delete)
    save_items_to_file(items, 'items.json')
    return jsonify({"message": "Item deleted successfully"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


