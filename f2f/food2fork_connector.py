import json
import os
import re
from typing import List, Optional, NamedTuple

from f2f import ROOT_DIR
from f2f.food2fork_api import Food2ForkApi

SECRETS_LOCATION = '../config/secrets.json'


class ConnectorException(Exception):
    """
    An error raised by the Food2ForkConnector
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RecipeMeta(NamedTuple):
    """
    A simple metadata structure for a returned Food2Fork Recipe
    """
    image_url: Optional[str]
    source_url: Optional[str]
    f2f_url: Optional[str]
    title: Optional[str]
    publisher: Optional[str]
    publisher_url: Optional[str]
    social_rank: Optional[float]
    page: Optional[int]
    ingredients: Optional[List[str]]

    @classmethod
    def from_json(cls, meta):
        return cls(
            image_url=meta.get('image_url'),
            source_url=meta.get('source_url'),
            f2f_url=meta.get('f2f_url'),
            title=meta.get('title'),
            publisher=meta.get('publisher'),
            publisher_url=meta.get('publisher_url'),
            social_rank=meta.get('social_rank'),
            page=meta.get('page'),
            ingredients=meta.get('ingredients')
        )


class SearchResponse(NamedTuple):
    """
    Response returned by Food2Fork Search API
    """
    count: Optional[int]
    recipes: Optional[List[RecipeMeta]]

    @classmethod
    def from_json(cls, resp):
        return cls(count=resp.get('count'), recipes=[RecipeMeta.from_json(recipe) for recipe in resp.get('recipes')])


class GetReponse(NamedTuple):
    """
    Response returned by Food2Fork Get API
    """
    recipe: Optional[RecipeMeta]

    @classmethod
    def from_json(cls, resp):
        recipe = RecipeMeta.from_json(resp.get('recipe'))
        return cls(recipe=recipe)


class Food2ForkConnector:
    """
    Higher level Food2Fork client for our purposes
    """
    def __init__(self):
        self.f2f_url_struct = 'scheme//base/path/rId'

    @property
    def api(self):
        """
        loads Food2Fork API key
        """
        secrets_file_path = os.path.abspath(os.path.join(ROOT_DIR, SECRETS_LOCATION))
        with open(secrets_file_path) as f:
            secrets = json.load(f)
        return Food2ForkApi(secrets.get('food2fork_api_key'))

    def most_popular_recipe(self, ingredients: List[str]) -> RecipeMeta:
        """
        gets most popular recipe given a list of ingredients
        :param ingredients: list of ingredients to search
        :return: recipe metadata of the most popular recipe given the searched ingredients
        """
        response = self.api.search_recipes(q=ingredients)
        if not response.ok:
            raise ConnectorException('Unexpected API response: ', response.text)
        search_data = SearchResponse.from_json(response.json())
        return search_data.recipes[0]

    def recipe_ingredients(self, url: str) -> List[str]:
        """
        gets ingredients given the url of the recipe
        :param url: food2fork url of the recipe desired
        :return:
        """
        rId = self._get_rId_from_f2f_url(url)
        response = self.api.get_recipe(rId)
        if not response.ok:
            raise ConnectorException('Unexpected API response: ', response.text)
        get_data = GetReponse.from_json(response.json())
        return get_data.recipe.ingredients

    def _get_rId_from_f2f_url(self, url) -> str:
        """
        given a url of a food2fork url (eg. http://food2fork.com/view/Jalapeno_Popper_Grilled_Cheese_Sandwich/35382),
        get the rId of the recipe (above would be 35382)
        :param url: food2fork url
        :return: rId
        """
        parts = self._split_url_into_parts(url)
        return parts.get('rId')

    def _split_url_into_parts(self, url) -> dict:
        """
        break food2fork url (eg. http://food2fork.com/view/Jalapeno_Popper_Grilled_Cheese_Sandwich/35382)
        into its requisite structure
        :param url: food2fork url
        :return: key-value map of url structure
        """
        url_parts = re.split('[/:]+', url)
        expected_parts = re.split('[/:]+', self.f2f_url_struct)
        return {key: value for key, value in zip(expected_parts, url_parts)}