from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from jinja2 import Template
from cameo_claw.cameo_claw_reuse import pd_read_csv, fastapi_app

app = fastapi_app()

t1 = Template('''
import polars as pl

lst_tasks={{lst_tasks}}
def add(a,b):
    df = pl.DataFrame(
      { "A": [1, 2, 3, 4, 5],
        "fruits": ["banana", "banana", "apple", "apple", "banana"],
        "B": [5, 4, 3, 2, 1],
        "cars": ["beetle", "audi", "beetle", "beetle", "beetle"],
      }
    )
    return a+b,df
    
print(f'add a b {add(3,4)}, {lst_tasks}')
''')
lst_tasks = list(range(0, 3100))


@app.get("/api/get_tasks/", response_class=PlainTextResponse)
def get_tasks(token):
    if not token == '123':
        return False
    global lst_tasks
    py = t1.render(lst_tasks=lst_tasks[0:10])
    lst_tasks = lst_tasks[10:]
    return py


def server(host='0.0.0.0', int_port=20419):
    uvicorn.run("fastapi_distributed:app", host=host, port=int_port, reload=True, debug=False, workers=1)


if __name__ == '__main__':
    server()
