import grpc
import time
import items_pb2
import items_pb2_grpc

# Setting up a connection to the server
channel = grpc.insecure_channel('localhost:50051')

stub = items_pb2_grpc.ItemServiceStub(channel)

print("=== Unary RPC ===")
response = stub.GetItemById(items_pb2.ItemRequest(id=1))
print(f"ID: {response.id}, Name: {response.name}")

print("\n=== Server Streaming RPC ===")
responses = stub.ListAllItems(items_pb2.Empty())
for item in responses:
    print(f"ID: {item.id}, Name: {item.name}")

print("\n=== Client Streaming RPC ===")
def generate_items():
    items = [
        items_pb2.Item(name="Streamed Item 1"),
        items_pb2.Item(name="Streamed Item 2"),
        items_pb2.Item(name="Streamed Item 3"),
    ]
    for item in items:
        print(f"Sending: {item.name}")
        yield item
        time.sleep(1)

response = stub.AddItems(generate_items())
print(f"Result of adding: {response.count} items added")

print("\n=== Bidirectional Streaming RPC ===")
def chat_stream():
    messages = [
        items_pb2.ChatMessage(user="Client", message="Hello, server!"),
        items_pb2.ChatMessage(user="Client", message="How are you?"),
        items_pb2.ChatMessage(user="Client", message="Goodbye!")
    ]
    for msg in messages:
        print(f"{msg.user}: {msg.message}")
        yield msg
        time.sleep(1)

responses = stub.ChatAboutItems(chat_stream())
for response in responses:
    print(f"Server: {response.message}")
