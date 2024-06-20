
# format_data.py

def format_data_for_display(people):
  """
  Formats a list of dictionaries containing person information
  into a list of strings with "Full Name: Title" format.

  Args:
      people: A list of dictionaries, where each dictionary represents
              a person with keys like "given_name", "family_name", and "title".

  Returns:
      A list of strings with formatted data for display.
  """
  formatted_data = []
  for person in people:
    full_name = f"{person['given_name']} {person['family_name']}"
    formatted_data.append(f"{full_name}: {person['title']}")
  return formatted_data

def format_data_for_excel(people):
  """
  Formats a list of dictionaries containing person information
  into a string suitable for pasting into an Excel spreadsheet.

  Args:
      people: A list of dictionaries, where each dictionary represents
              a person with keys like "given_name", "family_name", and "title".

  Returns:
      A string with formatted data for Excel.
  """

  headers = ",".join([person.keys() for person in people][0])
  data_lines = []
  for person in people:
    data_line = ",".join(person.values())
    data_lines.append(data_line)
  data = "\n".join(data_lines)
  
  return f"{headers}\n{data}\n"




