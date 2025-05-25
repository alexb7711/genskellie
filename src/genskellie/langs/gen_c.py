from pathlib import Path

from genskellie.gen_util import prompt_y_n

##==============================================================================
# PRIVATE VARIABLES
CLASS_NAME = None
HEADER_GUARD = None
NAMESPACE = None
FILE_PATH = None

##==============================================================================
#
def run(out_f: Path, ft: str):
    # Get file text
    f_txt = None
    with open(ft, 'r') as f:
        f_txt = f.read()

    # Populate variables
    _populate_header_impl_vars(out_f)

    match ft.stem:
        case "header" | "implementation":
            _gen_header_implementation(ft, out_f, f_txt)
        case "interface":
            _replace_txt(out_f.with_suffix('.h'), f_txt)
        case "test":
            ## If the name is not formatted correctly
            if 'test_' not in str(out_f):
                out_f = out_f.parent / Path('test_' + out_f.name).with_suffix('.cpp')

            _replace_txt(out_f, f_txt)
        case _:
            return

    return

################################################################################
# GENERATION FUNCTIONS
################################################################################

##==============================================================================
#
def _gen_header_implementation(ft: str, out_f: Path, f_txt: str):
    """!
    @brief Logic to determine whether to generate header and/or implementation
    files.

    @param ft
    @param out_f
    @param f_txt
    """
    ## Default to generate files
    bool_header = True if ft.stem == 'header' else False
    bool_implementation = True if ft.stem == 'implementation' else False

    ## If generating the header file, and the implementation file does not
    ## exist, prompt user to generate
    if bool_header and not out_f.with_suffix('.cpp').exists():
        bool_implementation = prompt_y_n("Generate implementation?")
    ## Else if generating the implementation file, and the header file does not
    ## exist, prompt user to generate
    elif bool_implementation and not out_f.with_suffix('.h').exists():
        bool_header = prompt_y_n("Generate header?")

    ## If the header is to be generated
    if bool_header: _replace_txt(out_f.with_suffix('.h'), f_txt)
    ## If the implementation is to be generated
    if bool_implementation: _replace_txt(out_f.with_suffix('.cpp'), f_txt)
    return

################################################################################
# HELPER FUNCTIONS
################################################################################
##==============================================================================
#
def _populate_header_impl_vars(out_f: Path):
    """!
    @brief Populate the required variables for header/implementation files

    @param out_f Output file path
    """
    global NAMESPACE
    global CLASS_NAME
    global HEADER_GUARD
    global FILE_PATH

    if not NAMESPACE: NAMESPACE = input('Namespace [None]: ')
    if not NAMESPACE: NAMESPACE = 'IGNORE'

    if not CLASS_NAME: CLASS_NAME = input(f'Class Name [{out_f.stem}]: ')
    if not CLASS_NAME or CLASS_NAME.isspace(): CLASS_NAME = out_f.stem

    HEADER_GUARD = out_f.stem.upper()
    FILE_PATH = out_f.stem.upper()
    return

##==============================================================================
#
def _replace_txt(out_f: Path, f_txt: str):
    """!
    @brief Update the text for C files

    @param f_txt Text of the file

    @returns
    Updated file text
    """
    # Remove namespace
    if not NAMESPACE or NAMESPACE.isspace() or NAMESPACE == 'IGNORE':
        f_txt = f_txt.replace('${NAMESPACE_BEGIN}\n\n', '')
        f_txt = f_txt.replace('${NAMESPACE_END}\n\n', '')
    # Include namespace
    else:
        f_txt = f_txt.replace('${NAMESPACE_BEGIN}', f'NAMESPACE {NAMESPACE}\n{{')
        f_txt = f_txt.replace('${NAMESPACE_END}', '}')

    f_txt = f_txt.replace('${HEADER_GUARD}', HEADER_GUARD)
    f_txt = f_txt.replace('${CLASS_NAME}', CLASS_NAME)
    ft_txt = f_txt.replace('${FILE_PATH}', FILE_PATH)
    f_txt = _method_separator(f_txt)

    with open(out_f, 'a') as f: f.write(f_txt)
    return f_txt

##==============================================================================
#
def _method_separator(f_txt: str, separator='=', length=78) -> str:
    """!
    @brief Update the text separator comments.

    @param f_txt
    @param separator
    @param length

    @return
    Updated text string with method separator.
    """
    return f_txt.replace('${METHOD_SEPARATOR}', '//'+(separator * length))
