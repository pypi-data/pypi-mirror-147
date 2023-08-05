from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json

async def fetch(target: str, timeout: int = None, parse_json: bool = False, with_headers: dict = {'User-Agent': 'Badut/1.0.1'}):
    """HTTP Request to the target URL
    
    Parameters
    ----------
    target : str
        The target URL

    timeout : int
        The timeout in seconds

    headers : dict
        The headers to be sent with the request

    parse_json : bool
        Whether to return the data as JSON

    Returns
    -------
    dict
        The raw data
    """
    req = Request(target, headers=with_headers)
    with urlopen(req, timeout=timeout) as response:
        data = response.read()
        if parse_json:
            return json.loads(data)
        return data

async def post(url, data):
    """HTTP POST Request to the target URL
    
    Parameters
    ----------
    url : str
        The target URL

    data : dict
        The data to be sent with the request

    Returns
    -------
    dict
        The response data
    """
    data = urlencode(data).encode('utf-8')
    req = Request(url, data)
    with urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def reformat(parser: dict):
    """Converts the json object to a more readable object.
    
    Parameters
    ----------
    parser : dict   
        The raw data

    Returns
    -------
    dict
        The new dictionaries with neat keys.
    """
    return json.dumps(parser, sort_keys=True, indent=4, ensure_ascii=False)