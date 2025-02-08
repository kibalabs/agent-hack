import json
from typing import Any

from core import logging
from core.requester import Requester
from core.util import file_util


async def load_or_query(
    requester: Requester,
    source: str,
    entityName: str,
    url: str,
    dataDict: dict[str, Any],
    cacheEntityName: str | None = None,
    hasInlinedItems: bool = False,
    expirySeconds: int = 3600,  # Default 1 hour
) -> dict[str, Any]:
    if cacheEntityName is None:
        cacheEntityName = entityName
    cacheFilePath = f'./data/{source}-{cacheEntityName}.json'
    fileExists = await file_util.file_exists(filePath=cacheFilePath)
    fileAgeMillis = await file_util.get_file_age_millis(filePath=cacheFilePath) if fileExists else 0
    if fileExists and (fileAgeMillis / 1000) < expirySeconds:
        logging.info(f'loading {cacheEntityName}...')
        items = json.loads(await file_util.read_file(filePath=cacheFilePath))
    else:
        logging.info(f'querying {cacheEntityName}...')
        items = []
        while True:
            dataDict['variables']['skip'] = len(items)
            response = await requester.post_json(url=url, dataDict=dataDict)
            data = response.json()
            if hasInlinedItems:
                items += data['data'][entityName]
                pageInfo = None
            else:
                items += data['data'][entityName]['items']
                pageInfo = data['data'][entityName].get('pageInfo')
            if pageInfo is None:
                break
            if pageInfo['count'] < pageInfo['limit']:
                break
        if len(items) > 0:
            await file_util.write_file(filePath=cacheFilePath, content=json.dumps(items, indent=2))
    return items
