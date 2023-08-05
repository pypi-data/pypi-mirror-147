'''pysvn utilities module.
'''
import subprocess
from typing import List

def check_svn_installed() -> bool:
    """Check if the current system has the svn cli client installed.

    Returns:
        bool: True if svn is installed, otherwise False
    """
    try:
        subprocess.run('svn', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def get_longest_line_len(lines: List[str]) -> int:
    longest_len = 0
    for line in lines:
        if len(line) > longest_len:
            longest_len = len(line)
    return longest_len