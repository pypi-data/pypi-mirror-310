import asyncio
import hashlib
import json
import logging
import os
import aiohttp
import backoff
from typing import List, Optional
from datetime import datetime, timedelta
from dhisana.utils.cache_output import cache_output,retrieve_output
from dhisana.utils.assistant_tool_tag import assistant_tool

# Assuming cache_output and retrieve_output are defined elsewhere in the file
# from .cache_utils import cache_output, retrieve_output

@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=2,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def enrich_person_info_from_apollo(
    linkedin_url: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
):
    """
    Fetch a person's details from Apollo using LinkedIn URL, email, or phone number.
    
    Parameters:
    - **linkedin_url** (*str*, optional): LinkedIn profile URL of the person.
    - **email** (*str*, optional): Email address of the person.
    - **phone** (*str*, optional): Phone number of the person.

    Returns:
    - **dict**: JSON response containing person information.
    """
    APOLLO_API_KEY = os.environ.get('APOLLO_API_KEY')
    if not APOLLO_API_KEY:
        return {'error': "Apollo API key not found in environment variables"}

    if not linkedin_url and not email and not phone:
        return {'error': "At least one of linkedin_url, email, or phone must be provided"}

    headers = {
        "X-Api-Key": f"{APOLLO_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {}
    if linkedin_url:
        data['linkedin_url'] = linkedin_url
        cached_response = retrieve_output("enrich_person_info_from_apollo", linkedin_url)
        if cached_response:
            return cached_response
    if email:
        data['email'] = email
    if phone:
        data['phone_numbers'] = [phone]  # Apollo expects a list for phone numbers

    url = 'https://api.apollo.io/v1/people/match'

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                if linkedin_url:
                    cache_output("enrich_person_info_from_apollo", linkedin_url, result)
                return result
            elif response.status == 429:
                logging.warning("enrich_person_info_from_apollo Rate limit hit")
                await asyncio.sleep(30)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Rate limit exceeded",
                    headers=response.headers
                )
            else:
                result = await response.json()
                logging.warning(f"enrich_person_info_from_apollo Failed to run assistant: ${result}")
                return {'error': result}


@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=2,
    giveup=lambda e: e.status != 429,
    factor=30,
)
async def enrich_company_info_from_apollo(
    company_domain: Optional[str] = None,
):
    """
    Fetch a company's details from Apollo using the company domain.
    
    Parameters:
    - **company_domain** (*str*, optional): Domain of the company.

    Returns:
    - **dict**: JSON response containing company information.
    """
    APOLLO_API_KEY = os.environ.get('APOLLO_API_KEY')
    if not APOLLO_API_KEY:
        return {'error': "Apollo API key not found in environment variables"}

    if not company_domain:
        return {'error': "Company domain must be provided"}

    headers = {
        "X-Api-Key": f"{APOLLO_API_KEY}",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "accept": "application/json"
    }

    cached_response = retrieve_output("enrich_company_info_from_apollo", company_domain)
    if cached_response:
        return cached_response

    url = f'https://api.apollo.io/api/v1/organizations/enrich?domain={company_domain}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                cache_output("enrich_company_info_from_apollo", company_domain, result)
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
                result = await response.json()
                return {'error': result}
            
@assistant_tool
async def get_enriched_customer_information(
    linkedin_url: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    required_fields: Optional[List[str]] = None,
    data_sources: Optional[List[str]] = None,
):
    """
    Fetch a person's details from specified data sources using LinkedIn URL, email, or phone number.

    Parameters:
    - **linkedin_url** (*str*, optional): LinkedIn profile URL of the person.
    - **email** (*str*, optional): Email address of the person.
    - **phone** (*str*, optional): Phone number of the person.
    - **required_fields** (*List[str]*, optional): Properties of the customer to fetch (e.g., 'job_history', 'education_history', 'skills', etc.).
    - **data_sources** (*List[str]*, optional): Data sources to fetch from (e.g., 'apollo', 'zoominfo', 'websearch', 'linkedin'). Defaults to all sources.

    Returns:
    - **dict**: JSON response containing person information.
    """
    # Set default values if not provided
    if required_fields is None:
        required_fields = [
            'job_history',
            'education_history',
            'skills',
            'headline',
            'summary',
            'experiences',
            'projects',
            'certifications',
            'publications',
            'languages',
            'volunteer_work',
        ]
    if data_sources is None:
        data_sources = ['apollo', 'zoominfo', 'websearch', 'linkedin']
        
    data = await enrich_person_info_from_apollo(
                linkedin_url=linkedin_url,
                email=email,
                phone=phone,
            )
    return data

