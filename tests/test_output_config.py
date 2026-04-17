"""Tests for the centralized output manager system."""

import pytest
import shutil
import tempfile
from pathlib import Path
import sys

# Add path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'offline'))
from utils.output_config import resolve_output_dir, move_output, PyRadmonOutputManager


class TestResolveOutputDir:
    """Tests for resolve_output_dir."""

    def test_returns_path_object(self):
        result = resolve_output_dir('spatial', 'f5295_fp', '20240101')
        assert isinstance(result, Path)

    def test_path_contains_component(self):
        result = resolve_output_dir('spatial', 'f5295_fp', '20240101')
        assert 'spatial' in result.parts

    def test_path_contains_expid(self):
        result = resolve_output_dir('spatial', 'f5295_fp', '20240101')
        assert 'f5295_fp' in result.parts

    def test_path_contains_date_tag(self):
        result = resolve_output_dir('spatial', 'f5295_fp', '20240101')
        assert '20240101' in result.parts

    def test_component_before_expid_before_date(self):
        """Verify canonical order: run/<component>/<expid>/<date_tag>"""
        result = resolve_output_dir('spatial', 'myexp', '20240101')
        parts = result.parts
        idx_component = parts.index('spatial')
        idx_expid = parts.index('myexp')
        idx_date = parts.index('20240101')
        assert idx_component < idx_expid < idx_date

    def test_run_root_override(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = resolve_output_dir('spatial', 'myexp', '20240101', run_root=tmpdir)
            assert result == Path(tmpdir) / 'spatial' / 'myexp' / '20240101'

    def test_timeseries_component(self):
        result = resolve_output_dir('timeseries', 'f5295_fp', '20240115')
        assert 'timeseries' in result.parts
        assert 'f5295_fp' in result.parts
        assert '20240115' in result.parts


class TestMoveOutput:
    """Tests for move_output."""

    def test_moves_directory_to_correct_location(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir) / 'run'
            source = Path(tmpdir) / '20240101'
            source.mkdir()
            (source / 'output.txt').write_text('data')

            dest = move_output(
                source=source,
                component='spatial',
                expid='myexp',
                date_tag='20240101',
                run_root=run_root
            )

            assert dest == run_root / 'spatial' / 'myexp' / '20240101'
            assert dest.exists()
            assert (dest / 'output.txt').read_text() == 'data'

    def test_source_is_removed_after_move(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir) / 'run'
            source = Path(tmpdir) / '20240101'
            source.mkdir()

            move_output(
                source=source,
                component='spatial',
                expid='myexp',
                date_tag='20240101',
                run_root=run_root
            )

            assert not source.exists()

    def test_creates_parent_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir) / 'deeply' / 'nested' / 'run'
            source = Path(tmpdir) / 'source_dir'
            source.mkdir()

            move_output(
                source=source,
                component='spatial',
                expid='myexp',
                date_tag='20240101',
                run_root=run_root
            )

            assert (run_root / 'spatial' / 'myexp' / '20240101').exists()

    def test_returns_destination_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir) / 'run'
            source = Path(tmpdir) / '20240101'
            source.mkdir()

            result = move_output(
                source=source,
                component='spatial',
                expid='myexp',
                date_tag='20240101',
                run_root=run_root
            )

            assert isinstance(result, Path)
            assert result.exists()

    def test_collision_appends_rerun1(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir) / 'run'

            # Pre-create the destination so collision occurs
            existing = run_root / 'spatial' / 'myexp' / '20240101'
            existing.mkdir(parents=True)

            source = Path(tmpdir) / '20240101'
            source.mkdir()

            dest = move_output(
                source=source,
                component='spatial',
                expid='myexp',
                date_tag='20240101',
                run_root=run_root
            )

            assert dest == run_root / 'spatial' / 'myexp' / '20240101_rerun1'
            assert dest.exists()

    def test_collision_increments_rerun_suffix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir) / 'run'
            base = run_root / 'spatial' / 'myexp'

            # Pre-create original and first rerun
            (base / '20240101').mkdir(parents=True)
            (base / '20240101_rerun1').mkdir(parents=True)

            source = Path(tmpdir) / '20240101'
            source.mkdir()

            dest = move_output(
                source=source,
                component='spatial',
                expid='myexp',
                date_tag='20240101',
                run_root=run_root
            )

            assert dest == run_root / 'spatial' / 'myexp' / '20240101_rerun2'

    def test_raises_if_source_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir) / 'run'
            nonexistent = Path(tmpdir) / 'does_not_exist'

            with pytest.raises(FileNotFoundError):
                move_output(
                    source=nonexistent,
                    component='spatial',
                    expid='myexp',
                    date_tag='20240101',
                    run_root=run_root
                )

    def test_accepts_string_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir) / 'run'
            source = Path(tmpdir) / '20240101'
            source.mkdir()

            dest = move_output(
                source=str(source),
                component='spatial',
                expid='myexp',
                date_tag='20240101',
                run_root=run_root
            )

            assert dest.exists()


class TestPyRadmonOutputManager:
    """Tests for PyRadmonOutputManager class directly."""

    def test_resolve_output_dir_class_method(self):
        result = PyRadmonOutputManager.resolve_output_dir('spatial', 'exp1', '20240101')
        assert isinstance(result, Path)
        assert result.name == '20240101'

    def test_move_output_class_method(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_root = Path(tmpdir) / 'run'
            source = Path(tmpdir) / '20240101'
            source.mkdir()

            dest = PyRadmonOutputManager.move_output(
                source=source,
                component='timeseries',
                expid='m21c',
                date_tag='20240101',
                run_root=run_root
            )

            assert dest == run_root / 'timeseries' / 'm21c' / '20240101'
