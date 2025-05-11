import time
from unittest import result
from fastapi import FastAPI
import asyncio

app = FastAPI()
result_dict = {}
# result_queue = asyncio.Queue()


# async def background_task(item_id, future):
#     print("start task...")
#     await asyncio.sleep(1)  # 模拟后台任务的处理
#     result = item_id + 10  # 任务计算结果
#     future.set_result(result)  # 设置任务的结果
#     print("end task...")  

async def fetch():
    print("start fetch")
    # await asyncio.sleep(1)  # 模拟异步 I/O
    print("end fetch")

async def background_task(item_id, event, stop_event):
    while not stop_event.is_set():
        print("start task...")
        await asyncio.sleep(1)  # 模拟后台任务的处理
        result = item_id + 10  # 任务计算结果
        result_dict[item_id] = result  # 存储结果（这里可以是数据库或缓存）
        event.set()
        stop_event.set()
        print("end task...")
    print(f"end background_task ...")

    
def callback(future):
    print(f"Task finished with result: {future.result()}")

# Simulate a delay with async function
@app.get("/process/{item_id}")
async def process_item(item_id: int):
    # 创建一个Future对象来存储结果
    # future = asyncio.get_event_loop().create_future()
    # future.add_done_callback(callback)
    # 启动后台任务，传入 future 对象
    # asyncio.create_task(background_task(item_id, future))

    event = asyncio.Event()  # 创建 Event 对象
    stop_event = asyncio.Event()
    asyncio.create_task(background_task(item_id, event, stop_event))
    await asyncio.sleep(2)  # Simulate a 2-second delay

    # if future.done():
        # result = await future
    
    await event.wait()  # 直到后台任务完成，event.set() 被触发
    result = result_dict.get(item_id, "Unknown result")
    print(f"Background task result: {result}")

    await fetch()
    return {"message": f"Processed item {item_id}, result: {result}"}

