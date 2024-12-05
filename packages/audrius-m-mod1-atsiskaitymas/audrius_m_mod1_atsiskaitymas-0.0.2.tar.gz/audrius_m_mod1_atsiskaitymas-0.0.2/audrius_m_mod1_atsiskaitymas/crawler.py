import requests
from typing import Optional
from bs4 import BeautifulSoup


def crawl(time_limit: int = 60, source: str = 'https://en.wikipedia.org/wiki/Main_Page', return_format: str = 'html') -> \
        Optional[str]:
    """
    Crawl data from a specified source within a given time limit and return the data in a specified format.

    :param time_limit: The maximum time (in seconds) to spend crawling. Default is 60 seconds.
    :param source: The source to crawl data from. Default is 'https://en.wikipedia.org/wiki/Main_Page'.
    :param return_format: The format in which to return the data. Default is 'html'. But plain text is available
    :return: The crawled data in the specified format, or None if no data is found.
    """
    try:
        # Set a timeout for the request
        response: requests.Response = requests.get(source, timeout=time_limit)

        # Check if the request was successful
        if response.status_code == 200:
            # Process the response data
            data = response.text
            if return_format == 'html':
                return data
            elif return_format == 'text':
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract text content (this will also remove HTML tags)
                text = soup.get_text(separator=' ')  # Use a space as a separator between elements
                # - Remove extra whitespace
                text = ' '.join(text.split())
                return text
            else:
                raise NotImplementedError("This data format has not been implemented yet.")
        else:
            print(f"Failed to retrieve data: HTTP {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
