import io
import logging
import numbers
import traceback
from contextlib import closing
from types import TracebackType
from typing import Dict, List, Tuple, Type, cast

ExcInfo = Tuple[Type[BaseException], BaseException, TracebackType]

# Reserved log record attributes cannot be overwritten. They
# will not included in the formatted log.
#
# https://docs.python.org/3/library/logging.html#logrecord-attributes
RESERVED: Tuple[str, ...] = (
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "message",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
)


class Logfmter(logging.Formatter):
    @classmethod
    def format_string(cls, value: str) -> str:
        """
        Process the provided string with any necessary quoting and/or escaping.
        """
        needs_dquote_escaping = '"' in value
        needs_newline_escaping = "\n" in value
        needs_quoting = " " in value or "=" in value

        if needs_dquote_escaping:
            value = value.replace('"', '\\"')

        if needs_newline_escaping:
            value = value.replace("\n", "\\n")

        if needs_quoting:
            value = '"{}"'.format(value)

        return value if value else '""'

    @classmethod
    def format_value(cls, value) -> str:
        """
        Map the provided value to the proper logfmt formatted string.
        """
        if value is None:
            return ""
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, numbers.Number):
            return str(value)

        return cls.format_string(str(value))

    @classmethod
    def format_exc_info(cls, exc_info: ExcInfo) -> str:
        """
        Format the provided exc_info into a logfmt formatted string.

        This function should only be used to format exceptions which are
        currently being handled. Not with those exceptions which are
        manually passed into the logger. For example:

            try:
                raise Exception()
            except Exception:
                logging.exception()
        """
        _type, exc, tb = exc_info

        with closing(io.StringIO()) as sio:
            traceback.print_exception(_type, exc, tb, None, sio)
            value = sio.getvalue()

        # Tracebacks have a single trailing newline that we don't need.
        value = value.rstrip("\n")

        return cls.format_string(value)

    @classmethod
    def format_params(cls, params: dict) -> str:
        """
        Return a string representing the logfmt formatted parameters.
        """
        return " ".join(
            [
                "{}={}".format(key, cls.format_value(value))
                for key, value in params.items()
            ]
        )

    @classmethod
    def get_extra(cls, record: logging.LogRecord) -> dict:
        """
        Return a dictionary of logger extra parameters by filtering any reserved keys.
        """
        return {
            key: value for key, value in record.__dict__.items() if key not in RESERVED
        }

    def __init__(
        self,
        keys: List[str] = ["at"],
        mapping: Dict[str, str] = {"at": "levelname"},
        datefmt: str = None,
    ):
        self.keys = keys
        self.mapping = mapping
        self.datefmt = datefmt

    def format(self, record: logging.LogRecord) -> str:
        # If the 'asctime' attribute will be used, then generate it.
        if "asctime" in self.keys or "asctime" in self.mapping.values():
            record.asctime = self.formatTime(record, self.datefmt)

        if isinstance(record.msg, dict):
            params = record.msg
        else:
            extra = self.get_extra(record)
            params = {"msg": record.getMessage(), **extra}

        tokens = []

        # Add the initial tokens from the provided list of default keys.
        #
        # This supports parameters which should be included in every log message. The
        # values for these keys must already exist on the log record. If they are
        # available under a different attribute name, then the formatter's mapping will
        # be used to lookup these attributes. e.g. 'at' from 'levelname'
        for key in self.keys:

            attribute = key

            # If there is a mapping for this key's attribute, then use it to lookup
            # the key's value.
            if key in self.mapping:
                attribute = self.mapping[key]

            # If the attribute doesn't exist on the log record, then skip it.
            if not hasattr(record, attribute):
                continue

            value = getattr(record, attribute)

            tokens.append("{}={}".format(key, self.format_value(value)))

        formatted_params = self.format_params(params)
        if formatted_params:
            tokens.append(formatted_params)

        if record.exc_info:
            # Cast exc_info to its not null variant to make mypy happy.
            exc_info = cast(ExcInfo, record.exc_info)

            tokens.append("exc_info={}".format(self.format_exc_info(exc_info)))

        return " ".join(tokens)
