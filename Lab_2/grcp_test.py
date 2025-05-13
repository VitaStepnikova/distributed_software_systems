import grpc
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from items_pb2 import ItemRequest
from items_pb2_grpc import ItemServiceStub

NUM_REQUESTS = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
GRPC_ADDRESS = 'localhost:50051'
OUTPUT_FILE = "grpc_times2.txt"


def make_request(_):
    start = time.time()
    channel = grpc.insecure_channel(GRPC_ADDRESS)
    stub = ItemServiceStub(channel)
    response = stub.GetItemById(ItemRequest(id=3))
    end = time.time()
    duration = end - start

    with open(OUTPUT_FILE, "a") as f:
        f.write(f"{duration}\n")

    print(f"Received: {response.name} in {duration:.4f} seconds")
    return duration


def main():
    open(OUTPUT_FILE, "w").close()

    print(f"Starting parallel gRPC requests with {NUM_REQUESTS} requests...")

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(make_request, range(NUM_REQUESTS)))

    times = [result for result in results if result is not None]

    print(f"Total time for {len(times)} requests: {sum(times):.4f} seconds")
    print(f"Average time per request: {sum(times) / len(times):.4f} seconds")

    with open(OUTPUT_FILE, "a") as f:
        f.write(f"\nTotal time for {len(times)} requests: {sum(times):.4f} seconds\n")
        f.write(f"Average time per request: {sum(times) / len(times):.4f} seconds")

    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
