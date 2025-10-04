##==============================================================================
#
def prompt_y_n(question: str) -> bool:
    """!
    @brief Prompt the user with the given question and expect a yes or no
    response

    @param question String to prompt the user with.

    @returns True if user responds (Y/y) or False if user response (N/n).
    """
    response = input(question + ' (Y/N): ').lower()
    if not response or response.isspace(): response = False
    return True if response == 'y' else False

##==============================================================================
#
def method_separator(f_txt: str,
                     indent_lvl: int  = 0,
                     indent: int = 4,
                     comment: str = '//',
                     separator: str = '=',
                     width: int = 80) -> str:
    """!
    @brief Update the text separator comments.

    @param f_txt
    @param indent_lvl
    @param indent
    @param comment
    @param separator
    @param width

    @return
    Separator comment.
    """
    length = width - (indent_lvl * indent) - len(comment)
    return comment + (separator * length)
