""" aigens.blog Ideas Methods """
import json
import requests


__all__ = ['BlogIdeasAPI']


class BlogIdeasAPI:
    """ BlogIdeasAPI Class """
    # https://rapidapi.com/apis-world-apis-world-default/api/blog-ideas/
    def __init__(self, api_key, api_host, request_timeout=10):
        """ BlogIdeasAPI.__init__

        Constructor for BlogIdeasAPI.

        Arguments:
            api_key: RapidAPI key
            api_host: RapidAPI host
            request_timeout: Seconds before timeout

        Returns:
            An intialized BlogIdeasAPI object.
        """
        self._api_key = api_key
        self._api_host = api_host
        self._request_timeout = request_timeout
        self._session = requests.Session()
        self._api_url = f'https://{self._api_host}/blog-idea'

    def __construct_headers(self):
        """ BlogIdeasAPI.__construct_headers

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
        """ BlogIdeasPI.__request

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

    def generate_idea(self, prompt):
        """ BlogIdeasAPI.generate_outline

        Uses trained models to generate blog ideas based on
        the user's prompt text.

        Arguments:
            prompt: Topic prompt

        Returns:
            List of strings
        """
        # TODO: Add type checking and sanity checking to prompt

        return self.__request(
            params={"description": prompt}
        )
