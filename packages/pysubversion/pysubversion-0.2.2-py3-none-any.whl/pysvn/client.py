from datetime import datetime
import subprocess
from subprocess import Popen
import os
from typing import List, Union
import xml.etree.ElementTree
import pathlib

from pysvn.errors import RepositoryDirDoesNotExistError, SVNNotInstalledError, NoSuchRevisionError, RevisionSyntaxError

from pysvn.models import LogEntry, Revision, Diff, SVNItemPath, Depth

from pysvn.utils import check_svn_installed, get_longest_line_len


class Client:
    """SVN client.

    Subversion is a tool for version control.
    For additional information, see http://subversion.apache.org/
    """
    def __init__(self, repository_dir: str = os.getcwd()) -> None:
        """SVN client.

        Subversion is a tool for version control.
        For additional information, see http://subversion.apache.org/

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
        """Show the log messages for a set of revision(s) and/or path(s).

        Args:
            file (str, optional): file to get logs for. Defaults to None.
            revision (int | Revision | str, optional): revision. Defaults to HEAD.

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
        """Display local changes or differences between two revisions or paths.

        Args:
            start_revision (int): starting revision
            end_revision (int, optional): ending revision. Defaults to HEAD.

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
        """Restore pristine working copy state (undo local changes).

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
        stdout = cmd.stdout.read().decode('utf-8')
        stderr = cmd.stderr.read().decode('utf-8')
        output = ''
        output += stdout.strip()
        output += stderr.strip()
        return output
        

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
