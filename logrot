#!/usr/bin/env python3
import asyncio
from asyncio.subprocess import PIPE
import sys
import concurrent.futures

output = []

@asyncio.coroutine
def wait_heat_death(proc, loop):
    print("Wating for heat death of the universe")
    yield from proc.wait() # Asynchronously join with the process
    print("Process died, killing myself?")
    loop.stop() # Stop the async loop, successfully killing myself

@asyncio.coroutine
def reader(read, pfx):
    while True:
        try:
            line = yield from read.readline()
            output.append("%s %s" % (pfx, line))
        except Exception as e:
            print("Exception %s"%str(e))
            break

@asyncio.coroutine
def runner(*args, loop=None):
    """Function to run a subprocess and wait for input on a pipe"""
    global output
    proc = yield from asyncio.create_subprocess_exec(*args, stdout=PIPE, stderr=PIPE)
    print("Started process pid:%s"%proc.pid)
    if loop:
        asyncio.ensure_future(wait_heat_death(proc, loop))
    asyncio.ensure_future(reader(proc.stdout, "stdout>>"))
    asyncio.ensure_future(reader(proc.stderr, "stderr>>"))

@asyncio.coroutine
def main_loop():
    """Actually wait for output, print and truncate"""
    global output
    print("OK starting print loop")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        while True:
            yield from asyncio.sleep(0.5) # Sleep for 1 second
            to_print = list(output) # See what output we have now, and make a copy.
            executor.submit(printer, to_print) # Send printing (or boto copying to a thread on a threadpool)
            output.clear() # Clear the output array

# This is to emulate boto which is insane
def printer(array):
    print('\n'.join(map(str, array)))


try:
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(runner(*sys.argv[1:], loop=loop)) # Get the process bit running
    asyncio.ensure_future(main_loop())
    loop.run_forever()
finally:
    loop.close()
