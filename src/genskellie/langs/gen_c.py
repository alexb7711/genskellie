from pathlib import Path
from string import Template

from genskellie.gen_util import *

##==============================================================================
# PRIVATE VARIABLES
_CLASS_NAME = None
_CLASS_TESTED = None
_HEADER_GUARD = None
_NAMESPACE = None
_FILE_PATH = None
_FILE_TYPE = 'definition'

##==============================================================================
#
def run(out_f: Path, ft: str):
    # Get file text
    f_txt = _get_file_text(ft)

    match ft.stem:
        case "header" | "implementation":
            ## Update the extension
            ext = None
            if ft.stem == 'header': ext = '.h'
            else: ext = '.cpp'

            ## Populate the variables
            _populate_header_impl_vars(out_f.with_suffix(ext), f_txt)

            ## Generate file
            _gen_header_implementation(ft, out_f)
        case "interface":
            ## Populate variables
            _populate_header_impl_vars(out_f.with_suffix('.h'), f_txt)

            ## Generate file
            _replace_txt(out_f.with_suffix('.h'), f_txt)
        case "test":
            ## Populate variables
            _populate_header_impl_vars(out_f.with_suffix('.cpp'), f_txt)

            ## If the name is not formatted correctly
            if 'test_' not in str(out_f):
                out_f = out_f.parent / Path('test_' + out_f.name).with_suffix('.cpp')
            ## Generate file
            _replace_txt(out_f, f_txt)
        case _:
            ## Populate variables
            _populate_header_impl_vars(out_f, f_txt)

            ## Generate file
            _replace_txt(out_f, f_txt)
            return

    return

################################################################################
# GENERATION FUNCTIONS
################################################################################

##==============================================================================
#
def _gen_header_implementation(ft: str, out_f: Path):
    """!
    @brief Logic to determine whether to generate header and/or implementation
    files.

    @param ft Path to filetype
    @param out_f Output file path
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
    if bool_header:
        _FILE_TYPE = 'definition'
        ft = Path(ft).parent / 'header.skel'
        f_txt = _get_file_text(ft)
        _replace_txt(out_f.with_suffix('.h'), f_txt)
    ## If the implementation is to be generated
    if bool_implementation:
        _FILE_TYPE = 'implementation'
        ft = Path(ft).parent / 'implementation.skel'
        f_txt = _get_file_text(ft)
        _replace_txt(out_f.with_suffix('.cpp'), f_txt)
    return

################################################################################
# HELPER FUNCTIONS
################################################################################
##==============================================================================
#
def _populate_header_impl_vars(out_f: Path, f_txt: str):
    """!
    @brief Populate the required variables for header/implementation files

    @param out_f Output file path
    @param f_txt File text
    """
    global _NAMESPACE
    global _CLASS_NAME
    global _CLASS_TESTED
    global _HEADER_GUARD
    global _FILE_PATH
    global _FILE_TYPE

    if not _NAMESPACE and '${NAMESPACE_BEGIN}' in f_txt: _NAMESPACE = input('Namespace [None]: ')
    if not _NAMESPACE: _NAMESPACE = 'IGNORE'

    if not _CLASS_NAME and '${CLASS_NAME}' in f_txt: _CLASS_NAME = input(f'Class Name [{out_f.stem}]: ')
    if not _CLASS_NAME or _CLASS_NAME.isspace(): _CLASS_NAME = out_f.stem

    if not _CLASS_TESTED and '${CLASS_TESTED}' in f_txt: _CLASS_TESTED = input(f'Class being tested: ')
    if not _CLASS_TESTED or _CLASS_TESTED.isspace(): _CLASS_TESTED = out_f.stem

    _HEADER_GUARD = "_" + out_f.stem.upper() + "_H_"
    _FILE_PATH = out_f.stem.lower()
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
    if not _NAMESPACE or _NAMESPACE.isspace() or _NAMESPACE == 'IGNORE':
        f_txt = f_txt.replace('${NAMESPACE_BEGIN}\n\n', '')
        f_txt = f_txt.replace('${NAMESPACE_END}\n\n', '')
    # Include namespace
    else:
        f_txt = f_txt.replace('${NAMESPACE_BEGIN}', f'namespace {_NAMESPACE}\n{{')
        f_txt = f_txt.replace('${NAMESPACE_END}', '}')

    f_txt = Template(f_txt).substitute(
            HEADER_GUARD=_HEADER_GUARD,
            CLASS_NAME=_CLASS_NAME,
            CLASS_TESTED=_CLASS_TESTED,
            FILE_PATH=_FILE_PATH,
            FILE_TYPE=_FILE_TYPE,
            METHOD_SEPARATOR=method_separator(f_txt, indent=2)
            )

    # Write text to disk
    with open(out_f, 'a') as f: f.write(f_txt)
    return f_txt

##==============================================================================
#
def _get_file_text(ft: str):
    with open(ft, 'r') as f:
        return f.read()
