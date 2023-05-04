#!/usr/bin/env python3

import argparse
import json
import psutil
import datetime
import sys
import time


def main(args):
    
    while True:
        for proc in psutil.process_iter():
            now = datetime.datetime.now().isoformat()
            process_name = proc.name()
            process_username = proc.username()
            process_cpu_percent = proc.cpu_percent()
            process_create_time = datetime.datetime.fromtimestamp(proc.create_time())
            process_memory_info = psutil.Process(proc.pid).memory_info()._asdict()
            print(json.dumps({
                "timestamp": now,
                "process_name": process_name,
                "username": process_username,
                "timestamp_process_created": str(process_create_time),
                "cpu_percent": process_cpu_percent,
                "memory_info": process_memory_info,
            }))
        time.sleep(args.interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', type=int, default=10)
    args = parser.parse_args()
    main(args)
