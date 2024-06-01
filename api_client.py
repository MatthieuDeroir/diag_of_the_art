import httpx
import asyncio
import json
import os 
from dotenv import load_dotenv

load_dotenv()
# import logging

# logging.basicConfig(level=logging.DEBUG)

async def get_response_from_mistral_stream(api_key, api_url, messages, prompt, preprompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mistral-large-2402",  # Replace with the correct model name for Mistral
        "messages": messages + [{"role": "user", "content": prompt}]
    }

    if preprompt:
        payload["messages"].append({"role": "system", "content": preprompt})

    timeout = httpx.Timeout(10.0, read=30.0)  # Increase the read timeout to 30 seconds

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream("POST", api_url, headers=headers, json=payload) as response:
                buffer = ""
                async for chunk in response.aiter_text():
                    buffer += chunk
                    try:
                        # Attempt to parse the buffered content
                        data = json.loads(buffer)
                        yield data
                        buffer = ""
                    except json.JSONDecodeError:
                        # Incomplete JSON data, continue accumulating
                        continue
    except httpx.RequestError as exc:
        # logging.error(f"An error occurred while requesting {exc.request.url!r}.")
        # logging.error(exc)
        raise
    # except httpx.RequestError as exc:
    #     logging.error(f"An error occurred while requesting {exc.request.url!r}.")
    #     logging.error(exc)
    #     raise
    # except httpx.HTTPStatusError as exc:
    #     logging.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
    #     logging.error(exc)
    #     raise
    # except httpx.TimeoutException as exc:
    #     logging.error(f"Request timed out while requesting {exc.request.url!r}.")
    #     logging.error(exc)
    #     raise
