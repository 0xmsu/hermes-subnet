from typing import Any, Dict
import aiohttp
import asyncio

async def request_subquery(options: Dict[str, Any]):
    async with aiohttp.ClientSession() as session:
        payload = {
            "variables": options.get("variables", {}),
             "query": options["query"]
        }
        url = options.get("url") or "https://index-api.onfinality.io/sq/subquery/subquery-mainnet"
        timeout = options.get("timeout", 30)
        method = options.get("method", "POST").upper()

        async with session.request(
            method,
            url,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as resp:
            result = await resp.json()
            res = result.get("data", {}).get(options["type"])
        return res

if __name__ == "__main__":

    query = '''
    query (
      $id: String!
    ) {
      indexerReward(
        id: $id
      ) {
        id
        amount
      }
    }
    '''
    r = asyncio.run(request_subquery({
        "query": query,
        "type": "indexerReward",
        "variables": {
            "id": "0x92E4888B6789EB52Da0BebDD82AfE660bf3E8d8f:0x30"
        },
    }))
    print(r)
