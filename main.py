from selenium.webdriver.support import expected_conditions as EC
from typing import List
from dataclasses import dataclass
import json
from capture import validate_capture_type
from extract import ExtractResult, extract_html, extract_json
from log import setup_logger_level

from macro import Macro, validate_macros
from notify import Condition, notify, validate_conditions
from pageing import parse_url_with_optional_pageing
import argparse

import logging
logger = logging.getLogger(__name__)

@dataclass
class Job:
    url: str
    path: str
    post_body: str
    response_type: str  
    macros: List[Macro]
    capture_type: str
    conditions: List[Condition]

def validate_response_type(response_type: str):
    valid_response_types = {'json', 'html'}
    if response_type not in valid_response_types:
        logger.error(f"Invalid response type: {response_type}. Must be either 'json' or 'html'.")
        return False
    return True

def extract(response_type: str, url: str, post_body: str, path: str, macros: List[Macro], capture_type: str):
    if response_type == 'json':
        return extract_json(url, post_body, path, capture_type)
    elif response_type == 'html':
        return extract_html(url, path, macros, capture_type)

def main():
    # Create a parser for command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-f', '--file', help='JSON file')
    args = parser.parse_args()

    setup_logger_level(args.debug)

    with open(args.file, 'r') as file:
        data = json.load(file)

    data['conditions'] = [Condition(**c) for c in data['conditions']]
    data['macros'] = [Macro(**m) for m in data['macros']]
    job = Job(**data)

    # Validate Job parameters
    if not validate_macros(job.macros):
        logger.error("Invalid macros.")
        return

    if not validate_response_type(job.response_type):
        logger.error("Invalid response type.")
        return

    if not validate_conditions(job.conditions):
        logger.error("Invalid conditions.")
        return

    if not validate_capture_type(job.capture_type, job.response_type):
        logger.error("Invalid capture type.")
        return

    urls = parse_url_with_optional_pageing(job.url)
    results: List[ExtractResult] = []
    for url in urls:
        result = extract(job.response_type, url, job.post_body, job.path, job.macros, job.capture_type)
        results.extend(result)
    
    for result in results:
        logger.info(f"Result #{result.order}: {result.match}")
        notify(result, job.conditions)

if __name__ == "__main__":
    main()