from .simulator import Simulation

from subprocess import Popen, PIPE
import sys
import os
import time
import datetime

import argparse

from jelka_validator import DataReader

parser = argparse.ArgumentParser(description="Run jelka simulation.")

parser.add_argument("runner", type=str, nargs="?", help="How to run your program.")
parser.add_argument("target", type=str, help="Your program name.")


def main(header_wait: float = 0.5):
    print(f"You are executing jelkasim from '{os.getcwd()}' using python '{sys.executable}'")
    args = parser.parse_args()

    cmd = []
    if args.runner:
        if not args.target:
            # TODO: UI
            raise ValueError("You must provide a target program.")
    if args.target:
        if args.runner:
            cmd = [args.runner, args.target]
        elif args.target.endswith(".py"):
            cmd = [sys.executable, args.target]
        else:
            cmd = [args.target]
    if cmd == []:
        raise ValueError("You must provide a target program. (Wait for the next update.)")
    
    print(f"Running: {cmd} at {datetime.datetime.now()}")

    with Popen(cmd, stdout=PIPE) as p:
        sim = Simulation()
        dr = DataReader(p.stdout.read1)  # type: ignore
        dr.update()

        t_start = time.time()
        while time.time() - t_start < header_wait and dr.header is None:
            dr.update()
            time.sleep(0.01)
        
        if dr.header is None:
            raise ValueError(f"No header found in the first {header_wait} seconds. Is your program running?")

        sim.init()
        while sim.running:
            c = next(dr)
            dr.user_print()
            sim.set_colors(dict(zip(range(len(c)), c)))
            sim.frame()
        sim.quit()
    
    print(f"Finished running at {datetime.datetime.now()} (took {time.time() - t_start:.2f} seconds).")