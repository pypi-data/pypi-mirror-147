import datetime
import re
from typing import Union
import packaging.version

from cli_changelog_md.enums import ChangeTypes
from cli_changelog_md.exceptions import ChangeBlockFoundException


RE_VERSION_RAW_BLOCK = re.compile(r'##[^#]?(\[.+\]?.+$)', flags=re.MULTILINE)
RE_VERSION_BLOCK = re.compile(r'\[(.+)\]')


class ChangeBlock(object):
    def __init__(self, name):
        self.change_type: ChangeTypes = ChangeTypes.get_by_tag(tag=name)
        self.changes: list[str] = []

    def text(self):
        result = f'### {self.change_type.tag.capitalize()}\n'
        result += ''.join([f"- {item}\n" for item in self.changes])
        return result

    def add(self, change):
        self.changes.append(change)


class VersionBlock(object):
    def __init__(self, version_row, raw=None):
        self.changes: list[ChangeBlock] = []
        self.version: packaging.version.Version = packaging.version.parse(self._detect_version(version_row))
        self.date: datetime.datetime = self._detect_date(version_row)

        self._init_from_raw(raw=raw)

    @property
    def is_empty(self):
        for item in self.changes:
            if item.changes:
                return False
        else:
            return True

    def add(self, change, change_type=ChangeTypes.FEATURED):
        for item in self.changes:
            if item.change_type == change_type:
                change_block = item
                break
        else:
            change_block = ChangeBlock(name=change_type.tag)
            self.changes.append(change_block)

        change_block.changes.append(change)

    def _init_from_raw(self, raw):
        if raw is None:
            return

        for row in [item.strip() for item in raw.strip().split('\n')]:
            if row.startswith('#'):
                change_block = ChangeBlock(name=row.replace('#', '').strip())
                self.changes.append(change_block)
            else:
                if not row.strip() or row.strip() == '---':
                    continue
                try:
                    change_block.add(row[1:].strip() if row.startswith('-') else row.strip())
                except UnboundLocalError:
                    raise ChangeBlockFoundException(f'Not found "##ChangeBlockName" in version "{self.version}"')

    def __gt__(self, other):
        if 'unreleased' in [self.version.base_version, other.version.base_version]:
            return other.version.base_version.lower() == 'unreleased'
        return self.version < other.version

    def __lt__(self, other):
        if 'unreleased' in [self.version.base_version.lower(), other.version.base_version.lower()]:
            return self.version.base_version.lower() == 'unreleased'
        return self.version > other.version

    def text(self):
        result = f"## [{self.version}]"
        result = result + f' - {self.date.strftime("%Y-%m-%d")}\n' if self.date else result + '\n'
        for item in self.changes:
            result += item.text()
        if self.version.public.lower() == 'unreleased':
            result += '\n---\n\n'
        else:
            result += '\n'
        return result

    @staticmethod
    def _detect_version(version_row):
        if version_row.startswith('['):
            return RE_VERSION_BLOCK.findall(version_row)[0]
        else:
            return version_row

    @staticmethod
    def _detect_date(version_row):
        split = version_row.split('-', maxsplit=1)
        return datetime.datetime.strptime(split[-1].strip(), "%Y-%m-%d") if len(split) > 1 else None

    def next_version(self) -> str:
        a = self.get_priority()
        v = self.version if self.version.__class__.__name__ != "LegacyVersion" else packaging.version.parse('0.0.0')

        if a == 0:
            return f'{v.major}.{v.minor + 1}.0'
        else:
            return f'{v.major}.{v.minor}.{v.micro}'

    def get_priority(self):
        return min([item.change_type.priority for item in self.changes])


class Changelog(object):
    def __init__(self, name='CHANGELOG', path=None):
        self.path: Union[str, None] = path
        self._versions: list[VersionBlock] = []
        self.name: str = name

    @property
    def versions(self):
        return sorted(self._versions)

    @classmethod
    def from_str(cls, value):
        blocks = RE_VERSION_RAW_BLOCK.split(value)
        obj = cls(name=blocks[0].strip()[1:] if blocks[0].startswith('#') else None)

        for index, item in enumerate(blocks[1:]):
            if item.strip().startswith('['):
                version = VersionBlock(version_row=item.strip(), raw=blocks[index + 2])
                obj.add(version)
        return obj

    @classmethod
    def from_file(cls, path):
        obj = Changelog.from_str(value=open(path, 'r', encoding='UTF8').read())
        obj.path = path
        return obj

    def add(self, version):
        self._versions.append(version)

    def text(self):
        result = f'#{self.name.upper()}\n'
        for item in self.versions:
            result += item.text()
        return result.strip() + '\n'

    def save(self, path=None):
        path = path if path else self.path
        if path:
            with open(path, 'w', encoding='UTF8') as fp:
                fp.write(self.text())

    def next_version(self):
        return self.last_version().next_version()

    def bump_version(self):
        return f'{self.last_version().version.major + 1}.0.0'

    def last_version(self):
        for item in self.versions:
            if item.version.epoch >= 0:
                return item
        return self.versions[0] if self.versions else None

    @property
    def unreleased(self):
        for item in self.versions:
            if item.version.public.lower() == 'unreleased':
                return item

    @property
    def has_unreleased_changes(self):
        return not self.unreleased.is_empty
