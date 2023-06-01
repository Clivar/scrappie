from common import retry
from shared_driver import SharedDriver

def validate_capture_type(capture_type: str, response_type: str) -> bool:
    allowed_types = {'outerhtml', 'innerhtml', 'text', 'func'}
    allowed_types_for_json = {'text', 'func'}

    if response_type == 'json':
        if capture_type not in allowed_types_for_json:
            print(f"Invalid capture_type for JSON response: {capture_type}")
            return False
    else:
        if capture_type not in allowed_types:
            print(f"Invalid capture_type: {capture_type}")
            return False

    return True

def execute_func(script):
    driver = SharedDriver.get_instance()
    result = driver.execute_script(script)

    if isinstance(result, list) and len(result) == 2:
        return tuple(result)

    raise ValueError('Script did not return an array with exactly 2 items')

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
        func = f"return ({func})({element.get_attribute('innerHTML')}, {element.get_attribute('outerHTML')}, {element.text}, {url})"
        return execute_func(func)

@retry()   
def capture_json_value(value, capture_type: str, url: str):
    if capture_type == 'text':
        return value, value
    elif capture_type.startswith('func:'):
        func = capture_type[5:]
        func = f"return ({func})({value}, {url})"
        return execute_func(func)