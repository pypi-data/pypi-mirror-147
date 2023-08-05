from xml.etree import ElementTree
from typing import List, Set


def validate_child_elements(target_element: ElementTree.Element, expected_child_element_set: Set[str]) -> None:
    """
    Validate that there are unexpected child elements.

    :param target_element: Element you want to verify child elements
    :param expected_child_element_set: Expected element set
    :return: None
    """
    child_element_set = set([child_element.tag for child_element in target_element.findall('*')])
    different_child_element_set = child_element_set.difference(expected_child_element_set)
    if different_child_element_set:
        raise Exception(f"Unexpected child element(s) in {target_element.tag}.\n{different_child_element_set}")


def validate_attributes(target_element: ElementTree.Element, expected_attribute_set: Set[str]) -> dict:
    """
    Validate that there are unexpected attributes.

    :param target_element: Element you want to verify attributes
    :param expected_attribute_set: Expected attribute set
    :return: Attribute dict of the target element
    """
    element_attribute_dict = target_element.attrib
    different_attribute_set = set(element_attribute_dict.keys()).difference(expected_attribute_set)
    if different_attribute_set:
        raise Exception(f"Unexpected attribute(s) in {target_element.tag}.\n{different_attribute_set}")
    return element_attribute_dict


def validate_no_attributes(target_element: ElementTree.Element) -> None:
    """
    Validate that there are no attributes.

    :param target_element: Element you want to verify that there are no attributes
    :return: None
    """
    if target_element.attrib:
        raise Exception(f"Unexpected attribute(s) in {target_element.tag}.\n{target_element.attrib}")


def validate_no_child_elements(target_element: ElementTree.Element) -> None:
    """
    Validate that there are no child elements.

    :param target_element: Element you want to verify that there are no child elements
    :return: None
    """
    if target_element.findall('*'):
        child_element_set = set([child_element.tag for child_element in target_element.findall('*')])
        raise Exception(f"Unexpected child element(s) in {target_element.tag}.\n{child_element_set}")


def validate_one_element(target_elements: List[ElementTree.Element]) -> ElementTree.Element:
    """
    In the XML preprocessing, it is verified that only one element searched in findall() function.
    If only one element exists, take out the corresponding element and return it.

    :param target_elements: Element you want to verify that there are only one element
    :return: ElementTree.Element
    """
    if not target_elements:
        raise Exception(f"This is an empty list. Use the conditional statement.")
    elif len(target_elements) != 1:
        raise Exception(f"More than one of {target_elements[0].tag} exists. Use a repeat statement.")
    else:
        return target_elements[0]


def validate_element(
        target: List[ElementTree.Element] or ElementTree.Element,
        expected_attribute_set: Set[str] = None,
        expected_child_element_set: Set[str] = None) -> ElementTree.Element:
    """
    Perform overall verification of the target(Elements or Element).

    :param target: (Elements or Element) you want to verify
    :param expected_attribute_set: Expected attribute set
    :param expected_child_element_set: Expected element set
    :return: target
    """
    if isinstance(target, list):
        target = validate_one_element(target)

    if expected_attribute_set:
        validate_attributes(target, expected_attribute_set)
    else:
        validate_no_attributes(target)

    if expected_child_element_set:
        validate_child_elements(target, expected_child_element_set)
    else:
        validate_no_child_elements(target)

    return target


def get_cleaned_inner_text(target_element: ElementTree.Element) -> str or None:
    """
    Extract the string from the element and return it.
    The returned string is refined using the strip() function.

    :param target_element: Element you want to get inner text.
    :return: Refined text or None
    """
    result = target_element.text
    if not result:
        result = None
    else:
        result = result.strip()
        if not result:
            result = None

    return result


def get_cleaned_inner_text_with_validation(target_element: ElementTree.Element) -> str or None:
    """
    When element has only content, you can perform validation and getting text.

    :param target_element: Element(it has only content) you want to get inner text.
    :return: Refined text or None
    """
    return get_cleaned_inner_text(validate_element(target_element))
