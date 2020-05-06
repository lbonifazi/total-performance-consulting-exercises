import math
from model.enums import SearchType
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
        return element_list[0] if element_list else None
    return None


def find_element_near_to(element, locator, search_type=SearchType.ALL):
    """Find a element object of the elements with locator X that is nearest to element A
    :param element: element A
    :type element: Element

    :param locator: locator X
    :type locator: str

    :param search_type: Type of search. Default = SearchType.ALL
    :type search_type: SearchType

    :return an Element object or a None value if not found.
    """
    if None not in (element, locator):
        # Get list of elements that match with the locator
        element_list = get_elements(locator)
        if element_list:
            # Get the center of the element
            x1, y1 = get_center_coordinates(element)

            found_elements = []
            min_distance = None
            # calculate distance for each element
            for e in element_list:
                element_distance = None
                x2, y2 = get_center_coordinates(e)
                if search_type in (SearchType.X_AXIS, SearchType.LEFT, SearchType.RIGHT):
                    # Search in X axis
                    if search_type == SearchType.LEFT and x1 >= x1:
                        continue
                    elif search_type == SearchType.RIGHT and x2 <= x1:
                        continue
                    else:
                        element_distance = abs(x2 - x1)
                elif search_type in (SearchType.Y_AXIS, SearchType.UP, SearchType.DOWN):
                    # Search in Y axis
                    if search_type == SearchType.UP and y2 <= y1:
                        continue
                    elif search_type == SearchType.DOWN and y2 >= y1:
                        continue
                    else:
                        element_distance = abs(y2 - y1)
                elif search_type == SearchType.ALL:
                    # Search in both axis. Calculate the distance using the Pythagorean Theorem and find the minimum
                    element_distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

                # save the minimal distance
                if min_distance is None or element_distance < min_distance:
                    min_distance = element_distance
                    found_elements = [e]
                elif element_distance == min_distance:
                    found_elements.append(e)

            # print a message if there are more than one element found with the same distance
            if len(found_elements) > 1:
                print("There are more than one element with the same distance. First element was returned. See log "
                      "for more information.")
                logger.info('Element founds: \n' + '\n'.join([str(e) for e in found_elements]))

            # return the first element of the list
            return found_elements[0] if found_elements else None
    return None
