"""
Make snapshot

{"Tasks": {"total": 440, "running": 1, "sleeping": 354, "stopped": 1, "zombie": 0},
"%CPU": {"user": 14.4, "system": 2.2, "idle": 82.7},
"KiB Mem": {"total": 16280636, "free": 335140, "used": 11621308},
"KiB Swap": {"total": 16280636, "free": 335140, "used": 11621308},
"Timestamp": 1624400255}
"""
import json
import os
import psutil
import time
import argparse
from psutil._common import bytes2human


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


class SystemMonitor:
    def __init__(self, interval, output_file):
        self.interval = interval
        self.output_file = output_file

    @staticmethod
    def get_system_snapshot():

        zombie = 0
        stopped = 0
        total = 0
        running = 0
        sleeping = 0
        for proc in psutil.process_iter():
            total += 1
            if proc.status() == psutil.STATUS_RUNNING:
                running += 1
            elif proc.status() == psutil.STATUS_SLEEPING:
                sleeping += 1
            elif proc.status() == psutil.STATUS_STOPPED:
                stopped += 1
            elif proc.status() == psutil.STATUS_ZOMBIE:
                zombie += 1

        snapshot = {
            "Tasks": {
                "total": total,
                "running": running,
                "sleeping": sleeping,
                "stopped": stopped,
                "zombie": zombie,
            },
            "%CPU": {
                "user": psutil.cpu_times_percent(interval=0.1).user,
                "system": psutil.cpu_times_percent(interval=0.1).system,
                "idle": psutil.cpu_times_percent(interval=0.1).idle,
            },
            "KiB Mem": {
                "total": psutil.virtual_memory().total // 1024,
                "free": psutil.virtual_memory().free // 1024,
                "used": psutil.virtual_memory().used // 1024,
            },
            "KiB Swap": {
                "total": psutil.swap_memory().total // 1024,
                "free": psutil.swap_memory().free // 1024,
                "used": psutil.swap_memory().used // 1024,
            },
            "Timestamp": int(time.time())
        }
        return snapshot

    def write_snapshot_to_file(self, snapshot):
        with open(self.output_file, "a") as file:
            json.dump(snapshot, file)
            file.write('\n')

    def run(self, num_snapshots):
        # Clear file content when the script is started
        open(self.output_file, 'w').close()

        for _ in range(num_snapshots):
            clear()  # for console output
            snapshot = self.get_system_snapshot()
            self.write_snapshot_to_file(snapshot)
            # print(snapshot, end="\r")
            print(snapshot, end="\r")
            time.sleep(self.interval)


def main():
    """Snapshot tool."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Interval between snapshots in seconds", type=int, default=5)
    parser.add_argument("-f", help="Output file name", default="snapshot.json")
    parser.add_argument("-n", help="Quantity of snapshot to output", default=20)
    args = parser.parse_args()
    monitor = SystemMonitor(args.i, args.f)
    monitor.run(args.n)


if __name__ == "__main__":
    main()

