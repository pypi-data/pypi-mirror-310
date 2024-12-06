import ast


def extract_lists_from_text(text: str, num_lists: int = -1):
    """
    Extracts and parses lists from the given text. Can retrieve all lists or a specified number of lists.

    :param text: The text containing lists to be extracted.
    :param num_lists: The number of lists to extract. Default is -1 (extract all lists).
    :returns: A list of parsed lists or an empty list if no valid lists are found.
    """
    try:
        # Find all list occurrences in the text
        lists = []
        start_index = 0

        while True:
            start_index = text.find("[", start_index)
            if start_index == -1:
                break  # No more lists found

            end_index = text.find("]", start_index) + 1
            if end_index == 0:
                break  # Invalid list syntax

            list_text = text[start_index:end_index]
            start_index = end_index  # Move index forward for the next search

            # Replace any wrong quote types with correct quotes
            list_text = list_text.replace("“", "\"").replace(
                "”", "\"").replace("‘", "'").replace("’", "'")

            try:
                # Safely parse the list
                parsed_list = ast.literal_eval(list_text)
                if isinstance(parsed_list, list):
                    lists.append(parsed_list)
            except Exception:
                continue  # Skip invalid lists

        # Limit the number of lists if num_lists is provided
        if num_lists > 0:
            return lists[:num_lists]

        return lists
    except Exception:
        return []  # Return an empty list in case of any errors


def extract_list_items_from_text(text: str):
    """
    Extracts all list items from the given text and combines them into a single flat list.

    :param text: The text containing lists to be extracted.
    :returns: A single combined list of all items from the extracted lists.
    """
    # Use the existing extract_lists_from_text function
    lists = extract_lists_from_text(text=text, num_lists=-1)

    # Combine all lists into one flat list
    combined_items = []
    for lst in lists:
        combined_items.extend(lst)

    return combined_items
