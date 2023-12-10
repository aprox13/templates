"""Containers module."""
import pkgutil
from pathlib import Path

from dependency_injector import containers, providers

from services.notes import Notes
from loggers import get_logger

logger = get_logger("app-dependencies")


def _collect_all_submodules(work_dir: Path, root: Path):
    base_relative = root.relative_to(work_dir)
    logger.info(f"Resolving all modules in {base_relative}")

    def sub_dirs(root_path: Path):
        if root_path.is_dir():
            yield root_path
            for x in root_path.iterdir():
                for elem in sub_dirs(x):
                    yield elem

    def prefix(directory):
        res = str(directory.relative_to(work_dir))
        if res.endswith("/"):
            res = res[:-1]
        res = res.replace("/", ".") + "."
        return res

    modules = []
    for dir_ in sub_dirs(root):
        for m in pkgutil.iter_modules(path=[dir_], prefix=prefix(dir_)):
            modules.append(m.name)
    return modules


def wirein(*paths):
    work_dir = Path(".").resolve().absolute()
    result = []

    for p in paths:
        result.extend(_collect_all_submodules(work_dir, Path(p).resolve().absolute()))

    logger.info(f"Collected {len(result)} submodules")
    for m in result:
        logger.info(f"Collected module: {m}")

    def _inner(cls):
        cls.wiring_config = containers.WiringConfiguration(modules=result)
        return cls

    return _inner


@wirein("api")
class AppDependencies(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])

    notes = providers.Singleton(Notes)
