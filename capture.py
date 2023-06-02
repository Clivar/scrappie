from common import retry
from shared_driver import SharedDriver
import logging
logger = logging.getLogger(__name__)

def validate_capture_type(capture_type: str, response_type: str) -> bool:
    allowed_types = {'outerhtml', 'innerhtml', 'text'}
    allowed_types_for_json = {'text'}

    if capture_type.startswith('func:'):
        return True

    if response_type == 'json':
        if capture_type not in allowed_types_for_json:
            logger.error(f"Invalid capture_type for JSON response: {capture_type}")
            return False
    elif capture_type not in allowed_types:
        logger.error(f"Invalid capture_type: {capture_type}")
        return False

    return True

def execute_func(script):
    driver = SharedDriver.get_instance()
    result = driver.execute_script(script)
    if isinstance(result, list) and len(result) == 2:
        return tuple(result)
    elif not isinstance(result, list):
        return result, result

    raise ValueError('Script did not return one value or an array with exactly 2 items')

@retry()
def capture_element(element, capture_type: str, url: str):
    if capture_type == 'outerhtml':
        return element.get_attribute('outerHTML'), element.get_attribute('outerHTML')
    elif capture_type == 'innerhtml':
        return element.get_attribute('innerHTML'), element.get_attribute('innerHTML')
    elif capture_type == 'text':
        return element.text, element.text
    elif capture_type.startswith('func:'):
        func = capture_type[5:]
        func = f"return (function(innerhtml, outerhtml, text, url) {{ {func} }})('{element.get_attribute('outerHTML')}', '{element.get_attribute('innerHTML')}', '{element.text}', '{url}')"
        return execute_func(func)

@retry()   
def capture_json_value(value, capture_type: str, url: str):
    if capture_type == 'text':
        return value, value
    elif capture_type.startswith('func:'):
        func = capture_type[5:]
        func = f"return (function(value, url) {{ {func} }})('{value}', '{url}')"
        return execute_func(func)