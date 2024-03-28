import os
import subprocess
import tempfile
import shutil
import logging
from enum import Enum
from pathlib import Path


logger = logging.getLogger("scanline_wrapper")


class PageSize(Enum):
    """Page size."""

    A4 = "-a4"
    LEGAL = "-legal"
    LETTER = "-letter"


class FileFormat(Enum):
    """Output file format."""

    AUTO = -1
    PDF = None
    TIFF = "-tiff"
    JPEG = "-jpeg"


class Color(Enum):
    """Color or monochrome output."""

    COLOR = None
    MONOCHROME = "-mono"


class ScanlineException(Exception):
    """Base class for Scanline exceptions."""


class ScanlineUnknownError(ScanlineException):
    pass


class ScanlineExecutableNotFound(ScanlineException):
    pass


class ScanlineScannerNotFound(ScanlineException):
    pass


class ScanlineInvalidPageSize(ScanlineException):
    pass


class ScanlineInvalidFileFormat(ScanlineException):
    pass


class ScanlineInvalidColor(ScanlineException):
    pass


_FILE_EXT_TO_FORMAT = {
    ".pdf": FileFormat.PDF,
    ".tif": FileFormat.TIFF,
    ".tiff": FileFormat.TIFF,
    ".jpg": FileFormat.JPEG,
    ".jpeg": FileFormat.JPEG,
}


_FORMAT_TO_FILE_EXT = {
    FileFormat.PDF: ".pdf",
    FileFormat.TIFF: ".tif",
    FileFormat.JPEG: ".jpg",
}


def _get_scanline_cmd():
    """Get the scanline command name or path.

    This can be overided by the ``SCANLINE_CMD`` environment variable.

    :rtype: str
    """
    return os.environ.get("SCANLINE_CMD", "scanline")


def _is_scanline_available():
    """Checks if the scanline command is available.

    :rtype: bool
    """
    cmd = _get_scanline_cmd()
    if os.path.isfile(cmd) and os.access(cmd, os.X_OK):
        return True
    if "PATH" in os.environ:
        for path in os.environ["PATH"].split(":"):
            cmd_path = os.path.join(path, cmd)
            if os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
                return True
    return False


def list_scanners(browsesecs=1, verbose=False):
    """Get a list of available scanners.

    Example:

    >>> import scanline_wrapper
    >>> scanline_wrapper.list_scanners()
    ... ['HP Color LaserJet MFP M281fdw (035F4A)', 'My other scanner']

    :param int browsesecs: Specify how long to wait when searching for scanners
        (in seconds, default: ``1``).
    :param bool verbose: Increase verbosity of scanline logs (default: ``False``).

    :raise ScanlineExecutableNotFound: if the scanline app is not installed.
    :raise subprocess.CalledProcessError: if something goes wrong while running
        the scanline command.

    :rtype: list(str)
    :returns: the available scanners.
    """
    if verbose:
        logging.basicConfig(level=logging.INFO)

    if not _is_scanline_available():
        raise ScanlineExecutableNotFound(
            "The scanline command was not found. Is scanline installed?"
        )

    command = [_get_scanline_cmd()]
    command += ["-list"]
    command += ["-browsesecs", str(browsesecs)]
    if verbose:
        command += ["-verbose"]

    logger.info("Running command: %s" % " ".join(command))
    proc = subprocess.run(command, check=True, capture_output=True)
    logger.info(proc.stdout.decode("UTF-8", errors="ignore"))

    scanners = []

    for line in proc.stdout.decode("UTF-8", errors="ignore").split("\n"):
        if line.startswith("* "):
            scanners.append(line[2:])

    return scanners


