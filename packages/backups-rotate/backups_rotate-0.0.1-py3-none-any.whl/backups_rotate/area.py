"""
an area has a name, and a folder,
and it refers to a set of files defined by some patterns
together with a policy
"""

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from collections.abc import Iterator

import pandas as pd

from .policy import Policy


def extract_date_from_filename(path: Path, dateformat) -> pd.Timestamp | None:
    """
    Extracts a date from a filename using the provided date format.

    Args:
        filename (str): The filename to search for a date.
        dateformat (str): A strptime-compliant date format to match.

    Returns:
        datetime: The extracted date if found, None otherwise.
    """
    filename = path.name
    # we need to know how many characters to try and match
    dummy = datetime(2000, 1, 1, 0, 0, 0)
    partial_length = len(dummy.strftime(dateformat))

    for i in range(len(filename) - partial_length + 1):
        substring = filename[i:i + partial_length]
        try:
            # print(substring)
            return pd.Timestamp(datetime.strptime(substring, dateformat))
        except ValueError:
            continue
    return None


@dataclass
class TimedPath:
    """
    a path with a timestamp
    knows how to get the timestamp from the path or a format
    """
    path: Path
    timestamp: pd.Timestamp = None

    def attach_timestamp(self, *, datetime_format: str = None,
                         use_modification_time: bool = False):
        """
        attach a timestamp to the path

        if datetime_format is provided, it is used to parse the timestamp from
        the filename

        otherwise, and if use_modification_time is True, the modification time
        is used - the default is to use the creation time
        """
        # no format
        if datetime_format is None:
            if use_modification_time:
                self.timestamp = pd.Timestamp(self.path.stat().st_mtime)
            else:
                self.timestamp = pd.Timestamp(self.path.stat().st_ctime)
            return
        # otherwise use the format
        date = extract_date_from_filename(self.path, datetime_format)
        if date is None:
            raise ValueError(
                f"Could not extract date from {self.path} using {datetime_format}")
        self.timestamp = date

    def __lt__(self, other):
        return self.timestamp < other.timestamp


class Area:
    """
    an area is a set of files with a policy
    """

    def __init__(self, area_dict: dict):
        try:
            self.name = area_dict['name']
            self.path = Path(area_dict['folder'])
            self.patterns = area_dict['patterns']
            self.policy = Policy(area_dict['policy'])
        except KeyError as e:
            raise ValueError(f"Missing key {e}") from e
        self.datetime_format = area_dict.get('datetime_format', None)
        self.use_modification_time = area_dict.get('use_modification_time', None)
        # for the record
        self.area_dict = area_dict
        # stats
        self.total = 0
        self.deleted = 0
        # list of TimedPath
        self._files = None
        self._kept = None
        # sanity check
        self._check()

    def __repr__(self):
        return f"Area({self.name} on {self.path} - {self.total} files, {self.deleted} deleted)"

    def _check(self):
        """
        sanity check
        """
        # no need to check for mandatory fields
        # as they are used in the constructor already
        allowed = set("name|folder|patterns|policy|datetime_format|use_modification_time".split("|"))
        # any non-supported key ? this can be dangerous
        unsupported = set(self.area_dict.keys()) - allowed
        if unsupported:
            raise ValueError(f"Invalid keys in {self.name} : {unsupported}")

        if not isinstance(self.patterns, list):
            raise ValueError(f"Invalid patterns in {self.name} - should be a list")
        if not isinstance(self.use_modification_time, (bool, type(None))):
            raise ValueError(f"Invalid use_modification_time in {self.name} - should be a boolean")
        if self.datetime_format is not None and not isinstance(self.datetime_format, str):
            raise ValueError(f"Invalid datetime_format in {self.name} - should be a string")
        if self.use_modification_time is not None and self.datetime_format is not None:
            raise ValueError(f"Cannot have both use_modification_time and datetime_format {self.name}")

        # check the folder
        if not self.path.exists():
            raise ValueError(f"Folder {self.path} does not exist")
        if not self.path.is_dir():
            raise ValueError(f"{self.path} is not a folder")
        if not self.path.is_absolute():
            raise ValueError(f"{self.path} is not an absolute path")


    def _populate(self):
        """
        read the disk to populate the list of files
        """
        self._files = []
        for pattern in self.patterns:
            self._files.extend(self.path.glob(pattern))
        self._files = [TimedPath(path) for path in self._files]
        self.total = len(self._files)

    def _time_files(self):
        """
        attach a timestamp to each file
        """
        for file in self._files:
            file.attach_timestamp(
                datetime_format=self.datetime_format,
                use_modification_time=self.use_modification_time)
        # use TimedPath __lt__ to sort by timestamp
        self._files.sort()

    def read(self):
        """
        read the disk and computes which files to keep
        """
        self._populate()
        self._time_files()
        self._kept = self.policy.keep_timestamps([
            file.timestamp for file in self._files])
        self.deleted = 0
        for i, file in enumerate(self._files):
            if not self._kept[i]:
                self.deleted += 1


    def _iterate(self) -> Iterator[tuple[bool, Path, pd.Timestamp]]:
        """
        iterate on tuples (path: Path, kept: bool)
        """
        if self._kept is None:
            print("warning: area not read yet - bailing out")
            return
        for i, file in enumerate(self._files):
            yield (self._kept[i], file.path, file.timestamp)


    def list(self, *, deleted=True, kept=True):
        """
        shows the files in the area, with an indication of kept/deleted
        """
        if self._files is None:
            print("warning: area not populated yet")
            return
        if self._kept is None:
            print("warning: area not read yet - showing all files")
            for file in self._files:
                print(file)
            return
        for kept_file, file, ts in self._iterate():
            # show only selected entries
            if (deleted and not kept_file) or (kept and kept_file):
                print("KEEP" if kept_file else "DELE", end=" ")
                print(file, ts)

    def delete(self, *, dry_run=True, verbose=False):
        """
        delete the files in the area
        """
        for kept_file, file, _ts in self._iterate():
            if kept_file:
                if dry_run:
                    print("dry-run: would KEEP  ", file)
                continue
            if dry_run:
                print("dry-run: would DELETE", file)
            elif not file.exists():
                print("MISSING", file)
            else:
                if verbose:
                    print("DELETING", file)
                file.unlink()