@assistant_tool
async def get_enriched_company_information(
    company_domain: Optional[str] = None,
    required_fields: Optional[List[str]] = None,
    data_sources: Optional[List[str]] = None,
):
    """
    Fetch a company's details from specified data sources using the company domain.
    
    Parameters:
    - **company_domain** (*str*, optional): Domain of the company.
    - **required_fields** (*List[str]*, optional): Properties of the company to fetch (e.g., 'technographics', 'firmographics', 'employee_count', etc.).
    - **data_sources** (*List[str]*, optional): Data sources to fetch from (e.g., 'apollo', 'zoominfo', 'builtwith', 'linkedin'). Defaults to all sources.

    Returns:
    - **dict**: JSON response containing company information.
    """
    return await enrich_company_info_from_apollo(company_domain=company_domain)



# Define the backoff strategy for handling rate limiting
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=5,
    giveup=lambda e: e.status != 429,
    factor=2,
)
async def fetch_apollo_data(session, url, headers, payload):
    key_data = f"{url}_{json.dumps(payload, sort_keys=True)}"
    key_hash = hashlib.sha256(key_data.encode()).hexdigest()
    cached_response = retrieve_output("fetch_apollo_data", key_hash)
    if cached_response:
        return cached_response

    async with session.post(url, headers=headers, json=payload) as response:
        if response.status == 200:
            result = await response.json()
            cache_output("fetch_apollo_data", key_hash, result)
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
            response.raise_for_status()

@assistant_tool
async def search_recent_job_changes(
    job_titles: List[str],
    locations: List[str],
    organization_num_employees_ranges: Optional[List[str]] = None,
    items_to_return: int = 100
) -> List[dict]:
    """
    Search for individuals with specified job titles, locations, and optionally organization employee ranges who have recently changed jobs using searchSignalIds.

    Parameters:
    - **job_titles** (*List[str]*): List of job titles to search for.
    - **locations** (*List[str]*): List of locations to search in.
    - **organization_num_employees_ranges** (*Optional[List[str]]*, optional): List of employee ranges to filter organizations by (e.g., ["1,10", "11,50"]). Defaults to None.
    - **items_to_return** (*int*, optional): Total number of items to return. Defaults to 100.

    Returns:
    - **List[dict]**: List of individuals matching the criteria or error details.
    """
    APOLLO_API_KEY = os.getenv('APOLLO_API_KEY')
    if not APOLLO_API_KEY:
        raise EnvironmentError("Apollo API key not found in environment variables")

    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "X-Api-Key": f"{APOLLO_API_KEY}",
    }

    url = 'https://api.apollo.io/v1/mixed_people/search'

    # Define the search signal ID for recent job changes (e.g., "Job Change (90 Days)")
    search_signal_ids = ["643daa349293c1cdaa4d00f8"]

    # Initialize the session
    async with aiohttp.ClientSession() as session:
        results = []
        page = 1
        per_page = min(items_to_return, 100)  # Apollo API allows a maximum of 100 items per page

        while len(results) < items_to_return:
            payload = {
                "person_titles": job_titles,
                "person_locations": locations,
                "search_signal_ids": search_signal_ids,
                "page": page,
                "per_page": per_page
            }

            if organization_num_employees_ranges:
                payload["organization_num_employees_ranges"] = organization_num_employees_ranges

            try:
                data = await fetch_apollo_data(session, url, headers, payload)
                people = data.get('people', [])
                if not people:
                    break
                results.extend(people)
                if len(people) < per_page:
                    break
                page += 1
            except aiohttp.ClientResponseError as e:
                if e.status == 429:
                    await asyncio.sleep(30)  # Wait before retrying
                else:
                    # Return error details as JSON string in an array
                    error_details = {
                        'status': e.status,
                        'message': str(e),
                        'url': str(e.request_info.url),
                        'headers': dict(e.headers),
                    }
                    error_json = json.dumps(error_details)
                    return [error_json]

        return results[:items_to_return]