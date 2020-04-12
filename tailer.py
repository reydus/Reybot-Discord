import asyncio
import tailf
import time
async def main():
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
            print("tik!")
            time.sleep(1)
            flag = 1
        if flag == 1:
            print("tok!")
            time.sleep(1)
            flag = 0

async def clocke():
    flag=0
    while True:
        if flag == 0:
            print("tek!")
            time.sleep(1)
            flag = 1
        if flag == 1:
            print("tik!")
            time.sleep(1)
            flag = 0

#asyncio.run(main())
async def runner():
    taskee = asyncio.create_task(main())
    taskclock = asyncio.create_task(clock())
    taskclocke = asyncio.create_task(clocke())
    await taskee
    await taskclock
    await taskclocke


if __name__ == "__main__":
    asyncio.run(runner())