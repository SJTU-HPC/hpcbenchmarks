import platform
import sys
from os.path import dirname, abspath, join
from environs import Env
from loguru import logger
import shutil

env = Env()
env.read_env()

# definition of flags
IS_WINDOWS = platform.system().lower() == 'windows'

# definition of dirs
ROOT_DIR = dirname(abspath(__file__))
LOG_DIR = join(ROOT_DIR, env.str('LOG_DIR', 'logs'))

# definition of environments
CLUSTER_SCALE = None
CLUSTER_NAME = env.str('CLUSTER_NAME')
APP_DEBUG = env.bool('APP_DEBUG', False)
APP_CONFIG = env.str('APP_CONFIG', None)

HPCbench_RESULT = env.str('HPCbench_RESULT',join(ROOT_DIR, 'result'))
HPCbench_BENCHMARK = env.str('HPCbench_BENCHMARK',join(ROOT_DIR, 'benchmark'))

GPU_PARTITION = env.str('GPU_PARTITION')
CPU_PARTITION = env.str('CPU_PARTITION')
CPU_MAX_CORES = env.str('CPU_MAX_CORES')
HADOOP_DATA = env.str('HADOOP_DATA')
CLUSTER_POWER = env.str('CLUSTER_POWER', 10000)
CLUSTER_BURSTBUFFER = env.str('CLUSTER_BURSTBUFFER', 10000)
# CLUSTER_MEMORY = env.int('CLUSTER_MEMORY', 10000)
BW_BURSTBUFFER = env.str('BW_BURSTBUFFER', 10000)
PARA_STORAGE_PATH = env.str('PARA_STORAGE_PATH')
TOTAL_NODES =  env.str('TOTAL_NODES')

ENABLE_LOG_FILE = env.bool('ENABLE_LOG_FILE', True)
ENABLE_LOG_RUNTIME_FILE = env.bool('ENABLE_LOG_RUNTIME_FILE', True)
ENABLE_LOG_ERROR_FILE = env.bool('ENABLE_LOG_ERROR_FILE', True)

LOG_LEVEL = "DEBUG" if APP_DEBUG else "INFO"
LOG_ROTATION = env.str('LOG_ROTATION', '100MB')
LOG_RETENTION = env.str('LOG_RETENTION', '1 week')

logger.remove()
logger.add(sys.stderr, level='INFO')

if ENABLE_LOG_FILE:
    if ENABLE_LOG_RUNTIME_FILE:
        logger.add(env.str('LOG_RUNTIME_FILE', join(LOG_DIR, 'runtime.log')),
                    level=LOG_LEVEL, rotation=LOG_ROTATION, retention=LOG_RETENTION)
    if ENABLE_LOG_ERROR_FILE:
        logger.add(env.str('LOG_ERROR_FILE', join(LOG_DIR, 'error.log')),
                    level='ERROR', rotation=LOG_ROTATION)
else:
    shutil.rmtree(LOG_DIR, ignore_errors=True)
