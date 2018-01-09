import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("no_processes", help="Number of separate processes to execute in parallel. Default 10.",
                    type=int, default=10)
args = parser.parse_args()

for i in range(args.no_processes):
    file_name = "execution_" + str(i) + ".txt"
    with open(file_name, "wb") as out:
        subprocess.Popen("python3 MyCube.py", stdout=out, stderr=None)
