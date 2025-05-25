##==============================================================================
#
def prompt_y_n(question: str) -> bool:
    """!
    @brief Prompt the user with the given question and expect a yes or no
    response

    @param question String to prompt the user with.

    @returns True if user responds (Y/y) or False if user response (N/n).
    """
    response = input(question + ' (Y/N): ')
    if not response or response.isspace(): response = False
    return True if response == 'y' else False
