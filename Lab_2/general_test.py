import subprocess
import pandas as pd
import os
import matplotlib.pyplot as plt

# Configuration
rest_script = '/Users/vitalinaviktorivna/Desktop/distributed_sofrware_systems/Lab_1/parallel_rest_test.py'
grpc_script = '/Users/vitalinaviktorivna/Desktop/distributed_sofrware_systems/Lab_2/grcp_test.py'
rest_output_file = 'rest_performance_results2.txt'
grpc_output_file = 'grpc_times2.txt'
requests_list = [100, 500, 1000, 5000, 10000, 15000, 20000]

if not os.path.exists(rest_script):
    print(f"❌ File not found: {rest_script}")
    exit(1)

if not os.path.exists(grpc_script):
    print(f"❌ File not found: {grpc_script}")
    exit(1)

performance_data = []

for num_requests in requests_list:
    print(f"\n🚀 Running tests with {num_requests} requests...")

    try:
        print("🌐 Running REST tests...")
        result = subprocess.run(f"python3 {rest_script} {num_requests}", shell=True)

        with open(rest_output_file, 'r') as f:
            lines = f.readlines()
        
        rest_total_time, rest_avg_time = None, None
        for line in lines:
            if "Total time" in line:
                rest_total_time = float(line.split(': ')[1].strip().split()[0])
            if "Average time" in line:
                rest_avg_time = float(line.split(': ')[1].strip().split()[0])

        if rest_total_time is None or rest_avg_time is None:
            print(f"❌ Failed to parse REST results from {rest_output_file}")
            continue

    except subprocess.CalledProcessError as e:
        print("❌ Error during REST script execution:")
        print(e.stderr.decode())
        continue

    try:
        print("🔌 Running gRPC tests...")
        

        subprocess.run(f"python3 {grpc_script} {num_requests}", shell=True)


        with open(grpc_output_file, 'r') as f:
            lines = f.readlines()

        grpc_total_time, grpc_avg_time = None, None
        for line in lines:
            if "Total time" in line:
                grpc_total_time = float(line.split(': ')[1].strip().split()[0])
            if "Average time" in line:
                grpc_avg_time = float(line.split(': ')[1].strip().split()[0])

        if grpc_total_time is None or grpc_avg_time is None:
            print(f"❌ Failed to parse gRPC results from {grpc_output_file}")
            continue

    except subprocess.CalledProcessError as e:
        print("❌ Error during gRPC script execution:")
        print(e.stderr.decode())
        continue

    performance_data.append({
        "Requests": num_requests,
        "REST Total Time (s)": rest_total_time,
        "REST Avg Time (ms)": rest_avg_time * 1000,
        "gRPC Total Time (s)": grpc_total_time,
        "gRPC Avg Time (ms)": grpc_avg_time * 1000
    })

df = pd.DataFrame(performance_data)
df.to_csv("performance_comparison.csv", index=False)
print("\n📊 Performance Comparison Table:")
print(df)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(df['Requests'], df['REST Total Time (s)'], label='REST Total Time (s)', marker='o')
plt.plot(df['Requests'], df['gRPC Total Time (s)'], label='gRPC Total Time (s)', marker='o')
plt.title('Total Time Comparison')
plt.xlabel('Number of Requests')
plt.ylabel('Total Time (s)')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(df['Requests'], df['REST Avg Time (ms)'], label='REST Avg Time (ms)', marker='o')
plt.plot(df['Requests'], df['gRPC Avg Time (ms)'], label='gRPC Avg Time (ms)', marker='o')
plt.title('Average Time Comparison')
plt.xlabel('Number of Requests')
plt.ylabel('Average Time (ms)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
