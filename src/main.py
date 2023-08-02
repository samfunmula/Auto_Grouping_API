from fastapi import FastAPI
from routers.grouping_v1 import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='biggoapi-auto-grouping')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router, prefix='/api')