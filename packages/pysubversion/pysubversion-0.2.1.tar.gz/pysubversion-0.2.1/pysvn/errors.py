'''pysvn errors module.
'''

class SVNNotInstalledError(Exception):
    pass

class RepositoryDirDoesNotExistError(Exception):
    pass

class NoSuchRevisionError(Exception):
    pass

class RevisionSyntaxError(Exception):
    pass
