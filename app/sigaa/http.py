""""A module for making HTTP requests."""

import requests

from urllib.parse import urljoin


class HttpClient:
    """A class for making HTTP requests."""

    def __init__(self, base_url: str) -> None:
        """
        Initialize the HttpClient.

        Args:
            base_url (str): The base URL for the requests.
        """
        self.base_url = base_url
        self.session = requests.Session()

    def _send_request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
        cookies: dict = None,
        allow_redirects: bool = True,
    ) -> requests.Response:
        """
        Send an HTTP request.

        Args:
            method (str): The HTTP method (e.g., GET, POST, PUT, DELETE).
            endpoint (str): The endpoint for the request.
            params (dict, optional): The query parameters. Defaults to None.
            data (dict, optional): The request body data. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.
            cookies (dict, optional): The request cookies. Defaults to None.
            allow_redirects (bool, optional): Whether to allow redirects. Defaults to True.

        Returns:
            requests.Response: The response object.
        """
        url = urljoin(base=self.base_url, url=endpoint)
        session = self.session
        response = session.request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            allow_redirects=allow_redirects,
        )
        return response

    def get(
        self,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
        cookies: dict = None,
        allow_redirects: bool = True,
    ) -> requests.Response:
        """
        Send a GET request.

        Args:
            endpoint (str): The endpoint for the request.
            params (dict, optional): The query parameters. Defaults to None.
            data (dict, optional): The request body data. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.
            cookies (dict, optional): The request cookies. Defaults to None.
            allow_redirects (bool, optional): Whether to allow redirects. Defaults to True.

        Returns:
            requests.Response: The response object.
        """
        return self._send_request(
            method="GET",
            endpoint=endpoint,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            allow_redirects=allow_redirects,
        )

    def put(
        self,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
        cookies: dict = None,
        allow_redirects: bool = True,
    ) -> requests.Response:
        """
        Send a PUT request.

        Args:
            endpoint (str): The endpoint for the request.
            params (dict, optional): The query parameters. Defaults to None.
            data (dict, optional): The request body data. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.
            cookies (dict, optional): The request cookies. Defaults to None.
            allow_redirects (bool, optional): Whether to allow redirects. Defaults to True.

        Returns:
            requests.Response: The response object.
        """
        return self._send_request(
            method="PUT",
            endpoint=endpoint,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            allow_redirects=allow_redirects,
        )

    def post(
        self,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
        cookies: dict = None,
        allow_redirects: bool = True,
    ) -> requests.Response:
        """
        Send a POST request.

        Args:
            endpoint (str): The endpoint for the request.
            params (dict, optional): The query parameters. Defaults to None.
            data (dict, optional): The request body data. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.
            cookies (dict, optional): The request cookies. Defaults to None.
            allow_redirects (bool, optional): Whether to allow redirects. Defaults to True.

        Returns:
            requests.Response: The response object.
        """
        return self._send_request(
            method="POST",
            endpoint=endpoint,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            allow_redirects=allow_redirects,
        )

    def delete(
        self,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
        cookies: dict = None,
        allow_redirects: bool = True,
    ) -> requests.Response:
        """
        Send a DELETE request.

        Args:
            endpoint (str): The endpoint for the request.
            params (dict, optional): The query parameters. Defaults to None.
            data (dict, optional): The request body data. Defaults to None.
            headers (dict, optional): The request headers. Defaults to None.
            cookies (dict, optional): The request cookies. Defaults to None.
            allow_redirects (bool, optional): Whether to allow redirects. Defaults to True.

        Returns:
            requests.Response: The response object.
        """
        return self._send_request(
            method="DELETE",
            endpoint=endpoint,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            allow_redirects=allow_redirects,
        )
