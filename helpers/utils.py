import json
import traceback

from setup.setup_app import FINDERS_KEY_NAME, IMPORT_KEY_NAME, DATA_FILE_PATH
from model.element_dto import Element
from setup.setup_logger import logger


def load_json(filename):
    """Receives the file name and returns the contained dictionary."""
    try:
        with open(filename) as json_file:
            dictionary = json.load(json_file)

            # import the dictionaries in import list
            if IMPORT_KEY_NAME in dictionary.keys():
                for filename_to_import in dictionary[IMPORT_KEY_NAME]:
                    imported_dict = load_json('{}/{}.json'.format(DATA_FILE_PATH, filename_to_import))

                    # add items from the dictionary imported to the main dictionary
                    for k, v in imported_dict.items():
                        if k == FINDERS_KEY_NAME:
                            if FINDERS_KEY_NAME in dictionary.keys():
                                dictionary[FINDERS_KEY_NAME] += v
                            else:
                                dictionary[FINDERS_KEY_NAME] = v
                        else:
                            dictionary.update({k: v})

            # remove unnecessary key from the dictionary
            dictionary.pop(IMPORT_KEY_NAME, None)
            return dictionary
    except IOError:
        logger.error(traceback.format_exc())


def get_elements(locator):
    """Receives a locator and returns a list of all element objects found with this locator.
    NOTE: this is a mock method created to test the logic of the exercise
    """
    elements_list = []
    if locator == 'Element1':
        elements_list = [Element(locator, 2, 3, 4, 5)]
    elif locator == 'class_name':
        elements_list = [
            Element(locator, 5, 4, 4, 5),
            Element(locator, 87, 22, 2, 7),
            Element(locator, 64, 26, 22, 24),
            Element(locator, 5, 4, 4, 5),
            Element(locator, 43, 33, 4, 5)]
    elif locator == '...class_name1...':
        elements_list = [
            Element(locator, 2, 35, 74, 85),
            Element(locator, 12, 22, 42, 52),
            Element(locator, 13, 11, 31, 42)]
    return elements_list


def get_center_coordinates(element):
    """Return the element's center coordinates of the Element object sent
    :type element: Element
    """
    x, y = element.position()
    width, height = element.size()

    # calculate center coordinates
    x_center = x + (width / 2)
    y_center = y + (height / 2)
    return x_center, y_center
