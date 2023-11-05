import threading
import asyncio, time
from async_handler import task_gather_runner, pending_tasks, completed_tasks

gather_thread = threading.Thread(target=asyncio.run, args=(task_gather_runner(),))
gather_thread.start()


while True:
    print("how are you")
    time.sleep(1)
    pending_tasks.append({"_id": "B01M2ZHQ1Y", "stage": 1})
    time.sleep(20)