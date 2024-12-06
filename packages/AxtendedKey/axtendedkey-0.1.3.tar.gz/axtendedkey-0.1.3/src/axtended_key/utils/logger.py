
class Logger:
    """
    Logger
    Simple log extension to manage --verbose behavior
    """
    def __init__(self):
        self.verbose = False

    def set_verbose(self, verbose):
        self.verbose = verbose

    def log(self, message):
        if self.verbose:
            print(message)


# Create a shared logger instance
logger = Logger()
