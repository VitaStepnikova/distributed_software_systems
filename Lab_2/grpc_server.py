import grpc
from concurrent import futures
import items_pb2
import items_pb2_grpc
from grpc_reflection.v1alpha import reflection
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Sample data
items = [
    {"id": 1, "name": "Item 1", "description": "Description of Item 1." * 1000},
    {"id": 2, "name": "Item 2", "description": "Description of Item 2." * 1000},
    {"id": 3, "name": "Item 3", "description": "Description of Item 3." * 1000}
]

current_id = 4

# Logging Interceptor
class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        metadata = handler_call_details.invocation_metadata
        logger.info(f"[Interceptor] Method called: {method}")
        return continuation(handler_call_details)

# gRPC Service Implementation
class ItemService(items_pb2_grpc.ItemServiceServicer):
    def GetItemById(self, request, context):
        logger.info(f"Received request for item with ID: {request.id}")
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
        logger.info("Received request to list all items")
        for item in items:
            yield items_pb2.Item(id=item['id'], name=item['name'])

    def AddItems(self, request_iterator, context):
        global current_id
        count = 0
        for new_item in request_iterator:
            logger.info(f"Adding new item: {new_item.name}")
            items.append({"id": current_id, "name": new_item.name})
            current_id += 1
            count += 1
        return items_pb2.ItemsAddedResult(count=count)

    def ChatAboutItems(self, request_iterator, context):
        for message in request_iterator:
            logger.info(f"[{message.user}]: {message.message}")
            yield items_pb2.ChatMessage(user="Server", message=f"Received: {message.message}")

# Server Setup
def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=100),
        interceptors=[LoggingInterceptor()]
    )
    logger.info("Interceptor initialized")

    items_pb2_grpc.add_ItemServiceServicer_to_server(ItemService(), server)

    service_names = (
        items_pb2.DESCRIPTOR.services_by_name['ItemService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    logger.info("gRPC server running on port 50051 with Reflection and Interceptor enabled")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
