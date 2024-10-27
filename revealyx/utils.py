import logging


class LogOutputFmt(logging.Formatter):
    GREY = ""
    BLUE = ""
    MAGENTA = ""
    YELLOW = ""
    RED = ""
    BOLD_RED = ""
    RESET = ""
    FORMATS = {
        "DEFAULT": GREY + "[+] %(message)s" + RESET,
        logging.DEBUG: MAGENTA + "[*] %(module)s [%(lineno)d]: %(message)s" + RESET,
        logging.INFO: GREY + "[+] %(message)s" + RESET,
        logging.WARNING: YELLOW + "[!] %(levelname)s: %(message)s" + RESET,
        logging.ERROR: RED + "[X] %(message)s" + RESET,
        logging.CRITICAL: BOLD_RED + "[!?] %(message)s" + RESET,
    }

    def format(self, record):
        format_orig = self._style._fmt

        self._style._fmt = self.FORMATS.get(record.levelno, self.FORMATS["DEFAULT"])
        result = logging.Formatter.format(self, record)

        self._style._fmt = format_orig

        return result
