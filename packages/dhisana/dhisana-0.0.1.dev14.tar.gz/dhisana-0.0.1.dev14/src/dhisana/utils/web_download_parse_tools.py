# Tools to download and parse web content

import csv
import logging
import os
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from dhisana.utils.assistant_tool_tag import assistant_tool
from urllib.parse import urlparse
import re
from datetime import datetime

from dhisana.utils.dataframe_tools import get_structured_output

@assistant_tool
async def get_html_content_from_url(url):
    # Ensure the URL has a scheme
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = "https://" + url
        parsed_url = urlparse(url)

    # Ensure the URL has a subdomain
    if parsed_url.hostname and parsed_url.hostname.count('.') == 1:
        url = url.replace(parsed_url.hostname, "www." + parsed_url.hostname)
    
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        logging.info(f"Requesting {url}")
        try:
            await page.goto(url, timeout=10000)
            html_content = await page.content()
            return await parse_html_content(html_content)
        except Exception as e:
            logging.info(f"Failed to fetch {url}: {e}")
            return ""
        finally:
            await browser.close()

@assistant_tool
async def parse_html_content(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(['script', 'style']):
        element.decompose()
    return soup.get_text(separator=' ', strip=True)


@assistant_tool
async def clean_html_content(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(['script', 'style']):
        element.decompose()
    return str(soup)

@assistant_tool
async def process_files_in_folder_for_leads(folder_path: str, file_extension: str, response_type, required_properties=[], dedup_properties=[]):
    """
    Process files in a folder, extract structured data, and write to a CSV file.

    Parameters:
    - folder_path (str): The path to the folder containing files.
    - file_extension (str): The file extension to filter files (e.g., '*.html').
    - response_type: The type of response expected from get_structured_output.
    - required_properties (list, optional): List of properties that must be present in the structured data.
    - dedup_properties (list, optional): List of properties to use for deduplication.

    Returns:
    - str: The file path of the generated CSV file.
    """
    leads = []
    seen = set()

    for file_name in os.listdir(folder_path):
        if file_name.endswith(file_extension):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                html_content = file.read()
                parsed_content = await parse_html_content(html_content)
                prompt = "Extract structured content from input. Output is in JSON Format. \n\n Input: " + parsed_content
                prompt = prompt[:1040000]  # Limit prompt length to 4096 characters
                structured_data = await get_structured_output(parsed_content, response_type)

                # Check for required properties
                if required_properties and not all(prop in structured_data for prop in required_properties):
                    continue

                # Check for deduplication
                if dedup_properties:
                    dedup_key = tuple(structured_data.get(prop) for prop in dedup_properties if structured_data.get(prop))
                    if dedup_key in seen:
                        continue
                    seen.add(dedup_key)

                leads.append(structured_data)

    # Write the leads to a CSV file
    csv_file_path = os.path.join(folder_path, 'leads.csv')
    if leads:
        keys = leads[0].keys()
        with open(csv_file_path, 'w', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(leads)

    return csv_file_path


@assistant_tool
async def process_files_in_folder_for_linkedin_urls(folder_path: str, file_extension: str):
    """
    Process files in a folder, extract LinkedIn URLs, and write to a CSV file.

    Parameters:
    - folder_path (str): The path to the folder containing files.
    - file_extension (str): The file extension to filter files (e.g., '*.html').

    Returns:
    - str: The file path of the generated CSV file.
    """
    linkedin_urls = set()

    for file_name in os.listdir(folder_path):
        if file_name.endswith(file_extension):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    url = link['href']
                    if re.match(r'^https://www\.linkedin\.com/in/[^?]+', url):
                        linkedin_urls.add(url.split('?')[0])  # Remove query parameters

    # Write the LinkedIn URLs to a CSV file
    csv_file_path = os.path.join(folder_path, 'linkedin_urls.csv')
    with open(csv_file_path, 'w', newline='') as csv_file:
        dict_writer = csv.DictWriter(csv_file, fieldnames=['id', 'linkedin_url'])
        dict_writer.writeheader()
        for url in linkedin_urls:
            unique_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
            dict_writer.writerow({'id': unique_id, 'linkedin_url': url})

    return csv_file_path