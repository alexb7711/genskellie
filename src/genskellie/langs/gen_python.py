from pathlib import Path
from string import Template

from genskellie.gen_util import *

##==============================================================================
# PRIVATE VARIABLES
_CLASS_NAME = None
_FILE_PATH = None

##==============================================================================
#
def run(out_f: Path, ft: str):
    # Get file text
    f_txt = None
    with open(ft, 'r') as f:
        f_txt = f.read()

    match ft.stem:
        case 'class' | 'enum' | 'module' | 'script':
            ## Populate variables
            _populate_header_impl_vars(out_f.with_suffix('.py'), f_txt)

            ## Generate file
            _replace_txt(out_f.with_suffix('.py'), f_txt)
        case 'def':
            pass

################################################################################
# GENERATION FUNCTIONS
################################################################################

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
    global _CLASS_NAME
    global _FILE_PATH

    if not _CLASS_NAME and '${CLASS_NAME}' in f_txt: _CLASS_NAME = input(f'Class Name [{out_f.stem}]: ')
    if not _CLASS_NAME or _CLASS_NAME.isspace(): _CLASS_NAME = out_f.stem

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
    f_txt = Template(f_txt).substitute(
            CLASS_NAME = _CLASS_NAME,
            METHOD_SEPARATOR = method_separator(f_txt, indent_lvl=1, comment='##'),
            SECTION_SEPARATOR = method_separator(f_txt, indent_lvl=1, comment='#', separator='#')
            )

    # Write text to disk
    with open(out_f, 'a') as f: f.write(f_txt)
    return f_txt
