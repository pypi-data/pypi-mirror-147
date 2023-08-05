from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json

class Badut(object):
    def __init__(self):
        self.headers = {}
    
    async def fetch(self, target: str, timeout: int = None, parse_json: bool = False, with_headers: dict = {'User-Agent': 'Badut/1.0.1'}):
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
        self.req = Request(target, headers=with_headers)
        with urlopen(self.req, timeout=timeout) as response:
            data = response.read()
            if parse_json:
                return json.loads(data)
            return data