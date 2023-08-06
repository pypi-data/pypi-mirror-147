'''pysvn errors module.
'''

class SVNError(Exception):
    pass

class SVNNotInstalledError(Exception):
    pass

class RepositoryDirDoesNotExistError(Exception):
    pass

class NoSuchRevisionError(Exception):
    pass

class RevisionSyntaxError(Exception):
    pass

class SVNUpdateError(Exception):
    pass

class PreviousOperationNotFinishedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('previous operation has not finished')