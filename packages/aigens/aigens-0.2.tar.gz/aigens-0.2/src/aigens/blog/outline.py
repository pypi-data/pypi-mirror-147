""" aigens.blog Outline Methods """
import json
import requests


__all__ = ['BlogOutlineAPI']


class BlogOutlineAPI:
    """ BlogOutlineAPI Class """
    # https://rapidapi.com/apis-world-apis-world-default/api/blog-outline/
    def __init__(self, api_key, api_host, request_timeout=10):
        """ BlogOutlineAPI.__init__

        Constructor for BlogOutlineAPI.

        Arguments:
            api_key: RapidAPI key
            api_host: RapidAPI host
            request_timeout: Seconds before timeout

        Returns:
            An intialized BlogOutlineAPI object.
        """
        self._api_key = api_key
        self._api_host = api_host
        self._request_timeout = request_timeout
        self._session = requests.Session()
        self._api_url = f'https://{self._api_host}/blog-outline'

    def __construct_headers(self):
        """ BlogOutlineAPI.__construct_headers

        Internal method to construct headers for all API calls.

        Arguments:
            None

        Returns:
            Dictionary of headers
        """
        return {
            "X-RapidAPI-Host": self._api_host,
            "X-RapidAPI-Key": self._api_key,
        }

    def __request(self, params=None, method='GET'):
        """ BlogOutlineAPI.__request

        Internal request method.

        Arguments:
            url: URL to fetch
            params: Query string parameters
            method: HTTP method verb

        Returns:
            Dictionary of response content. Raises an error
            on failure.
        """
        try:
            response = self._session.request(
                method,
                self._api_url,
                headers=self.__construct_headers(),
                timeout=self._request_timeout,
                params=params,
            )
        except requests.exceptions.RequestException:
            raise

        try:
            response.raise_for_status()
            content = json.loads(response.content.decode('utf-8'))
            return content
        except json.decoder.JSONDecodeError:
            raise

    def generate_outline(self, prompt):
        """ BlogOutlineAPI.generate_outline

        Uses trained models to generate a blog article outline from
        the user's prompt text.

        Arguments:
            prompt: Topic prompt

        Returns:
            List of strings
        """
        # TODO: Add type checking and sanity checking to prompt

        return self.__request(
            params={"topic": prompt}
        )
