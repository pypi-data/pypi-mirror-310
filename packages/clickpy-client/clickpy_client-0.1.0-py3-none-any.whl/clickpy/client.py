import logging
import re
from contextlib import asynccontextmanager
from typing import Any

import httpx
from pydantic import BaseModel, TypeAdapter

from clickpy.queries.base import BaseClickPyQuery, TModel
from clickpy.queries.keywords_by_releases_query import KeywordsByReleasesQuery
from clickpy.queries.tables_query import TablesQuery
from clickpy.settings import CLICK_PY_DATA_BASE_SETTING

logger = logging.getLogger('clickpy')


class ClickHouseResponse(BaseModel):
    class ClickHouseStatisticsResponse(BaseModel):
        elapsed: float
        rows_read: int
        bytes_read: int

    meta: list[dict[str, str]]
    rows: int
    statistics: ClickHouseStatisticsResponse
    data: Any


class ClickPyClient(object):
    def __init__(self) -> None:
        self.http_client = httpx.AsyncClient()

    @asynccontextmanager
    async def lifespan(self, *args: Any, **kwargs: Any):
        yield
        await self.http_client.aclose()

    async def query(self, method: BaseClickPyQuery[TModel]) -> TModel:
        query = method.query()

        http_response = await self.http_client.post(
            CLICK_PY_DATA_BASE_SETTING.HOST,
            auth=(CLICK_PY_DATA_BASE_SETTING.USERNAME, CLICK_PY_DATA_BASE_SETTING.PASSWORD),
            headers={'Content-Type': 'application/json'},
            params={
                'default_format': 'JSON',
                'query': query,
            },
        )
        http_response.raise_for_status()

        response = ClickHouseResponse.model_validate_json(http_response.content)

        logger.info(
            'Query: "%s"; Elapsed: %s; Rows: %s; Rows_read: %s; Bytes_read: %s',
            re.sub(r'\s+', ' ', query).strip(),
            response.rows,
            response.statistics.elapsed,
            response.statistics.rows_read,
            response.statistics.bytes_read,
            extra={
                'query': query,
                'rows': response.rows,
                'elapsed': response.statistics.elapsed,
                'rows_read': response.statistics.rows_read,
                'bytes_read': response.statistics.bytes_read,
            },
        )

        return TypeAdapter(method.Model).validate_python(response.data)

    async def get_tables(self, *args: Any, **kwargs: Any) -> TablesQuery.Model:
        return await self.query(TablesQuery(*args, **kwargs))

    async def get_keywords_by_releases(self, *args: Any, **kwargs: Any) -> KeywordsByReleasesQuery.Model:
        return await self.query(KeywordsByReleasesQuery(*args, **kwargs))
