import re
import sys
from utils.tool import Tool
from pprint import pprint

tool = Tool()

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
    def walk(self):
        for key, value in self.items():
            if isinstance(value, Vividict):
                for tup in value.walk():
                    yield (key,) + tup
            else:
                yield key, value

def extract_pflops(file):
    content = tool.read_lines(file)
    content = content[::-1]
    pflops_value = 0
    for i in range(len(content)):
        if "Time" in content[i]:
            match = re.search(r"\d+\.\d+e[+-]\d+", content[i-2])
            if match:
                gflops_scientific = match.group(0)
                pflops_value = float(gflops_scientific)/1e6
                break
    return pflops_value

def extract_number(pattern, file):
    content = tool.read_file(file)
    match = re.search(pattern, content)
    if match:
        number = match.group(1)
        return float(number)
    else:
        return 0

def extract_number_multline(pattern, file):
    content = tool.read_file(file)
    match = re.search(pattern, content, re.MULTILINE)
    if match:
        number = match.group(1)
        return float(number)
    else:
        return 0
    
def extract_after_get_operation(file):
    number = 0
    content = tool.read_lines(file)
    for i in range(len(content)):
        if "Operation: GET. Concurrency: 256" in content[i]:
            number = re.findall(r'\d+\.\d+', content[i+1])[0]
    return float(number)

def get_result():
    result = Vividict()
    ## compute/HPL
    file = "result/compute/hpl.txt"
    result['compute']['HPL'] = extract_pflops(file)
    ## compute/HPCG
    file = "result/compute/hpcg.txt"
    pattern = r"Final Summary::HPCG result is VALID with a GFLOP/s rating of=(\d+\.\d+)"
    result['compute']['HPCG'] = extract_number(pattern, file)/1e6
    ## AI/infering
    file = "result/AI/resnet.txt"
    pattern = r"TestScenario\.Offline qps.*?time=(\d+\.\d+)"
    result['AI']['infering'] = 50000/extract_number(pattern, file)
    ## AI/training
    file = "result/AI/maskrcnn.txt"
    pattern = r"train_perf_fps : (\d+\.\d+)"
    result['AI']['training'] = extract_number(pattern, file)
    ## storage/single_client_single_fluence
    file = "result/storage/ior/single_client_single_fluence.txt"
    pattern = r"Max Write: \d+\.\d+ MiB/sec \((\d+\.\d+) MB/sec\)"
    result['storage']['single_client_single_fluence'] = extract_number(pattern, file)/1024
    ## storage/single_client_multi_fluence
    file = "result/storage/ior/single_client_multi_fluence.txt"
    pattern = r"Max Write: \d+\.\d+ MiB/sec \((\d+\.\d+) MB/sec\)"
    result['storage']['single_client_multi_fluence'] = extract_number(pattern, file)/1024
    ## storage/aggregation_bandwidth
    file = "result/storage/ior/aggregation_bandwidth.txt"
    pattern = r"Max Write: \d+\.\d+ MiB/sec \((\d+\.\d+) MB/sec\)"
    result['storage']['aggregation_bandwidth'] = extract_number(pattern,file)/1024
    ## storage/multi_request
    file = "result/storage/protocol/posix_test/posix.txt"
    pattern = r"Max Read:.*?(\d+\.\d+).*?MB/sec"
    posix = extract_number(pattern, file)
    file = "result/storage/protocol/nfs/nfs.txt"
    pattern = r"Max Read:.*?(\d+\.\d+).*?MB/sec"
    nfs = extract_number(pattern, file)
    file = "result/storage/protocol/mino/s3_read.log"
    s3 = extract_after_get_operation(file)
    file = "result/storage/protocol/hadoop/hdfs_read.log"
    pattern = r'Throughput mb/sec: +(\d+\.\d+)'
    hdfs = extract_number(pattern, file)
    result['storage']['multi_request']  = ((nfs/posix) + (s3/posix) + (hdfs/posix)) / 3
    ## storage/IO_rate
    file = "result/storage/ior/iops.txt"
    pattern = r"^write\s+\d+\s+(\d+)"
    result['storage']['IO_rate']  = extract_number_multline(pattern, file)
    ## network/P2P_network_bandwidth
    file = "result/network/osu_bibw.log"
    pattern = r'4194304\s+(\d+\.\d+)'
    result['network']['P2P_network_bandwidth'] = extract_number(pattern, file)/1024*8
    ## network/P2P_message_latency
    file = "result/network/osu_latency.log"
    pattern = r'8\s+(\d+\.\d+)'
    result['network']['P2P_message_latency'] = '1/' + str(extract_number(pattern, file))
    ## network/ratio
    result['network']['ratio'] = 0.5
    ## system/compute_efficiency
    file = "result/system/system.log"
    pattern = r'COMPUTE_EFFIENCY=(\d+\.\d+)'
    result['system']['compute_efficiency'] = extract_number(pattern, file)
    ## system/IO_operation_rate
    pattern = r'IO_operation_rate=(\d+\.\d+)'
    result['system']['IO_operation_rate'] = extract_number(pattern,file)
    ## balance
    file = "result/balance/balance.log"
    pattern = r"\w+=([\d.]+)"
    matches = list(map(float, re.findall(pattern, tool.read_file(file))))
    result['balance']['mem2cpu'] = matches[0]
    result['balance']['buffer2mem'] = matches[1]
    result['balance']['file2buffer'] = matches[2]
    result['balance']['mem2buffer'] = matches[3]
    result['balance']['buffer2file'] = matches[4]
    return result