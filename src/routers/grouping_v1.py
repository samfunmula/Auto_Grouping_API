from fastapi import APIRouter
from toolkit.lib import *
from toolkit.method  import generate_query_string, BRAND_DB_MANAGER

TAG_MODEL_VERSION = 'v1'
router = APIRouter(prefix='/v1/grouping', tags=[TAG_MODEL_VERSION])

@router.on_event("shutdown")
def shutdown_event():
    print('[斷開資料庫]')
    BRAND_DB_MANAGER.close_connection()

@router.post('/autogrouping/', responses={
        200: {'model': QueryStringResponse},
        400: {'model': HTTPErrorResult},
        500: {'model': HTTPErrorResult},
    },
)
@catch_error
async def get_query_string(request: dict):
    queryStringResponse, query_info = generate_query_string(request)
    print(queryStringResponse)
    return queryStringResponse

# for testing
@router.post('/test_autogrouping/', responses={
        200: {'model': dict},
        400: {'model': HTTPErrorResult},
        500: {'model': HTTPErrorResult},
    },
)
@catch_error
async def get_query_string(request: dict):
    queryStringResponse, query_info = generate_query_string(request)
    return query_info
