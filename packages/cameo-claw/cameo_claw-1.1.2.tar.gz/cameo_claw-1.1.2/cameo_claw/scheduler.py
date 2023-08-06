from pydantic import BaseModel
import uuid

from cameo_claw.cameo_claw_reuse import fastapi_app, split_list

app = fastapi_app()


class ItemTask(BaseModel):
    task_id: str = ''
    module_name: str = 'cameo_claw.remote'
    function_name: str = 'square'
    lst_iter: list = list(range(323))
    dic_param: dict = {}
    lst_result: list = []


lst_item_task_todo = []


@app.post("/api/add_task/")
async def add_task(i: ItemTask):
    i.task_id = uuid.uuid4()
    lst_chunk = split_list(i.lst_iter, 100)
    for lst_iter in lst_chunk:
        item_task = ItemTask()
        item_task.task_id = i.task_id
        item_task.module_name = i.module_name
        item_task.function_name = i.function_name
        item_task.lst_iter = lst_iter
        item_task.dic_param = i.dic_param
        lst_item_task_todo.append(item_task)
    return i


@app.get("/api/list_task/")
async def list_task():
    return lst_item_task_todo


@app.get("/api/get_task/")
async def get_task():
    try:
        return lst_item_task_todo.pop(0)
    except Exception as e:
        return None


dic_done_task = {}


@app.post("/api/done_task/")
async def done_task(i: ItemTask):
    dic_done_task.setdefault(i.task_id, [])
    dic_done_task[i.task_id].append(i)


@app.get("/api/get_done_task/")
async def get_done_task(task_id):
    return dic_done_task.get(task_id, None)


@app.get("/api/close_task/")
async def close_task(task_id):
    return dic_done_task.pop(task_id, None)
