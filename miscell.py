def check(bool, message, line_number):
    """
    Kind of like assert. If bool evaluates to False,
    it prints the message and terminates the python program.
    bool - The boolean to evaluate
    message - The message to print if bool is False
    """
    if not bool:
        raise SyntaxError(message + ' Line number: {}'.format(line_number))