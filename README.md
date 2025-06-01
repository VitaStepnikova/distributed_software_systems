# Quick-start guide
## 0. Prerequisites
| Tool                 | Tested version            | Purpose                                     |
| -------------------- | ------------------------- | ------------------------------------------- |
| Python               | ≥ 3.10 (venv recommended) | run / test the code, generate stubs locally |
| pip                  | latest                    | install Python deps                         |
| Docker Desktop       | ≥ 28                      | containerise & run the gRPC service         |
| `grpcurl` (optional) | 1.8+                      | interactive reflection testing              |

## 1. Clone & prepare
```
git clone https://github.com/VitaStepnikova/distributed_software_systems.git
cd distributed_software_systems
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
## 2. Compile the protobuf stubs (two ways)
### Option A Local tooling
```
python -m grpc_tools.protoc \
  -I ./Lab_2 \
  --python_out=./Lab_2 \
  --grpc_python_out=./Lab_2 \
  ./Lab_2/items.proto
```
### Option B Pre-built Docker image
```
docker run --rm \
  -v "${PWD}/Lab_2":/defs \
  namely/protoc-all:1.33_2 \
  -f items.proto -l python -o /defs
```
Generated files: items_pb2.py, items_pb2_grpc.py.

## 3. Build the gRPC service container
```
cd Lab_2
docker build -t my-grpc-server:1.0 .
```
## 4. Run (or re-run) the container
```
# Stop & remove an old instance if it exists
docker rm -f grpc-server-container 2>/dev/null || true

# Start fresh
docker run -d --name grpc-server-container -p 50051:50051 my-grpc-server:1.0
docker logs -f grpc-server-container         # tail the logs
```
## 5. Run the example client
```
# still inside the venv
python Lab_2/grpc_client.py
```
**The script demonstrates:**
- Unary – GetItemById
- Server-streaming – ListAllItems
- Client-streaming – AddItems
- Bidirectional – ChatAboutItems

## 6. Reflection with grpcurl (optional)
```
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 list items.ItemService
grpcurl -plaintext -d '{"id":1}' localhost:50051 items.ItemService/GetItemById
```
## 7. Performance tests
| Script                  | Location | What it does                                        |
| ----------------------- | -------- | ----------------------------------------------------|
| `parallel_rest_test.py` | `Lab_1/` | fires concurrent REST calls at `localhost:5000`     |
| `grpc_test.py`          | `Lab_2/` | fires concurrent gRPC calls at `localhost:50051`    |
| `general_test.py`       | `Lab_2/` | orchestrates both scripts for 100 → 20 000 requests |

## 8. Rebuilding after code changes
1. Edit your Python files.
2. Re-generate stubs if you changed items.proto.
3. Re-build & re-run the image:
```
docker build -t my-grpc-server:1.1 .
docker rm -f grpc-server-container
docker run -d --name grpc-server-container -p 50051:50051 my-grpc-server:1.1
```
