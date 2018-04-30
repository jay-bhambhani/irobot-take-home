from typing import List

import requests
from requests import Response

FREE_API_TIER = 500

class Food2ForkApi:
    """
    Low level Food2Fork API client
    """
    def __init__(self, api_key: str):
        self.base_uri = 'http://food2fork.com/api/{}'
        self.limit = FREE_API_TIER
        self.key = api_key


    def search_recipes(self, q: List[str], sort: str='r', page: int=1) -> Response:
        """
        searches for recipes given a list of ingredients, returning a requests.Response object
        :param q: list of ingredients searched
        :param sort: how to sort the results: r for top rated, t for trendiness
        :param page: which page of results
        :return: requests.Response
        """
        search_path = 'search'
        params = {'key': self.key, 'q': ','.join(q), 'sort': sort, 'page': page}
        return requests.get(self.base_uri.format(search_path), params=params)

    def get_recipe(self, rId: int) -> Response:
        """
        get the recipe details for a particular recipe by rId (as provided by Food2Fork),
        returning a requests.Response object
        :param rId: rId of recipe
        :return: requests.Response
        """
        search_path = 'get'
        params = {'key': self.key, 'rId': rId}
        return requests.get(self.base_uri.format(search_path), params=params)

