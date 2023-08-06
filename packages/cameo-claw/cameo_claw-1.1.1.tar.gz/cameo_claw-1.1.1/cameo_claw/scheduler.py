import uvicorn
from pydantic import BaseModel
import uuid

from cameo_claw.cameo_claw_reuse import fastapi_app

app = fastapi_app()


class ItemScheduler(BaseModel):
    module: str
    function_name: str
    lst: list
    dic: dict


class ItemTask(BaseModel):
    task_id: str = ''
    module: str = ''
    function_name: str = ''
    lst: list = []
    dic: dict = {}
    result: dict = {}


@app.post("/api/scheduler/")
def scheduler(i: ItemScheduler):
    item_task = ItemTask()
    item_task.task_id = uuid.uuid4()
    item_task.module = i.module
    item_task.function_name = i.function_name
    item_task.lst = i.lst
    item_task.dic = i.dic
    return item_task


lst_task = []


# #todo
# @app.post("/api/task/")
# def task(i: ItemGetTask):
#     return lst_task.pop(0)


class ItemTaskDone(BaseModel):
    worker_name: str
    task_id: str
    task_result: dict


@app.post("/api/task_done/")
def task_done(i: ItemWorker):
    return lst_task.pop(0)
