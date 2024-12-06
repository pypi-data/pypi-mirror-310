import os
import aiohttp
from typing import Optional
import os
import aiohttp
import backoff
from dhisana.utils.cache_output import cache_output,retrieve_output
from dhisana.utils.assistant_tool_tag import assistant_tool
from typing import Optional

@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=2,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def get_company_info_from_builtwith(
    company_domain: Optional[str] = None,
):
    """
    Fetch a company's technology details from BuiltWith using the company domain.
    
    Parameters:
    - **company_domain** (*str*, optional): Domain of the company.

    Returns:
    - **dict**: JSON response containing technology information.
    """
    BUILTWITH_API_KEY = os.environ.get('BUILTWITH_API_KEY')
    if not BUILTWITH_API_KEY:
        return {'error': "BuiltWith API key not found in environment variables"}

    if not company_domain:
        return {'error': "Company domain must be provided"}

    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "accept": "application/json"
    }

    cached_response = retrieve_output("get_company_info_from_builtwith", company_domain)  # Replace with your caching logic if needed
    if cached_response:
        return cached_response

    url = f'https://api.builtwith.com/v19/api.json?KEY={BUILTWITH_API_KEY}&LOOKUP={company_domain}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                cache_output("get_company_info_from_builtwith", company_domain, result)  # Replace with your caching logic if needed
                return result
            elif response.status == 429:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Rate limit exceeded",
                    headers=response.headers
                )
            else:
                try:
                    result = await response.json()
                    return {'error': result}
                except Exception as e:
                    return {'error': f"Unexpected error: {str(e)}"}

@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=2,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def get_company_financials_from_builtwith(
    company_domain: Optional[str] = None,
):
    """
    Fetch a company's financial details from BuiltWith using the company domain.
    
    Parameters:
    - **company_domain** (*str*, optional): Domain of the company.

    Returns:
    - **dict**: JSON response containing financial information.
    """
    BUILTWITH_API_KEY = os.environ.get('BUILTWITH_API_KEY')
    if not BUILTWITH_API_KEY:
        return {'error': "BuiltWith API key not found in environment variables"}

    if not company_domain:
        return {'error': "Company domain must be provided"}

    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "accept": "application/json"
    }

    cached_response = retrieve_output("get_company_financials_from_builtwith", company_domain)  # Replace with your caching logic if needed
    if cached_response:
        return cached_response

    url = f'https://api.builtwith.com/v19/financial.json?KEY={BUILTWITH_API_KEY}&LOOKUP={company_domain}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                cache_output("get_company_financials_from_builtwith", company_domain, result)  # Replace with your caching logic if needed
                return result
            elif response.status == 429:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Rate limit exceeded",
                    headers=response.headers
                )
            else:
                try:
                    result = await response.json()
                    return {'error': result}
                except Exception as e:
                    return {'error': f"Unexpected error: {str(e)}"}
