#!/usr/bin/env python3
import asyncio
from asyncio.subprocess import PIPE
import sys
import concurrent.futures

output = []

@asyncio.coroutine
def runner(*args):
    """Function to run a subprocess and wait for input on a pipe"""
    global output
    proc = yield from asyncio.create_subprocess_exec(*args, stdout=PIPE)
    print("Started process pid:%s"%proc.pid)
    while True:
        try:
            # Wait to read a line from the process
            line = yield from proc.stdout.readline()
            if not line: # Empty lines usually because process is dead
                break
            # Add line to output
            output.append(line)
        except Exception as e:
            print("Exception")
            print(e)
            break

@asyncio.coroutine
def main_loop():
    """Actually wait for output, print and truncate"""
    global output
    print("OK starting print loop")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        while True:
            yield from asyncio.sleep(1) # Sleep for 1 second
            to_print = list(output) # See what output we have now, and make a copy.
            executor.submit(printer, to_print) # Send printing (or boto copying to a thread on a threadpool)
            output.clear() # Clear the output array

# This is to emulate boto which is insane
def printer(array):
    print('\n'.join(map(str, array)))


try:
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(runner(*sys.argv[1:])) # Get the process bit running
    asyncio.ensure_future(main_loop())
    loop.run_forever()
finally:
    loop.close()
