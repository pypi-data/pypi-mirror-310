def flames_game(name1, name2):
    """
    Determine the FLAMES relationship between two names.

    Special case:
    - If either name is 'Tanujairam' or 'Rupali', a special message is returned.

    Args:
        name1 (str): The first name.
        name2 (str): The second name.

    Returns:
        str: The relationship category (Friends, Love, Affection, Marriage, Enemy, Siblings).
    """
    # Convert names to lowercase to make the comparison case-insensitive
    name1 = name1.lower()
    name2 = name2.lower()

    # Check if the names are "Tanujairam" or "Rupali"
    if name1 in {"tanujairam", "rupali"} or name2 in {"tanujairam", "rupali"}:
        return "You can't play the game with my owner, lol."

    # List of FLAMES categories
    flames_categories = ['Friends', 'Love', 'Affection', 'Marriage', 'Enemy', 'Siblings']

    # Remove spaces for calculation
    name1 = name1.replace(" ", "")
    name2 = name2.replace(" ", "")

    # Step 1: Calculate remaining characters after removing common letters
    combined_count = len(name1) + len(name2)
    for char in set(name1):
        common_count = min(name1.count(char), name2.count(char))
        combined_count -= 2 * common_count

    # Step 2: Use the combined_count to determine the FLAMES category
    while len(flames_categories) > 1:
        split_index = (combined_count % len(flames_categories)) - 1
        if split_index >= 0:
            flames_categories = flames_categories[split_index + 1:] + flames_categories[:split_index]
        else:
            flames_categories.pop()

    return flames_categories[0]


# Main code to run as a standalone script
if __name__ == "__main__":
    # Ask for user input directly when the script is executed
    name1 = input("Enter the first name: ")
    name2 = input("Enter the second name: ")

    # Call the flames_game function with user inputs
    result = flames_game(name1, name2)

    # Print the result
    print(f"The relationship between {name1} and {name2} is: {result}")
