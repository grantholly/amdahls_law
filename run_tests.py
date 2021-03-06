#!/usr/bin/env python3
import random
import datetime
import time
import os
import json
import sys

from counters import (Counter, 
                      UnsharedConcurrentCounter,
                      incr,
                      SharedConcurrentCounter)

OUTPUT_DIR = os.path.dirname(__file__) + "/output/"
TIME_FMT = "%Y-%m-%d-%H,%M,%S"
CONFIG = {
    "workload_size": 500,
    "job_ceiling": int(sys.argv[2]),
    "number_of_trials": 10,
    "concurrency": int(sys.argv[1]),
}

def counter_trial(counter_type, trials, workload, 
                  file_name, concurrency=0, **kwargs):
    date_stamp = datetime.datetime.now().strftime(TIME_FMT)
    results = []
    with open(OUTPUT_DIR +
              file_name +
              date_stamp, "a") as f:
        f.write(json.dumps(CONFIG) + "\n")
        for trial in range(trials):
            if concurrency != 0:
                c = counter_type(workload, concurrency)
            else:
                c = counter_type(workload)
            if kwargs:
                start = time.time()
                c.do_work(kwargs["func"])
            else:
                start = time.time()
                c.do_work()
            end = time.time()
            duration = end - start
            results.append(duration)
            # ugh, I should have thought of this ahead of time
            # instead of this ugly verbose hack
            if type(c) == UnsharedConcurrentCounter:
                f.write(str(len(workload)) + "," +
                        str(duration) + "\n")
            else:
                f.write(str(concurrency) + "," + 
                        str(duration) + "\n")

            
def main():
    size = CONFIG["workload_size"]
    work = [random.randint(0, CONFIG["job_ceiling"]) for n in range(size)]
    trials = CONFIG["number_of_trials"]

    counter_trial(Counter, trials, work, "plain_counter")
    counter_trial(UnsharedConcurrentCounter, trials, work, 
                  "mapped_counter", func=incr)
    counter_trial(SharedConcurrentCounter, trials, work,
                  "shared_counter", concurrency=CONFIG["concurrency"])


main()
