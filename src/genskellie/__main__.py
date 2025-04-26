import logging
import argparse
from logging import CRITICAL, DEBUG, WARNING
from pathlib import Path

import warnings

import genskellie

logger = logging.getLogger(__file__)

########################################################################################################################


##======================================================================================================================
#
def parse_options(args=None, values=None):
    """
    Define and parse `argparse` options for command-line usage.
    """

    # Program description and use
    usage = """%prog [options] [FILE PATH]"""
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

    # Parse the input arguments
    options = parser.parse_args(args, values)

    # Save the options
    return options


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
    logger.setLevel(WARNING)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

    if logging.root.level <= WARNING:
        # Ensure deprecation warnings get displayed
        warnings.filterwarnings("default")
        logging.captureWarnings(True)
        warn_logger = logging.getLogger("py.warnings")
        warn_logger.addHandler(console_handler)

    # Run `genskellie`
    # genskellie.genskellie(options)
    print("RUNNING!")
    return


########################################################################################################################

if __name__ == "__main__":  # pragma: no cover
    # Support running module as a command line command.
    #     python -m markdown [options] [args]
    run()
