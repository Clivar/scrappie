import re
from typing import List

def parse_url_with_optional_pageing(url: str) -> List[str]:
    page_num_regex = re.search(r'{pagestart:(\d+),pageend:(\d+)}', url)
    if page_num_regex is not None:
        page_start = int(page_num_regex.group(1))
        page_end = int(page_num_regex.group(2))
    else:
        page_start = 0
        page_end = 0

    while page_start <= page_end:
        yield re.sub(r'{pagestart:\d+,pageend:\d+}', str(page_start), url)
        page_start += 1