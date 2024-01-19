from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.student.urls import student_urls
from apps.staff.urls import staff_urls
from apps.root.update_urls import root_urls_update
from apps.root.delete_urls import root_urls_delete
from apps.root.search_urls import root_urls_search
from apps.root.insert_urls import root_urls_insert
from apps.login.urls import login_urls
import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_urls, prefix='/student', tags=['api for student users'])
app.include_router(staff_urls, prefix='/staff', tags=['api for staff users'])
app.include_router(root_urls_search, prefix='/root', tags=['search api for root users'])
app.include_router(root_urls_update, prefix='/root', tags=['update api for root users'])
app.include_router(root_urls_delete, prefix='/root', tags=['delete api for root users'])
app.include_router(root_urls_insert, prefix='/root', tags=['insert api for root users'])
app.include_router(login_urls, prefix='/login', tags=['api for login'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
