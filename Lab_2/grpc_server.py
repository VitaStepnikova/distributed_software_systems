import grpc
from concurrent import futures
import items_pb2
import items_pb2_grpc

import logging

# Set the logging level to ERROR to remove unnecessary INFO and DEBUG logs.
logging.basicConfig(level=logging.ERROR)

# Initialize the list of elements
items = [
    {"id": 1, "name": "Item 1", "description": "Description of Item 1." * 1000},
    {"id": 2, "name": "Item 2", "description": "Description of Item 2." * 1000},
    {"id": 3, "name": "Item 3", "description": "Description of Item 3." * 1000}
]

# ID counter for new objects
current_id = 4

class ItemService(items_pb2_grpc.ItemServiceServicer):

    def GetItemById(self, request, context):
        print(f"Запрос на получение объекта с ID: {request.id}")
        for item in items:
            if item['id'] == request.id:
                return items_pb2.Item(
                    id=item['id'], 
                    name=item['name'],
                    description=item['description']
                )
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Item not found')
        return items_pb2.Item(id=-1, name="Not Found")


    def ListAllItems(self, request, context):
        print("Request to get all objects")
        for item in items:
            yield items_pb2.Item(id=item['id'], name=item['name'])

    def AddItems(self, request_iterator, context):
        global current_id
        count = 0
        for new_item in request_iterator:
            print(f"Adding an element: {new_item.name}")
            items.append({"id": current_id, "name": new_item.name})
            current_id += 1
            count += 1
        return items_pb2.ItemsAddedResult(count=count)

    def ChatAboutItems(self, request_iterator, context):
        for message in request_iterator:
            print(f"[{message.user}]: {message.message}")
            yield items_pb2.ChatMessage(user="Server", message=f"Received: {message.message}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    items_pb2_grpc.add_ItemServiceServicer_to_server(ItemService(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
