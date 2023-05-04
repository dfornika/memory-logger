#!/usr/bin/env python3

import argparse
import csv
import json
import psutil
import datetime
import sys
import time


def main(args):
    output_fieldnames = [
        "timestamp",
        "process_name",
        "username",
        "timestamp_process_created",
        "cpu_percent",
        "mem_rss",
        "mem_vms",
        "mem_shared",
        "mem_text",
        "mem_lib",
        "mem_data",
        "mem_dirty",
    ]

    writer = csv.DictWriter(sys.stdout, fieldnames=output_fieldnames, dialect='unix', quoting=csv.QUOTE_MINIMAL)
    if args.csv and args.header:
        writer.writeheader()

    while True:
        for proc in psutil.process_iter():
            now = datetime.datetime.now().isoformat()
            process_name = proc.name()
            process_username = proc.username()
            process_cpu_percent = proc.cpu_percent()
            process_create_time = datetime.datetime.fromtimestamp(proc.create_time())
            process_memory_info = psutil.Process(proc.pid).memory_info()._asdict()
            output = {
                "timestamp": now,
                "process_name": process_name,
                "username": process_username,
                "timestamp_process_created": str(process_create_time),
                "cpu_percent": process_cpu_percent,
                "memory_info": process_memory_info,
            }

            if args.csv:
                for k, v in output['memory_info'].items():
                    output['mem_' + k] = v
                output.pop('memory_info')
                writer.writerow(output)
            else:
                print(json.dumps(output))
        time.sleep(args.interval)


        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', type=int, default=10, help="Pause interval (seconds) between process scans. (Default: 60)")
    parser.add_argument('--csv', action='store_true', help="Output in csv")
    parser.add_argument('--header', action='store_true', help="Print header (for csv mode)")
    args = parser.parse_args()
    main(args)
