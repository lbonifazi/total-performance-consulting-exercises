import math

from helpers.utils import load_json, get_elements, get_center_coordinates
from setup.setup_app import LOCATOR_KEY_NAME, ELEMENT_NAME_PLACEHOLDER, FINDERS_KEY_NAME, DATA_FILE_PATH
from model.element_dto import Element


def find_element(element_name):
    """Return the first matching Element object inside the dictionary.
    :param element_name: name of the Element to find
    :type element_name: str
    :return an Element object or a None value if not found
    """
    element_list = []

    # Load dictionary from File1.json
    dictionary = load_json('{}/File1.json'.format(DATA_FILE_PATH))

    if dictionary is not None:
        if element_name in dictionary.keys():
            # Look for specific definition that match with the element_name
            locator = dictionary[element_name][LOCATOR_KEY_NAME]
            element_list = get_elements(locator)
        else:
            # Look the element with the finders locators
            for finder in dictionary.get(FINDERS_KEY_NAME):
                locator = finder[LOCATOR_KEY_NAME].replace(ELEMENT_NAME_PLACEHOLDER, element_name)
                element_list = get_elements(locator)
                if len(element_list) > 0:
                    break
    if len(element_list) > 0:
        return element_list[0]
    else:
        return None


def find_element_near_to(element, locator):
    """Return the first element object of the element with locator X that is nearest to element A
    :param locator: locator X
    :type locator: str
    :param element: element A
    :type element: Element
    :return an Element object or a None value if not found.
    """
    if None not in (element, locator):
        # Get list of elements that match with the locator
        element_list = get_elements(locator)

        # Get the center of the element
        x1, y1 = get_center_coordinates(element)

        # Search min distance
        found_element = min_distance = None
        for e in element_list:
            x2, y2 = get_center_coordinates(e)

            # calculate the distance using the Pythagorean Theorem (a**2 + b**2 = c**2)
            element_distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
            if min_distance is None:
                min_distance = element_distance
            if element_distance <= min_distance:
                found_element = e
                min_distance = element_distance
        return found_element
    else:
        return None
