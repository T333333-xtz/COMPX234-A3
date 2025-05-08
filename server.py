#server.py
import socket
import threading
import time
from collections import defaultdict

# 元组空间
tuple_space = {}
# 操作计数器
operation_count = defaultdict(int)
# 错误计数器
error_count = 0
# 客户端连接计数器
client_count = 0
