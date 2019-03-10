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

class InputValidator:

    def __init__(self):
        pass

    def validate_input_type(self, input, type):
        assert(type(input), type), "'{input}' provided does not match the expected type of {type}".format(input=input, type=type)
        return input
