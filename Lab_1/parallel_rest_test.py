import requests
import time
import sys
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:5000/items/3"

NUM_REQUESTS = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
OUTPUT_FILE = "rest_performance_results2.txt"


def make_request(_):
    start = time.time()
    response = requests.get(URL)
    end = time.time()
    if response.status_code == 200:
        return end - start
    else:
        print(f"Request failed with status {response.status_code}")
        return None


def main():
    open(OUTPUT_FILE, "w").close()

    print(f"Starting parallel REST requests with {NUM_REQUESTS} requests...")

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(make_request, range(NUM_REQUESTS)))

    times = [result for result in results if result is not None]

    with open(OUTPUT_FILE, 'w') as f:
        f.write("REST Performance Test Results\n")
        f.write(f"Total time for {len(times)} requests: {sum(times):.4f} seconds\n")
        f.write(f"Average time per request: {sum(times) / len(times):.4f} seconds\n")
        f.write("\nIndividual request times:\n")
        for t in times:
            f.write(f"{t:.6f}\n")

    print(f"Results have been written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
