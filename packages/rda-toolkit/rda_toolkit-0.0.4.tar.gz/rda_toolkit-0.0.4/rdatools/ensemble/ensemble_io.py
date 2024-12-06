"""
ENSEMBLE I/O
"""

from typing import Any, Optional, List, Dict, Generator, TextIO, TypedDict

import os, sys, contextlib, json, warnings

from datetime import datetime


class Plan(TypedDict):
    _tag_: str
    name: str
    plan: dict[str, str | int]


class Metadata(TypedDict):
    _tag_: str
    properties: dict[str, Any]


@contextlib.contextmanager
def smart_write(
    filename: Optional[str] = None,
) -> Generator[TextIO | TextIO, None, None]:
    """Write to a file or stdout.

    Patterned after: https://stackoverflow.com/questions/17602878/how-to-handle-both-with-open-and-sys-stdout-nicely
    """

    if filename and filename != "-":
        fh: TextIO = open(os.path.expanduser(filename), "w")
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


def write_record(record: Any, outstream: TextIO) -> None:
    """
    Write a plan or metadata record as a JSONL "line" to a file

    The indent=None forces the JSON to be written on a single line
    The sort_keys=True sorts the keys alphabetically, which is good for consistency
    """

    json.dump(record, outstream, indent=None, sort_keys=True)
    outstream.write("\n")


@contextlib.contextmanager
def smart_read(
    filename: Optional[str] = None,
) -> Generator[TextIO | TextIO, None, None]:
    """Read from a file or stdin."""

    if filename and filename != "-":
        fh: TextIO = open(os.path.expanduser(filename), "r")
    else:
        fh = sys.stdin

    try:
        yield fh
    finally:
        if fh is not sys.stdin:
            fh.close()


def read_record(line) -> Dict[str, Any]:
    record = json.loads(line.strip())

    return record


def format_scores(
    scores_in: Dict[str, int | float], *, precision="{:.6f}"
) -> Dict[str, int | float]:
    """Format scores to a desired, fixed precision."""

    scores_out: Dict = dict()
    for k, v in scores_in.items():
        if isinstance(v, float):
            scores_out[k] = precision.format(v)
        else:
            scores_out[k] = v

    return scores_out


class WarningCaptureHandler:
    """
    A handler class to capture and redirect warnings to a file stream.
    Maintains a record of captured warnings and provides formatting options.

    [2024-11-02 20:41:46] UserWarning: {message} (File: {path}, Line: {#})

    """

    def __init__(self, output_file: TextIO, include_timestamp: bool = True):
        self.output_file = output_file
        self.include_timestamp = include_timestamp
        self.captured_warnings: List[str] = []

    def __call__(self, message, category, filename, lineno, file=None, line=None):
        warning_message = f"{category.__name__}: {str(message)}"
        # source_info = f" (File: {filename}, Line: {lineno})"
        source_info = ""  # Suppress source info

        if self.include_timestamp:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            warning_message = timestamp + warning_message

        full_message = warning_message + source_info + "\n"
        self.captured_warnings.append(full_message)
        self.output_file.write(full_message)
        self.output_file.flush()


@contextlib.contextmanager
def capture_warnings(output_file: TextIO, include_timestamp: bool = True):
    """
    Context manager for capturing warnings and redirecting them to a file.

    Args:
        output_file: A file-like object to write warnings to
        include_timestamp: Whether to include timestamps in warning messages

    Example:
        with open('warnings.log', 'w') as f:
            with capture_warnings(f):
                # Your code that might generate warnings
                warnings.warn("This is a test warning")
    """
    handler = WarningCaptureHandler(output_file, include_timestamp)
    original_showwarning = warnings.showwarning
    warnings.showwarning = handler

    try:
        yield handler
    finally:
        warnings.showwarning = original_showwarning


### END ###
