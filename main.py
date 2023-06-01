from selenium.webdriver.support import expected_conditions as EC
from typing import List
from dataclasses import dataclass
import json
import sys
import pprint
from capture import validate_capture_type
from extract import extract_html, extract_json

from macro import Macro, validate_macros
from notify import Condition, notify, validate_conditions
from pageing import parse_url_with_optional_pageing

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
        print(f"Invalid response type: {response_type}. Must be either 'json' or 'html'.")
        return False
    return True

def extract(response_type: str, url: str, post_body: str, path: str, macros: List[Macro], capture_type: str):
    if response_type == 'json':
        return extract_json(url, post_body, path, capture_type)
    elif response_type == 'html':
        return extract_html(url, path, macros, capture_type)

def main():
    # Check if there is at least one argument
    if len(sys.argv) < 2:
        print("Missing argument: job file")
        return

    # The first argument is the script name itself, so we take the second
    json_file = sys.argv[1]

    with open(json_file, 'r') as file:
        data = json.load(file)

    data['conditions'] = [Condition(**c) for c in data['conditions']]
    data['macros'] = [Macro(**m) for m in data['macros']]
    job = Job(**data)

    # Validate Job parameters
    if not validate_macros(job.macros):
        print("Invalid macros.")
        return

    if not validate_response_type(job.response_type):
        print("Invalid response type.")
        return

    if not validate_conditions(job.conditions):
        print("Invalid conditions.")
        return

    if not validate_capture_type(job.capture_type, job.response_type):
        print("Invalid capture type.")
        return

    urls = parse_url_with_optional_pageing(job.url)
    results = []
    for url in urls:
        result = extract(job.response_type, url, job.post_body, job.path, job.macros, job.capture_type)
        results.extend(result)
    
    for result in results:
        notify(result, job.conditions)

if __name__ == "__main__":
    main()