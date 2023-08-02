from __future__ import annotations
import logging
from dataclasses import dataclass
from pydantic import BaseModel
from functools import wraps
from typing import Any, Callable, Coroutine, ParamSpec
from fastapi.responses import JSONResponse

class QueryStringResponse(BaseModel):
    query_string: str
    price_range: dict | None

class HTTPErrorResult(BaseModel):
    result: str

BAD_KEYWORD_LIST = ['愛買']

BRAND_ALIASES = [
    ['HP', '惠普'],
    ['Dell', '戴爾'],
    ['Lenovo', '聯想', '聯想集團'],
    ['Acer', '宏碁'],
    ['Microsoft', '微軟'],
    ['LG', '樂金'],
    ['Toshiba', '東芝'],
    ['Panasonic', '松下'],
    ['Nikon', '尼康'],
    ['Canon', '佳能'],
    ['POCO', '小米POCO'],
    ['OPPO', '歐珀'],
    ['Samsung', '三星'],
    ['ASUS', '華碩'],
    ['Sony', '索尼'],
    ['Apple', '蘋果'],
    ['Motorola', '摩托羅拉'],
    ['Xiaomi', '小米'],
    ['OnePlus', '一加'],
    ['HTC', '宏達電'],
    ['Google', '谷歌'],
    ['Amazon', '亞馬遜'],
    ['GoPro'],
]

@dataclass
class Errors:
    UNSUPPORTED_REQUEST_FORMAT = JSONResponse({'result':'UNSUPPORTED_REQUEST_FORMAT'}, 400)
    GENERATE_QUERY_STRING_ERROR = JSONResponse({'result':'GENERATE_QUERY_STRING_ERROR'}, 400)
    INTERNAL_ERROR = JSONResponse({'result':'INTERNAL_ERROR'}, 500)

logger = logging.getLogger('uvicorn.error')
P = ParamSpec('P')

def catch_error(func: Callable[P, Coroutine[Any, Any, Any]]) -> Callable[P, Coroutine[Any, Any, Any]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as ex:
            logger.error(str(ex), exc_info=True, stack_info=True)
            return Errors.INTERNAL_ERROR

    return wrapper