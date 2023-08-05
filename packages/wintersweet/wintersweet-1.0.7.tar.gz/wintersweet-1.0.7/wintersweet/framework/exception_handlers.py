from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from wintersweet.framework.response import Response, HTTP400Response, HTTP500Response
from wintersweet.utils.base import Utils


async def http_exception_handler(
        request: Request, exc: HTTPException
) -> Response:

    headers = getattr(exc, r'headers', None)

    Utils.log.error(exc.detail)

    if headers:
        return HTTP500Response(headers=headers)
    else:
        return HTTP500Response()


async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> Response:
    Utils.log.error(f'{exc.body} --> {[err.get("loc") for err in exc.errors()]}')

    return HTTP400Response(content=jsonable_encoder(exc.errors()))
