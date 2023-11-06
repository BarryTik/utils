import logging
import sys
import argparse

def get_args():
    parser = argparse.ArgumentParser("logging_test")
    log_level = parser.add_mutually_exclusive_group()
    log_level.add_argument(
        "-v", "--verbose", action="store_true",
        help=("Include this flag to set log level to INFO. "
                "Default log level is ERROR.")
    )
    log_level.add_argument(
        "-d", "--debug", action="store_true",
        help=("Include this flag to set log level to DEBUG. "
                "Default log level is ERROR.")
    )
    return parser.parse_args()

def make_logger(args, name):

    # Add new logging level between DEBUG and INFO
    VERBOSE_LEVEL_NUM = 15

    logging.addLevelName(VERBOSE_LEVEL_NUM, "VERBOSE")
    def verbose(self, message, *args, **kws):
        if self.isEnabledFor(VERBOSE_LEVEL_NUM):
            self._log(VERBOSE_LEVEL_NUM, message, args, **kws)
    logging.Logger.verbose = verbose

    # Add new logging level for subprocesses
    logging.addLevelName(VERBOSE_LEVEL_NUM + 1, "SUBPROCESS")
    def subprocess(self, message, *args, **kws):
        if self.isEnabledFor(VERBOSE_LEVEL_NUM + 1):
            self._log(VERBOSE_LEVEL_NUM + 1, message, args, **kws)
    logging.Logger.subprocess = subprocess
    
    log = logging.getLogger(name)

    # Create standard format for log statements
    format = "\n%(name)s %(levelname)s %(asctime)s: %(message)s"
    formatter = logging.Formatter(format)
    subprocess_format = "%(id)s %(asctime)s: %(message)s"
    subprocess_formatter = logging.Formatter(subprocess_format)

    # Set log level based on user input
    if args.verbose:
        level = VERBOSE_LEVEL_NUM
    elif args.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    log.setLevel(level)

    # Redirect INFO and DEBUG to stdout
    handle_out = logging.StreamHandler(sys.stdout)
    handle_out.setLevel(logging.DEBUG)
    handle_out.addFilter(lambda record: record.levelno <= logging.INFO)
    handle_out.addFilter(lambda record: record.levelno != VERBOSE_LEVEL_NUM + 1)
    handle_out.setFormatter(formatter)
    log.addHandler(handle_out)

    handle_subprocess = logging.StreamHandler(sys.stdout)
    handle_subprocess.setLevel(VERBOSE_LEVEL_NUM + 1)
    handle_subprocess.addFilter(lambda record: record.levelno <= VERBOSE_LEVEL_NUM + 1)
    handle_subprocess.setFormatter(subprocess_formatter)
    log.addHandler(handle_subprocess)

    # Redirect WARNING+ to stderr
    handle_err = logging.StreamHandler(sys.stderr)
    handle_err.setLevel(logging.WARNING)
    handle_err.setFormatter(formatter)
    log.addHandler(handle_err)

    return log


def main():
    args = get_args()
    LOGGER = make_logger(args, "Test-Logger")

    LOGGER.debug("DEBUG")
    LOGGER.verbose("VERBOSE")
    LOGGER.subprocess("SUBPROCESS", extra={'id': "FSL"})
    LOGGER.info("INFO")
    LOGGER.error("ERROR")

if __name__ == "__main__":
    main()