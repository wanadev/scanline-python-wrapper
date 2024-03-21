from enum import Enum


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


class ScanlineUnknownError(Exception):
    pass


class ScanlineScannerNotFound(Exception):
    pass


class ScanlineNotAvailable(Exception):
    pass


_FILE_EXT_TO_FORMAT = {
    ".pdf": FileFormat.PDF,
    ".tif": FileFormat.TIFF,
    ".tiff": FileFormat.TIFF,
    ".jpg": FileFormat.JPEG,
    ".jpeg": FileFormat.JPEG,
}


def _check_scanline_available():
    raise NotImplementedError()  # TODO


def list_scanners(browsesecs=1, verbose=False):
    """Get a list of available scanners.

    :param int browsesecs: Specify how long to wait when searching for scanners
        (in seconds, default: ``1``).
    :param bool verbose: Increase verbosity of scanline logs (default: ``False``).

    :rtype: list(str)
    :returns: the available scanners.
    """
    raise NotImplementedError()  # TODO


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

    :param str,pathlib.Path output_path: The output file path.
    :param str scanner: The name of the scanner to use. If not provided, the
        first available scanner will be used (default: ``None``).
    :parma bool is_scanner_exact_name: If set to ``True``, scanline will try to
        fuzzy-match the scanner name (default: ``False``).
    :param PageSize page_size: The size of the page to scan (default.
        ``PageSize.A4``).
    :param FileFormat file_format: The output file format. If set to
    ``FileFormat.AUTO`` the format will be infered from the file extension. A
        ``ValueError`` will be raised if the file extension does not match a
        supported format. (default: ``FileFormat.AUTO``).
    :param Color color: Select color or monochrome scan (default:
        ``Color.COLOR``).
    :param int resolution: Specify minimum resolution at which to scan (in dpi,
        default: ``150``).
    :param int browsesecs: Specify how long to wait when searching for scanners
        (in seconds, default: ``1``).
    :param bool verbose: Increase verbosity of scanline logs (default: ``False``).

    :raise ValueError: if the extension of ``output_path`` does not match any
        supported file format when ``file_format`` is set to ``FileFormat.AUTO``.
    :raise ScanlineScannerNotFound: if the scanner requested in ``scanner``
        cannot be found or if no scanner are found.
    :raise ScanlineUnknownError: if scanline has not generated the expected
        output file without returning a specific error.
    :raise ScanlineNotAvailable: if the scanline app is not installed.

    :rtype: None
    """
    raise NotImplementedError()  # TODO