def scan_flatbed(
    output_path,
    scanner=None,
    is_scanner_exact_name=False,
    page_size=PageSize.A4,
    file_format=FileFormat.AUTO,
    color=Color.COLOR,
    resolution=150,
    browsesecs=1,
    verbose=False,
):
    """Scans a document using the flatbed unit of the scanner.

    Simple example:

    >>> import scanline_wrapper
    >>> scanline_wrapper.scan_flatbed("./out.tiff")

    More complete example:

    >>> import scanline_wrapper
    >>> scanline_wrapper.scan_flatbed(
    >>>     "./out.jpg",
    >>>     scanner="HP Color LaserJet MFP M281fdw (035F4A)",
    >>>     page_size=scanline_wrapper.PageSize.LETTER,        # A4, LEGAL or LETTER
    >>>     file_format=scanline_wrapper.FileFormat.JPEG,      # AUTO, PDF, TIFF or JPEG
    >>>     color=scanline_wrapper.Color.COLOR,                # COLOR or MONOCHROME
    >>>     resolution=150,                                    # DPI
    >>> )

    :param str,pathlib.Path output_path: The output file path.
    :param str scanner: The name of the scanner to use. If not provided, the
        first available scanner will be used (default: ``None``).
    :param bool is_scanner_exact_name: If set to ``True``, scanline will try to
        fuzzy-match the scanner name (default: ``False``).
    :param PageSize page_size: The size of the page to scan (default.
        ``PageSize.A4``).
    :param FileFormat file_format: The output file format. If set to
        ``FileFormat.AUTO`` the format will be infered from the file extension.
        A ``ValueError`` will be raised if the file extension does not match a
        supported format. (default: ``FileFormat.AUTO``).
    :param Color color: Select color or monochrome scan (default:
        ``Color.COLOR``).
    :param int resolution: Specify minimum resolution at which to scan (in dpi,
        default: ``150``).
    :param int browsesecs: Specify how long to wait when searching for scanners
        (in seconds, default: ``1``).
    :param bool verbose: Increase verbosity of scanline logs (default: ``False``).

    :raise ScanlineScannerNotFound: if the scanner requested in ``scanner``
        cannot be found or if no scanner are found.
    :raise ScanlineInvalidPageSize: if the given page size is not one from the
        :py:class:`~PageSize` enum.
    :raise ScanlineInvalidFileFormat: if the given file_format is not one from the
        :py:class:`~FileFormat` or if the file extension is not recognized when
        file format is set to :py:attr:`FileFormat.AUTO`.
    :raise ScanlineInvalidColor: if the given page color is not one from the
        :py:class:`~Color` enum.
    :raise ScanlineExecutableNotFound: if the scanline app is not installed.
    :raise ScanlineUnknownError: if scanline has not generated the expected
        output file without returning a specific error.
    :raise subprocess.CalledProcessError: if something goes wrong while running
        the scanline command.

    :rtype: None
    """
    if not _is_scanline_available():
        raise ScanlineExecutableNotFound(
            "The scanline command was not found. Is scanline installed?"
        )

    if verbose:
        logging.basicConfig(level=logging.INFO)

    # Normalize path
    output_path = Path(output_path).absolute()

    command = [_get_scanline_cmd()]
    command += ["-flatbed"]

    # Scanner selection
    if scanner:
        command += ["-scanner", scanner]
        if is_scanner_exact_name:
            command += ["-exactname"]

    # Page Size
    if type(page_size) is PageSize:
        command += [page_size.value]
    elif page_size in [item.value for item in PageSize]:
        command += [page_size]
    else:
        raise ScanlineInvalidPageSize("Invalid page size: %s." % str(page_size))

    # File Format
    if type(file_format) is not FileFormat:
        if file_format in [item.value for item in FileFormat]:
            file_format = FileFormat(file_format)
        else:
            raise ScanlineInvalidFileFormat(
                "Invalid file format: %s." % str(file_format)
            )

    if file_format == FileFormat.AUTO:
        if output_path.suffix.lower() in _FILE_EXT_TO_FORMAT:
            file_format = _FILE_EXT_TO_FORMAT[output_path.suffix.lower()]
        else:
            raise ScanlineInvalidFileFormat(
                "Auto file format: unsupported file extension: %s"
                % str(output_path.suffix)
            )

    if file_format.value:  # PDF == None (default behaviour, no argument)
        command += [file_format.value]

    # Color
    if type(color) is Color:
        if color.value:
            command += [color.value]
    elif color in [item.value for item in Color]:
        if color:
            command += [color]
    else:
        raise ScanlineInvalidColor("Invalid color: %s." % str(color))

    # Resolution
    command += ["-resolution", str(resolution)]

    # Browse wait time
    command += ["-browsesecs", str(browsesecs)]

    # Verbose
    if verbose:
        command += ["-verbose"]

    with tempfile.TemporaryDirectory(prefix="scanline_wrapper_") as tmp_dir:
        # Output file
        tmp_output_path = (Path(tmp_dir) / "scan").with_suffix(
            _FORMAT_TO_FILE_EXT[file_format]
        )

        command += ["-dir", tmp_output_path.parent.as_posix()]
        command += ["-name", tmp_output_path.with_suffix("").name]

        # Call scanline
        logger.info("Running command: %s" % " ".join(command))
        proc = subprocess.run(command, check=True, capture_output=True)
        logger.info(proc.stdout.decode("UTF-8", errors="ignore"))

        for line in proc.stdout.decode("UTF-8", errors="ignore").split("\n"):
            if line == "No scanner was found.":
                raise ScanlineScannerNotFound("No scanner was found.")

        # Check output file was created
        if not tmp_output_path.exists():
            raise ScanlineUnknownError(
                "Expected output file was not generated by scanline."
            )

        # Move output file to its final destination
        if output_path != tmp_output_path:
            shutil.move(tmp_output_path, output_path)
