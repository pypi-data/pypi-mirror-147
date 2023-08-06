class ChangeLogException(Exception): pass


class MainBlockNotFoundException(ChangeLogException): pass


class MultiSeparatorException(ChangeLogException): pass


class NotUnreleasedSeparator(ChangeLogException): pass


class UnsupportedTagException(ChangeLogException): pass


class ChangeBlockFoundException(ChangeLogException): pass


class ChangeLogFileNotFoundException(ChangeLogException): pass