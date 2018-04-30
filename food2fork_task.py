#!/usr/bin/env python
import argparse
import re
from typing import List

from inflection import pluralize, singularize

from f2f.food2fork_connector import Food2ForkConnector

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ingredients", help='comma-separated list of ingredients', type=str)


def most_popular_recipe_for_ingredients(ingredients: List[str]) -> List[str]:
    """
    gets missing ingredients for most popular recipe using ingredients searched
    :param ingredients: ingredients to search with
    :return: list of missing ingredients
    """
    f2f = Food2ForkConnector()
    recipe_for_ingredients = f2f.most_popular_recipe(ingredients)
    most_popular_ingredients_list = f2f.recipe_ingredients(recipe_for_ingredients.f2f_url)
    diffed_list = _diff_recipe_lists(ingredients, most_popular_ingredients_list)
    return diffed_list


def _diff_recipe_lists(searched_ingredients, popular_recipe_ingredients) -> List[str]:
    """
    diffs searched ingredient list with popular recipe ingredient list
    :param searched_ingredients: essentially the food2fork query
    :param popular_recipe_ingredients: most popular recipe returned ingredients
    :return: diffed list
    """
    searched_set = set(searched_ingredients)
    diffed_list = []
    for popular_recipe_ingredient in popular_recipe_ingredients:
        skip = False
        ingredient_tokens = _tokenize_popular_recipe_ingredient(popular_recipe_ingredient)
        for token in ingredient_tokens:
            if (token in searched_set) or (pluralize(token) in searched_set) or (singularize(token) in searched_set):
                skip = True
        if not skip:
            diffed_list.append(popular_recipe_ingredient)
    return diffed_list


def _tokenize_popular_recipe_ingredient(popular_recipe_ingredient: str) -> List[str]:
    """
    tokenizing ingredient returned in search. Simple tokenization for now
    :param popular_recipe_ingredient: returned recipe ingredient
    :return: tokenized recipe ingredient
    """
    tokens = re.compile('[a-zA-Z0-9/-]+')
    return tokens.findall(popular_recipe_ingredient)


if __name__ == '__main__':
    args = parser.parse_args()
    searched_ingredients = args.ingredients.split(',')
    print(most_popular_recipe_for_ingredients(searched_ingredients))
