import asyncio
import tailf
import time
from datetime import datetime

async def tailer():
    with tailf.Tail("test.txt") as tail:
        while True:
            event = await tail.wait_event()
            if isinstance(event, bytes):
                newtext = event.decode("utf-8")
                print(newtext, end='')
                if newtext == "secret":
                    return 0
            elif event is tailf.Truncated:
                print("File was truncated")
            else:
                assert False, "unreachable" # currently. more events may be introduced later

async def clock():
    flag=0
    while True:
        if flag == 0:
            print(str(datetime.now().timestamp())[8:13]+" tak!")
            await asyncio.sleep(1)
            flag = 1
        if flag == 1:
            print(str(datetime.now().timestamp())[8:13]+" tik!")
            await asyncio.sleep(1)
            flag = 0

async def clocke():
    flag=0
    await asyncio.sleep(0.5)
    while True:
        if flag == 0:
            print(str(datetime.now().timestamp())[8:13]+" tek!")
            await asyncio.sleep(1)
            flag = 1
        if flag == 1:
            print(str(datetime.now().timestamp())[8:13]+" tok!")
            await asyncio.sleep(1)
            flag = 0

#asyncio.run(main())
async def main():
    tasktailer = asyncio.create_task(tailer())
    taskclock = asyncio.create_task(clock())
    taskclocke = asyncio.create_task(clocke())
    #await asyncio.gather(taskclock,taskclocke)
    await tasktailer
    await taskclock
    #await asyncio.sleep(0.5)
    #time.sleep(0.5)
    await taskclocke


if __name__ == "__main__":
    asyncio.run(main())