from fastapi import FastAPI


app = FastAPI()


tasks = [
    {
        "id": 1,
        "title": "Написать код для такст-трекера",
        "status": "в работе"
    },
    {
        "id": 2,
        "title": "Протестировать API",
        "status": "не начато"
    }
]

@app.get('/tasks')
def get_tasks():
    return tasks
