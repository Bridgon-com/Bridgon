import re
import xml.etree.ElementTree as ET


def fix_cross_references(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Create a dictionary to store element IDs and their corresponding elements
    element_dict = {}

    # Build the element dictionary
    for element in root.iter():
        element_id = element.get("id")
        if element_id is not None:
            element_dict[element_id] = element

    # Find and fix broken cross-references
    for element in root.iter():
        for attribute, value in element.items():
            if attribute.endswith("ref"):
                match = re.match(r'#([A-Za-z]+_\d+)', value)
                if match:
                    referenced_id = match.group(1)
                    if referenced_id not in element_dict:
                        # Find the target element in the XML file
                        target_element = element_dict.get(referenced_id)
                        if target_element is not None:
                            # Find the parent topic element that contains the target element
                            parent_topic = None
                            for ancestor in target_element.iterancestors():
                                if ancestor.tag == "topic":
                                    parent_topic = ancestor.get("id")
                                    break

                            if parent_topic is not None:
                                # Add the parent topic ID before the target element ID in the cross reference
                                fixed_value = value.replace(referenced_id, f'{parent_topic}/{referenced_id}')
                                element.set(attribute, fixed_value)
                                print(f"Fixed broken cross reference in element: {element.tag}, attribute: {attribute}, "
                                      f"old value: {value}, new value: {fixed_value}")

    # Save the updated XML file
    tree.write(xml_file)


# Usage
fix_cross_references("input.xml")
