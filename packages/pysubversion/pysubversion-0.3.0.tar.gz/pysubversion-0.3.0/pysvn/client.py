from datetime import datetime
import subprocess
from subprocess import Popen
import os
from typing import List, Union
import xml.etree.ElementTree
import pathlib

from pysvn.errors import *
from pysvn.models import *
from pysvn.utils import *
from pysvn.constants import *


class Client:
    """# A command-line SVN client.

    Subversion is a tool for version control.
    For additional information, see [the subversion website](http://subversion.apache.org/)
    """
    def __init__(self, repository_dir: str = os.getcwd()) -> None:
        """# A command-line SVN client.
        
        Subversion is a tool for version control.
        For additional information, see [the subversion website](http://subversion.apache.org/)

        Args:
            repository_dir (str, optional): svn repository directory. Defaults to os.getcwd().

        Raises:
            SVNNotInstalledError: svn command line client is not installed.
            RepositoryDirDoesNotExistError: repository_dir provided does not exist.
            NotADirectoryError: reposiory_dir provided is not a directory.
        """
        if not check_svn_installed():
            raise SVNNotInstalledError(
                'Is the command line svn client installed? If so, check that it\'s in path.')

        repo_dir = pathlib.Path(repository_dir)
        if not repo_dir.exists():
            raise RepositoryDirDoesNotExistError(
                'the repository_dir provided does not exist')
        if not repo_dir.is_dir():
            raise NotADirectoryError(
                'the repository_dir provided is not a directory')

        self.cwd = str(repo_dir.resolve())


    def log(self, file: str = None, revision: Union[int, Revision, str] = 'HEAD:1') -> List[LogEntry]:
        """## Show the log messages for a set of revision(s) and/or path(s).

        Args:
            file (str, optional): file to get logs for. Defaults to None.
            revision (int | Revision | str, optional): revision. Defaults to `HEAD:1`.

        Raises:
            NoSuchRevisionError: unknown revision.
            RevisionSyntaxError: invalid revision syntax when providing a str.

        Returns:
            List[LogEntry]: list of log entries.
        """
        revision = revision.name if type(revision) == Revision else revision
        log_cmd = f'log --xml --revision {revision}' if not file else f'log {file} --xml --revision {revision}'
        log_entries: List[LogEntry] = []
        cmd = self._run_svn_cmd(log_cmd.split(' '))

        stderr = cmd.stderr.read()
        if stderr and 'No such revision' in stderr.decode('utf-8'):
            rev_num = stderr.decode('utf-8').split(' ')[-1]
            raise NoSuchRevisionError(f'no such revision {rev_num}')

        data = cmd.stdout.read()

        try:
            root = xml.etree.ElementTree.fromstring(data)

            for e in root.iter('logentry'):
                entry_info = {x.tag: x.text for x in list(e)}

                date = None
                if entry_info.get('date'):
                    date_str = entry_info.get('date').split('.', 1)[0]
                    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')

                log_entry = LogEntry(
                    message=entry_info.get('msg'),
                    author=entry_info.get('author'),
                    revision=int(e.get('revision')),
                    date=date
                )

                log_entries.append(log_entry)

            return log_entries
        except xml.etree.ElementTree.ParseError:
            raise RevisionSyntaxError(
                f"with great power comes great responsibility, '{revision}' is not valid revision syntax")


    def _run_svn_cmd(self, args: List[str]) -> Popen:
        args.insert(0, 'svn')
        return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.cwd)


    def __svn_update__(self) -> None:
        self._run_svn_cmd(['update'])
    

    def diff(self, start_revision: int, end_revision: int = None) -> Diff:
        """## Display local changes or differences between two revisions or paths.

        Args:
            start_revision (int): starting revision
            end_revision (int, optional): ending revision. Defaults to `HEAD`.

        Raises:
            NoSuchRevisionError: unknown revision.

        Returns:
            Diff: diff between starting and ending revisions.
        """
        self.__svn_update__()

        if not end_revision:
            end_revision = 'HEAD'

        cmd = self._run_svn_cmd(
            ['diff', '-r', f'{start_revision}:{end_revision}', '--xml', '--summarize'])

        stderr = cmd.stderr.read()
        if stderr and 'No such revision' in stderr.decode('utf-8'):
            rev_num = stderr.decode('utf-8').split(' ')[-1]
            raise NoSuchRevisionError(f'no such revision {rev_num}')

        data = cmd.stdout.read()
        paths: List[SVNItemPath] = []
        root = xml.etree.ElementTree.fromstring(data)

        for e in root.iter('path'):
            attrs = e.attrib
            filepath = e.text
            svn_path = SVNItemPath(
                item=attrs.get('item'),
                props=attrs.get('props'),
                kind=attrs.get('kind'),
                filepath=filepath
            )
            paths.append(svn_path)

        return Diff(paths)


    def revert(self, path: str, recursive: bool = False, remove_added: bool = False, depth: Depth = None) -> str:
        """## Restore pristine working copy state (undo local changes).

        Revert changes in the working copy at or within PATH, and remove
        conflict markers as well, if any.

        This subcommand does not revert already committed changes.

        Args:
            path (str): path of item to revert.
            recursive (bool, optional): descend recursively, same as Depth.INFINITY. Defaults to False.
            remove_added (bool, optional): reverting an added item will remove it from disk. Defaults to False.
            depth (Depth, optional): limit operation by depth. Defaults to None.

        Returns:
            str: revert output
        """
        revert_cmd = ['revert', path]
        if recursive:
            revert_cmd.append('--recursive')
        if remove_added:
            revert_cmd.append('--remove-added')
        if depth:
            revert_cmd.append('--depth')
            revert_cmd.append(depth.value)
        
        cmd = self._run_svn_cmd(revert_cmd)
        stdout, stderr = get_output(cmd)
        return '' + stdout.strip() + stderr.strip()
    

    def update(self, path: Union[str, List[str]] = None,
               revision: int = None,
               accept: CRAction = None,
               depth: Depth = None,
               force: bool = False,
               ignore_externals: bool = False,
               parents: bool = False,
               adds_as_modification: bool = False) -> str:
        """## Bring changes from the repository into the working copy.
        Examples:
            `output = svn.update()`\n
            `output = svn.update(path='foo.txt')`\n
            `output = svn.update(path='foo.txt', depth=Depth.FILES)`

        If no revision is given, bring working copy up-to-date with HEAD rev.
        Else synchronize working copy to revision.
        Example:
            `output = svn.update(path='foo.txt', revision=34)`

        For each updated item a line will be printed with characters reporting
        the action taken. These characters have the following meaning:

        - A  Added
        - D  Deleted
        - U  Updated
        - C  Conflict
        - G  Merged
        - E  Existed
        - R  Replaced

        Characters in the first column report about the item itself.
        Characters in the second column report about properties of the item.
        A `B` in the third column signifies that the lock for the file has
        been broken or stolen.
        A `C` in the fourth column indicates a tree conflict, while a `C` in
        the first and second columns indicate textual conflicts in files
        and in property values, respectively.

        If `force` is `True`, unversioned obstructing paths in the working
        copy do not automatically cause a failure if the update attempts to
        add the same path.  If the obstructing path is the same type (file
        or directory) as the corresponding path in the repository it becomes
        versioned but its contents are left `as-is` in the working copy.
        This means that an obstructing directory's unversioned children may
        also obstruct and become versioned. For files, any content differences
        between the obstruction and the repository are treated like a local
        modification to the working copy. All properties from the repository
        are applied to the obstructing path. Obstructing paths are reported
        in the first column with code `E`.

        If the specified update target is missing from the working copy but its
        immediate parent directory is present, checkout the target into its
        parent directory at the specified depth.  If `parents` is set,
        create any missing parent directories of the target by checking them
        out, too, at `depth=EMPTY`.

        Use `depth` to set a new working copy depth on the
        targets of this operation.

        Args:
            path (str | List[str], optional): path to file(s) to update (Example: `'foo.txt'` or `['foo.txt']`). Defaults to `'.'`.
            revision (int, optional): revision number to update to. Defaults to None.
            accept (CRAction, optional): specify automatic conflict resolution action. Defaults to None.
            depth (Depth, optional): limit operation by depth. Defaults to None.
            force (bool, optional): handle unversioned obstructions as changes. Defaults to False.
            ignore_externals (bool, optional): ignore externals definitions. Defaults to False.
            parents (bool, optional): make intermediate directories. Defaults to False.
            adds_as_modification (bool, optional): Local additions are merged with incoming additions
                                                   instead of causing a tree conflict. Use of this
                                                   option is not recommended!. Defaults to False.

        Raises:
            NoSuchRevisionError: raised if a revision is given and its unknown.
            SVNUpdateError: raised if something goes wrong in the svn update command.

        Returns:
            str: command output
        """
        update_cmd = ['update']
        if path:
            if type(path) == str:
                update_cmd.append(path)
            elif type(path) == list:
                update_cmd.extend(path)
        if revision:
            update_cmd.extend(['--revision', str(revision)])
        if accept:
            update_cmd.extend(['--accept', accept.value])
        if depth:
            update_cmd.extend(['--depth', depth.value])
        if force:
            update_cmd.append('--force')
        if ignore_externals:
            update_cmd.append('--ignore-externals')
        if parents:
            update_cmd.append('--parents')
        if adds_as_modification:
            update_cmd.append('--adds-as-modification')
        
        stdout, stderr = get_output(self._run_svn_cmd(update_cmd))

        if stderr:
            if 'No such revision' in stderr:
                rev_num = stderr.split(' ')[-1]
                raise NoSuchRevisionError(f'no such revision {rev_num}')
            else:
                raise SVNUpdateError(stderr)
        
        return stdout


    def __str__(self) -> str:
        cmd = self._run_svn_cmd(['info'])
        stats = cmd.stdout.read().decode('utf-8').strip()
        if stats:
            num_of_signs = get_longest_line_len(stats.split('\n'))
            signs = '=' * num_of_signs
            return f'SVN Client\n{signs}\n{stats}\n{signs}'
        return f'SVN Client - {self.cwd} - no svn repository info to show'


    def __repr__(self) -> str:
        return f'Client(cwd={self.cwd})'
