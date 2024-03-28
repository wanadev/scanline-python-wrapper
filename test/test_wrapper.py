import subprocess
from pathlib import Path

import pytest

import scanline_wrapper


class Test__get_scanline_cmd:

    def test_default_value(self, monkeypatch):
        monkeypatch.delenv("SCANLINE_CMD", raising=False)
        assert scanline_wrapper._get_scanline_cmd() == "scanline"

    def test_env_overide(self, monkeypatch):
        monkeypatch.setenv("SCANLINE_CMD", "foobar")
        assert scanline_wrapper._get_scanline_cmd() == "foobar"


class Test__is_scanline_available:

    def test_with_command_not_available(self, monkeypatch):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-not-exists").as_posix(),
        )
        assert scanline_wrapper._is_scanline_available() is False

    def test_with_command_path(self, monkeypatch):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-nop.sh").as_posix(),
        )
        assert scanline_wrapper._is_scanline_available() is True

    def test_with_command_in_path(self, monkeypatch):
        monkeypatch.setenv("PATH", (Path(__file__).parent / "mock").as_posix())
        monkeypatch.setenv("SCANLINE_CMD", "scanline-nop.sh")
        assert scanline_wrapper._is_scanline_available() is True


class Test_list_scanner:

    def test_list_scanner_with_2_scanners(self, monkeypatch):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-list-2-scanners.sh").as_posix(),
        )
        scanners = scanline_wrapper.list_scanners()
        assert len(scanners) == 2
        assert scanners[0] == "HP LaserJet MFP M130fw (XXXXXX)"
        assert scanners[1] == "My Other Scanner"

    def test_list_scanner_with_no_scanners(self, monkeypatch):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-list-0-scanners.sh").as_posix(),
        )
        scanners = scanline_wrapper.list_scanners()
        assert len(scanners) == 0

    def test_scanline_not_available(self, monkeypatch):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-not-exists").as_posix(),
        )
        with pytest.raises(scanline_wrapper.ScanlineExecutableNotFound):
            scanline_wrapper.list_scanners()

    def test_scanline_unknown_error(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-cmd-error.sh").as_posix(),
        )
        with pytest.raises(subprocess.CalledProcessError):
            scanline_wrapper.list_scanners()


class Test_scan_flatbed:

    def test_page_size(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-nop.sh").as_posix(),
        )

        scanline_wrapper.scan_flatbed(
            tmp_path / "out.jpg", page_size=scanline_wrapper.PageSize.A4
        )
        scanline_wrapper.scan_flatbed(
            tmp_path / "out.jpg", page_size=scanline_wrapper.PageSize.A4.value
        )
        with pytest.raises(scanline_wrapper.ScanlineInvalidPageSize):
            scanline_wrapper.scan_flatbed(tmp_path / "out.jpg", page_size="foo")

    def test_file_format(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-nop.sh").as_posix(),
        )

        scanline_wrapper.scan_flatbed(
            tmp_path / "out.jpg", file_format=scanline_wrapper.FileFormat.TIFF
        )
        scanline_wrapper.scan_flatbed(
            tmp_path / "out.jpg", file_format=scanline_wrapper.FileFormat.TIFF.value
        )
        scanline_wrapper.scan_flatbed(
            tmp_path / "out.jpg", file_format=scanline_wrapper.FileFormat.PDF
        )
        scanline_wrapper.scan_flatbed(
            tmp_path / "out.jpg", file_format=scanline_wrapper.FileFormat.PDF.value
        )
        with pytest.raises(scanline_wrapper.ScanlineInvalidFileFormat):
            scanline_wrapper.scan_flatbed(tmp_path / "out.jpg", file_format="foo")

    def test_file_format_auto(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-nop.sh").as_posix(),
        )

        scanline_wrapper.scan_flatbed(
            tmp_path / "out.jpg", file_format=scanline_wrapper.FileFormat.AUTO
        )
        with pytest.raises(scanline_wrapper.ScanlineInvalidFileFormat):
            scanline_wrapper.scan_flatbed(
                tmp_path / "out.png", file_format=scanline_wrapper.FileFormat.AUTO
            )

    def test_color(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-nop.sh").as_posix(),
        )

        scanline_wrapper.scan_flatbed(
            tmp_path / "out.jpg", color=scanline_wrapper.Color.MONOCHROME
        )
        scanline_wrapper.scan_flatbed(
            tmp_path / "out.jpg", color=scanline_wrapper.Color.MONOCHROME.value
        )
        with pytest.raises(scanline_wrapper.ScanlineInvalidColor):
            scanline_wrapper.scan_flatbed(tmp_path / "out.jpg", color="foo")

    def test_output_file_is_created(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-nop.sh").as_posix(),
        )

        scanline_wrapper.scan_flatbed(tmp_path / "out.jpeg")
        assert (tmp_path / "out.jpeg").exists()

        scanline_wrapper.scan_flatbed(
            tmp_path / "out.xxx", file_format=scanline_wrapper.FileFormat.TIFF
        )
        assert (tmp_path / "out.xxx").exists()

    def test_scanner_not_found(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-no-scanner.sh").as_posix(),
        )

        with pytest.raises(scanline_wrapper.ScanlineScannerNotFound):
            scanline_wrapper.scan_flatbed(tmp_path / "out.jpg", scanner="XXXXXXXX")

    def test_scanline_not_available(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-not-exists").as_posix(),
        )
        with pytest.raises(scanline_wrapper.ScanlineExecutableNotFound):
            scanline_wrapper.scan_flatbed(tmp_path / "out.jpg")

    def test_scanline_unknown_error(self, monkeypatch, tmp_path):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-cmd-error.sh").as_posix(),
        )
        with pytest.raises(subprocess.CalledProcessError):
            scanline_wrapper.scan_flatbed(tmp_path / "out.jpg")
