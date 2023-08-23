#!/usr/bin/env python
import re

def extract_GFLOPS(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    gflops_value = 0
    for i in range(len(lines)):
        if "Time" in lines[i]:
            match = re.search(r"\d+\.\d+e[+-]\d+", lines[i+2])
            if match:
                gflops_scientific = match.group(0)
                gflops_value = float(gflops_scientific)
                break
    return gflops_value

def extract_number(pattern,file):
    with open(file, 'r') as f:
        text = f.read()
        match = re.search(pattern, text)
    if match:
        extracted_number = match.group(1)
        return extracted_number
    else:
        return None

def extract_number_mutiline(pattern,file):
    with open(file, 'r') as f:
        text = f.read()
        match = re.search(pattern, text,re.MULTILINE)
    if match:
        extracted_number = match.group(1)
        return extracted_number
    else:
        return None
    
def find_number_after_get_operation(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        if "Operation: GET. Concurrency: 256" in lines[i]:
            next_line = lines[i+1]
            numbers = re.findall(r'\b\d+\.\d+\b', next_line)
            if numbers:
                return numbers[0]

    return None

def write_line(file, content):
    with open(file, 'a') as f:
        f.write(content + '\n')

output_file = "results.txt"

#COMPUTE
write_line(output_file, 'COMPUTE:')
# HPL
file_name = "result/compute/hpl.txt"
extracted_values = extract_GFLOPS(file_name)
write_line(output_file, f'HPL={extracted_values}')


# HPCG
file_name = "result/compute/hpcg.txt"
pattern = r"Final Summary::HPCG result is VALID with a GFLOP/s rating of=(\d+\.\d+)"
extracted_number = extract_number(pattern,file_name)
if extracted_number is not None:
    write_line(output_file, f'HPCG={extracted_number}')
else:
     print("未找到匹配的数字")
# AI
write_line(output_file, 'AI:')
# RESNET
file_name = "result/AI/resnet.txt"
pattern =   r"TestScenario\.Offline qps.*?time=(\d+\.\d+)"
resnet = extract_number(pattern,file_name)
resnet = 5000/float(resnet)
write_line(output_file, f'resnet={resnet}')

# MASKRCNN
file_name = "result/AI/maskrcnn.txt"
pattern = r"train_perf_fps : (\d+\.\d+)"
maskrcnn = extract_number(pattern,file_name)
write_line(output_file, f'maskrcnn={maskrcnn}')


# STORAGE
write_line(output_file, 'storage:')

file_name = "result/storage/ior/single_client_single_fluence.txt"
pattern = r"Max Write: \d+\.\d+ MiB/sec \((\d+\.\d+) MB/sec\)"
extracted_number = extract_number(pattern,file_name)
with open(output_file, 'a') as f:
        f.write('single_client_single_fluence' +'='+str(extracted_number) + '\n')

file_name = "result/storage/ior/single_client_multi_fluence.txt"
pattern = r"Max Write: \d+\.\d+ MiB/sec \((\d+\.\d+) MB/sec\)"
extracted_number = extract_number(pattern,file_name)
with open(output_file, 'a') as f:
        f.write('single_client_multi_fluence' +'='+str(extracted_number) + '\n')

file_name = "result/storage/ior/aggregation_bandwidth.txt"
pattern = r"Max Write: \d+\.\d+ MiB/sec \((\d+\.\d+) MB/sec\)"
extracted_number = extract_number(pattern,file_name)
with open(output_file, 'a') as f:
        f.write('aggregation_bandwidth' +'='+str(extracted_number) + '\n')

file_name = "result/storage/ior/iops.txt"
pattern = r"^write\s+\d+\s+(\d+)"
extracted_number = extract_number_mutiline(pattern,file_name)
with open(output_file, 'a') as f:
        f.write('iops' +'='+str(extracted_number) + '\n')

file_name = "result/storage/protocol/posix_test/posix.txt"
pattern = r"Max Read:.*?(\d+\.\d+).*?MB/sec"
posix = extract_number(pattern,file_name)


file_name = "result/storage/protocol/nfs/nfs.txt"
pattern = r"Max Read:.*?(\d+\.\d+).*?MB/sec"
nfs = extract_number(pattern,file_name)


file_name = "result/storage/protocol/mino/s3_read.log"
s3 = find_number_after_get_operation(file_name)

file_name = "result/storage/protocol/hadoop/hdfs_read.log"
pattern = r'Throughput mb/sec: +(\d+\.\d+)'
hdfs = extract_number(pattern,file_name)
posix = float(posix) if posix is not None else 0.0
nfs = float(nfs) if nfs is not None else 0.0
s3 = float(s3) if s3 is not None else 0.0
hdfs = float(hdfs) if hdfs is not None else 0.0

average = ((nfs/posix) + (s3/posix) + (hdfs/posix)) / 3 * 100
write_line(output_file, f'multi_request={average}')



#network
write_line(output_file, 'network:')
file_name = "result/network/osu_bibw.log"
pattern = r'4194304\s+(\d+\.\d+)'
P2P_network_bandwidth = extract_number(pattern,file_name)
write_line(output_file, f'P2P_network_bandwidth={P2P_network_bandwidth}')

file_name = "result/network/osu_latency.log"
pattern = r'8\s+(\d+\.\d+)'
P2P_message_latency = extract_number(pattern,file_name)
write_line(output_file, f'P2P_message_latency={P2P_message_latency}')

network_type = "Fat-Tree"
if network_type == "Fat-Tree":
     ratio = 0.5
write_line(output_file, f'ratio={ratio}')



#system
write_line(output_file, 'system:')
file_name = "result/system/system.log"
pattern = r'COMPUTE_EFFIENCY=(\d+\.\d+)'
compute_efficiency = extract_number(pattern,file_name)
write_line(output_file, f'compute_efficiency={compute_efficiency}')

pattern = r'IO_operation_rate=(\d+\.\d+)'
IO_operation_rate = extract_number(pattern,file_name)
write_line(output_file, f'IO_operation_rate={IO_operation_rate}')

#balance
write_line(output_file, 'balance:')
pattern = r"\w+=([\d.]+)"
file_name = "result/balance/balance.log"
with open(file_name, 'r') as f:
        text = f.read()
matches = re.findall(pattern, text)
write_line(output_file, f'mem2cpu={matches[0]}')
write_line(output_file, f'buffer2mem={matches[1]}')
write_line(output_file, f'file2buffer={matches[2]}')
write_line(output_file, f'mem2buffer={matches[3]}')
write_line(output_file, f'buffer2file={matches[4]}')
