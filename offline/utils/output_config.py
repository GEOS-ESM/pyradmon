import shutil
import logging
from pathlib import Path
from typing import Optional, Union


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent

RUN_ROOT = REPO_ROOT / 'offline' / 'run'


class PyRadmonOutputManager:
    @staticmethod
    def resolve_output_dir(
        component: str,
        expid: str,
        date_tag: str,
        run_root: Optional[Union[str, Path]] = None
    ) -> Path:

        base = Path(run_root) if run_root is not None else RUN_ROOT
        return base / component / expid / date_tag

    @staticmethod
    def move_output(
        source: Union[str, Path],
        component: str,
        expid: str,
        date_tag: str,
        run_root: Optional[Union[str, Path]] = None,
        logger: Optional[logging.Logger] = None
    ) -> Path:

        log = logger or logging.getLogger('pyradmon')
        source = Path(source)

        if not source.exists():
            raise FileNotFoundError(f"Source path does not exist: {source}")

        destination = PyRadmonOutputManager.resolve_output_dir(
            component=component,
            expid=expid,
            date_tag=date_tag,
            run_root=run_root
        )

        destination.parent.mkdir(parents=True, exist_ok=True)

        if destination.exists():
            log.warning(f'Destination {destination} already exists')
            n = 1
            while (destination.parent / f'{date_tag}_rerun{n}').exists():
                n += 1
            destination = destination.parent / f'{date_tag}_rerun{n}'

        shutil.move(str(source), str(destination))
        log.info(f'Output moved to: {destination}')

        return destination


def resolve_output_dir(
    component: str,
    expid: str,
    date_tag: str,
    run_root: Optional[Union[str, Path]] = None
) -> Path:
    return PyRadmonOutputManager.resolve_output_dir(
        component=component,
        expid=expid,
        date_tag=date_tag,
        run_root=run_root
    )


def move_output(
    source: Union[str, Path],
    component: str,
    expid: str,
    date_tag: str,
    run_root: Optional[Union[str, Path]] = None,
    logger: Optional[logging.Logger] = None
) -> Path:
    return PyRadmonOutputManager.move_output(
        source=source,
        component=component,
        expid=expid,
        date_tag=date_tag,
        run_root=run_root,
        logger=logger
    )
