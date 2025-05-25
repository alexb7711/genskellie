import logging
import argparse
import os
import platform
from logging import CRITICAL, DEBUG, WARNING, INFO
from pathlib import Path
import warnings

from .langs import *

logger = logging.getLogger(__file__)

################################################################################

class Skellie:
    from .langs.file_types import SUPPORTED_FILE_TYPES

    ############################################################################
    # CONSTANTS
    ############################################################################
    DEFAULT_CONFIGURATION_PATH = Path(os.path.dirname(os.path.abspath(__file__))) / Path(
        "config/"
    )

    # Select configuration directory location based on the operating system
    PROGRAM = "genkellie"
    CONF_DIR = Path(f".config/{PROGRAM}")

    if platform.system() == "Windows":
        CONF_DIR = Path(f"AppData/Local/Programs/{PROGRAM}")

    CONFIG_DIR = Path(f"{Path.home()}/{CONF_DIR}")

    ##==========================================================================
    #
    def __init__(self,
                 std_output: bool = False,
                 config_path: Path = None,
                 output_file = None,
                 language: str = None,
                 file_type: str = None):
        """!
        @brief Initialize the skellie class

        @param std_output Output text to the console
        @param config_path Configuration directory path
        @param output_file File to output the skeleton to
        @param language Language type
        @param file_type Type of file to generate
        """
        self.cpath = Path(config_path) if config_path != None else Path(Skellie.DEFAULT_CONFIGURATION_PATH)
        self.out_f = output_file
        self.lang = language
        self.ft = file_type
        return

    ##==========================================================================
    #
    def __call__(self) -> bool:
        """
        @brief Run the genskellie program

        @return
        True if file was generated, false otherwise
        """
        # If the language was not define, prompt for the language
        self.lang = self._prompt_item("language", self.out_f, self.cpath)

        if not self.lang:
            import sys
            logger.error("Unable to identify the language!")
            sys.exit(1)

        # If the file type was not define, prompt for the file to be generated
        self.cpath = self.cpath / self.lang
        self.ft = self.cpath / Path(self._prompt_item("file_type", self.ft, self.cpath)).with_suffix('.skel')

        # If a language or a file type was not select, exit early
        if not self.lang or not self.ft:
            return False

        # Generate the file
        self._gen_file()
        return True

    ##==========================================================================
    #
    def _prompt_item(self, item: str, selection, path: Path) -> str:
        """!
        @brief
        Either prompt a list of supported items if one was not provided
        or check if the given item is valid.

        @param item What to search for
        @param selection Item chosen by the user
        @param path Path to the base directory of the configuration directory

        @return
        Return None if the item does not match, or a string of name of item to
        be used.
        """
        # List the item and sort them
        if item == "language":
            ## Generate list of supported languages
            found_items = sorted([ x.name for x in path.iterdir() if x.is_dir() ])

            ## Try to identify the language
            for x in self.SUPPORTED_FILE_TYPES:
                if x[0] == selection.suffix:
                    logger.info(f'Language: {x[1]}')
                    selection = x[1]
                    break

            ## Determine if a selection was made
            if selection not in found_items:
                selection = None
        elif item == "file_type":
            ## Generate list of supported file types
            found_items = sorted([ x.stem for x in path.iterdir() if x.is_file() ])
            if selection in found_items:
                    logger.info(f'File Type: {selection}')
            else:
                selection = None
        else:
            return None

        # Attempt to automatically determine the item

        # If the item was not specified
        if not selection:
            ## Print out the found items
            for i, x in enumerate(found_items):
                print(f"{i}: {x}")

            ## Prompt for the selection of the item
            while True:
                ### Calculate the number of elements
                length = len(found_items)-1

                ### If there are no items in the list, return early
                if length < 0:
                    print("ERROR: No items found in directory! Exiting...")
                    return None

                ### Prompt the user to select an item
                idx = input(f"Select item (0-{length}): ")

                ### Check if the selection provided was valid
                if (idx.isdigit() and
                    int(idx) >= 0 and int(idx) < len(found_items)):
                    selection = found_items[int(idx)]
                    break
                else:
                    print("Invalid entry...")

        # Otherwise check whether the item is in the list
        elif selection not in found_items:
            selection = None

        return selection

    ##==========================================================================
    #
    def _gen_file(self) -> str:
        """!
        @brief
        Generate the output of the desired text item

        @returns
        String of the text
        """
        match self.lang.lower():
            case "python":
                gen_python.run(self.out_f, self.ft)
            case "c":
                gen_c.run(self.out_f, self.ft)
        return

################################################################################


##==============================================================================
#
def parse_options(args=None, values=None):
    """
    Define and parse `argparse` options for command-line usage.
    """

    # Program description and use
    usage = """%(prog)s [options] [FILE PATH] [FILE TYPE]"""
    desc = (
        "Generate file skeletons quickly, easily, and dynamically."
    )
    # Optional flags
    parser = argparse.ArgumentParser(prog="GenSkellie", usage=usage, description=desc)
    parser.add_argument(
        "-s", "--std",
        dest="std_output",
        default=False,
        help="Print the output to the terminal.",
    )
    parser.add_argument(
        "-c", "--config",
        dest="config_path",
        default=None,
        help="Select another configuration file directory location.",
    )
    parser.add_argument(
        "-l", "--language",
        dest="language",
        default=None,
        help="Select the language type to output.",
    )
    parser.add_argument(
        "-t", "--file_type",
        dest="file_type",
        default=None,
        help="Select the type of file output.",
    )
    parser.add_argument(
        "output_file", nargs=1,
        default='.',
        help="File to output text into.",
    )
    parser.add_argument(
        "file_type", nargs=1,
        default=None,
        help="Type of file to output.",
    )

    # Parse the input arguments
    options = parser.parse_args(args, values)

    # Update the path to be a Path object
    if options.output_file:
        options.output_file = Path(str(options.output_file[0])).absolute()
        options.file_type = options.file_type[0]

    # Save the options
    return vars(options)


##======================================================================================================================
#
def run():
    """Run genskellie from the command line."""
    import sys

    # Parse options and adjust logging level if necessary
    options = parse_options()

    # If options is empty
    if not options:
        sys.exit(2)

    # Set the logging level
    logger.setLevel(INFO)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

    if logging.root.level <= WARNING:
        # Ensure deprecation warnings get displayed
        warnings.filterwarnings("default")
        logging.captureWarnings(True)
        warn_logger = logging.getLogger("py.warnings")
        warn_logger.addHandler(console_handler)

    # Run `genskellie`
    s = Skellie(**options)
    s()
    return


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    run()
