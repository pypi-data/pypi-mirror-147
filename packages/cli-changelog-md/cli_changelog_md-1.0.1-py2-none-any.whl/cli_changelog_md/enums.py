import enum

from cli_changelog_md.exceptions import UnsupportedTagException


class ChangeTypes(enum.Enum):
    def __init__(self, values):
        self.tag = values['tag']
        self.priority = values['priority']

    FEATURED = {"tag": "Featured", "priority": 0}
    CHANGED = {"tag": "Changed", "priority": 0}
    FIXED = {"tag": "Fixed", "priority": 1}
    MISC = {"tag": "Misc", "priority": 1}

    @staticmethod
    def get_by_tag(tag):
        for item in ChangeTypes:
            if item.tag.lower() == tag.lower():
                return item
        raise UnsupportedTagException(f'Tag "{tag}" not supported!')

    @staticmethod
    def accept_tag():
        return [item.tag for item in ChangeTypes]
