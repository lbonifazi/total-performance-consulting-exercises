import math

from helpers.utils import load_json, get_elements, get_center_coordinates
from setup.setup_app import LOCATOR_KEY_NAME, ELEMENT_NAME_PLACEHOLDER, FINDERS_KEY_NAME, DATA_FILE_PATH
from model.element_dto import Element
from setup.setup_logger import logger


def find_element(element_name):
    """Find element that match with element_name.
    :param element_name: name of the element to find
    :type element_name: str
    :return an Element object or a None value if not found
    """
    # Load dictionary from File1.json
    dictionary = load_json('{}/File1.json'.format(DATA_FILE_PATH))

    locators = []
    if dictionary is not None:
        # Look for specific definition that match with the element_name. Add locator to the list
        if element_name in dictionary.keys():
            locators.append(dictionary[element_name][LOCATOR_KEY_NAME])
        else:
            # Look for each locator in finders, replace the placeholder and add to the list
            for finder in dictionary.get(FINDERS_KEY_NAME):
                loc = finder[LOCATOR_KEY_NAME].replace(ELEMENT_NAME_PLACEHOLDER, element_name)
                locators.append(loc)

    # Look for existing elements for each locator in list
    for locator in locators:
        element_list = get_elements(locator)
        if element_list:
            return element_list[0]
    return None


def find_element_near_to(element, locator):
    """Find a element object of the elements with locator X that is nearest to element A
    :param locator: locator X
    :type locator: str
    :param element: element A
    :type element: Element
    :return an Element object or a None value if not found.
    """
    if None not in (element, locator):
        # Get list of elements that match with the locator
        element_list = get_elements(locator)
        if element_list:
            # Get the center of the element
            x1, y1 = get_center_coordinates(element)

            # Search minimum distance
            found_elements = []
            min_distance = None
            for e in element_list:
                x2, y2 = get_center_coordinates(e)
                # calculate the distance using the Pythagorean Theorem and find the minimum
                element_distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
                if min_distance is None or element_distance < min_distance:
                    min_distance = element_distance
                    found_elements = [e]
                elif element_distance == min_distance:
                    found_elements.append(e)

            # print a message if there are more than one element found with the same distance
            if len(found_elements) > 1:
                print("There are more than one element with the same distance. First element was returned. See log "
                      "for more information.")
                logger.info('Element founds: \n' + '\n'.join([str(e.__dict__) for e in found_elements]))

            return found_elements[0]
    return None
