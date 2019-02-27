class StringModifier:
    """
    Is used to provide different treatments to string values
    """

    def __init__(self):
        pass

    def remove_escapes(self, string):
        """
        removes all escapes in the string
        """
        output = ''
        if not isinstance(string, str):
            pass

        else:
            for char in string:
                if char.isprintable():
                    output = output + char

        return output
