import re

def fix_xref(dita_file, encoding):
  """Fixes a broken xref in a DITA XML file.

  Args:
    dita_file: The path to the DITA XML file.
    encoding: The encoding of the DITA XML file.

  Returns:
    The fixed DITA XML file.
  """

  with open(dita_file, "r", encoding=encoding) as f:
    dita_content = f.read()

  # Find all xref elements.
  xref_elements = re.findall(r"<xref href=\"#(.*?)\">", dita_content)

  # For each xref element, check if the target element id exists in the same topic.
  for xref_element in xref_elements:
    target_element_id = xref_element[1]
    parent_topic_element = re.search(r"<topic id=\"(.*?)\">", dita_content)
    if parent_topic_element:
      parent_topic_id = parent_topic_element.group(1)

      # Check if the target element id is contained in the same topic.
      if target_element_id not in parent_topic_id:
        # The target element id is not contained in the same topic, so the xref is broken.

        # Search for the target element id in the complete file outside the current topic.
        for topic in dita_content.split("<topic"):
          if target_element_id in topic:
            break

        # If the target element id is found, do a recursive ancestor search until the first ancestor element named topic is found.
        if topic:
          topic_id = re.search(r"id=\"(.*?)\">", topic).group(1)
          while not topic_id.startswith("topic"):
            topic = re.search(r"<topic (.*?)>", topic).group(1)
            topic_id = re.search(r"id=\"(.*?)\">", topic).group(1)

        # Prepend the topic id value after '#' in the href attribute value of the xref in question. Also add a '/' after the topic id value.
        if topic_id:
          new_href = "#" + topic_id + "/" + target_element_id
          dita_content = dita_content.replace(xref_element, "<xref href=\"" + new_href + "\"/>")

  # Write the fixed DITA XML file to disk.
  with open(dita_file, "w", encoding=encoding) as f:
    f.write(dita_content)

if __name__ == "__main__":
  dita_file = "my_dita_file.dita"
  encoding = "utf-8"
  fix_xref(dita_file, encoding)
