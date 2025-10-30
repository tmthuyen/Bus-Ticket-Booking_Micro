# limiter.py (đơn giản, memory)
from collections import defaultdict
from time import time

hits = defaultdict(list)
WINDOW = 60   # 60s
LIMIT = 10    # 10 lần/phút/IP

def allow(ip: str) -> bool:
    now = time()
    q = hits[ip]
    while q and now - q[0] > WINDOW:
        q.pop(0)
    if len(q) >= LIMIT:
        return False
    q.append(now)
    return True
