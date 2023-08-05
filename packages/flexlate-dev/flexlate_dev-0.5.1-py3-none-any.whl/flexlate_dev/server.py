import contextlib
import os
import tempfile
import time
from pathlib import Path
from typing import Optional

from flexlate.main import Flexlate
import flexlate.exc as flexlate_exc
from git import Repo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from flexlate.template_data import TemplateData

from flexlate_dev.command_type import CommandType
from flexlate_dev.config import FlexlateDevConfig, load_config, DEFAULT_PROJECT_NAME
from flexlate_dev.project_ops import (
    update_or_initialize_project_get_folder,
)
from flexlate_dev.styles import (
    print_styled,
    INFO_STYLE,
    SUCCESS_STYLE,
)


def serve_template(
    run_config_name: Optional[str] = None,
    template_path: Path = Path("."),
    out_path: Optional[Path] = None,
    no_input: bool = False,
    auto_commit: bool = True,
    config_path: Optional[Path] = None,
    save: bool = False,
):
    config = load_config(config_path)

    with run_server(
        config,
        run_config_name=run_config_name,
        template_path=template_path,
        out_path=out_path,
        no_input=no_input,
        auto_commit=auto_commit,
        save=save,
    ):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            return


@contextlib.contextmanager
def run_server(
    config: FlexlateDevConfig,
    run_config_name: Optional[str] = None,
    template_path: Path = Path("."),
    out_path: Optional[Path] = None,
    no_input: bool = False,
    auto_commit: bool = True,
    save: bool = False,
):
    temp_file: Optional[tempfile.TemporaryDirectory] = None
    if out_path is None:
        temp_file = tempfile.TemporaryDirectory()
        out_path = Path(temp_file.name)
    # setting up inotify and specifying path to watch
    print_styled(
        f"Starting server, watching for changes in {template_path}. Generating output at {out_path}",
        INFO_STYLE,
    )
    observer = Observer()
    event_handler = ServerEventHandler(
        config,
        template_path,
        out_path,
        run_config_name=run_config_name,
        no_input=no_input,
        auto_commit=auto_commit,
        save=save,
    )
    event_handler.sync_output()  # do a sync before starting watcher
    observer.schedule(event_handler, str(template_path), recursive=True)
    observer.start()
    print_styled(
        f"Running auto-reloader, updating {event_handler.out_path} with changes to {template_path}",
        SUCCESS_STYLE,
    )

    yield

    observer.stop()
    observer.join()
    if temp_file is not None:
        temp_file.cleanup()


old = 0.0


class ServerEventHandler(FileSystemEventHandler):
    def __init__(
        self,
        config: FlexlateDevConfig,
        template_path: Path,
        out_root: Path,
        run_config_name: Optional[str] = None,
        no_input: bool = False,
        auto_commit: bool = True,
        save: bool = False,
    ):
        super().__init__()
        self.config = config
        self.run_config_name = run_config_name
        self.run_config = config.get_run_config(CommandType.SERVE, run_config_name)
        self.template_path = template_path
        self.out_root = out_root
        self.no_input = no_input
        self.auto_commit = auto_commit
        self.save = save
        self.folder: Optional[str] = None
        self.repo: Optional[Repo] = None
        self.fxt = Flexlate()

    @property
    def out_path(self) -> Path:
        if self.folder is None:
            raise ValueError("folder must be set")
        return self.out_root / self.folder

    @property
    def data(self) -> Optional[TemplateData]:
        return self.run_config.data.data if self.run_config.data else None

    def on_modified(self, event: FileSystemEvent):
        global old
        super().on_modified(event)
        if not os.path.exists(event.src_path):
            return
        # Watchdog has a bug where two events will be triggered very quickly for one modification.
        # Track whether it's been at least a half second since the last modification, and only then
        # consider it a valid event
        stat_buf = os.stat(event.src_path)
        new = stat_buf.st_mtime
        if (new - old) > 0.5:
            # This is a valid event, now the main logic
            self.sync_output()
        old = new

    def sync_output(self):
        self.folder = update_or_initialize_project_get_folder(
            self.template_path,
            self.out_root,
            self.config,
            self.run_config,
            data=self.data,
            no_input=self.no_input,
            auto_commit=self.auto_commit,
            save=self.save,
            known_folder_name=self.folder,
            default_folder_name=self.run_config.data.folder_name
            if self.run_config.data
            else DEFAULT_PROJECT_NAME,
        )
        self.repo = Repo(self.out_path)
