#!/usr/bin/env python3

"""
:brief: wrapper to simplify subprocess.Popen
"""

__author__ = "Nikolas Koesling"
__copyright__ = "Copyright 2024, Nikolas Koesling"
__license__ = "LGPLv3"
__version__ = "1.0.1"
__email__ = "nikolas@koesling.info"

import subprocess
import shlex


class CommandResult:
    """
    :brief: class that conntains the result of exec_cmd
    """

    def __init__(self, cmd: str, args: list[str], stdout: bytes, stderr: bytes,
                 exit_code: int) -> None:
        self.__cmd = cmd
        self.__args = args
        self.__stdout = stdout
        self.__stderr = stderr
        self.__exit_code = exit_code

    def command(self) -> str:
        """
        :brief: returns the command (without arguments)
        :return: command string
        """
        return self.__cmd

    def command_string(self) -> str:
        """
        :brief: returns the command (including its arguments) as string
        :return: command string including arguments (escaped for use in shell)
        """
        return shlex.join([self.__cmd] + self.__args)

    def decode_stdout(self, encoding: str = 'utf-8') -> str:
        """
        :brief: returns the command output (stdout) as string
        :param encoding: encoding that is used to decode the output
        :return: command output as string
        """
        return self.__stdout.decode(encoding)

    def decode_stderr(self, encoding: str = 'utf-8') -> str:
        """
        :brief: returns the command output (stderr) as string
        :param encoding: encoding that is used to decode the output
        :return: command output as string
        """
        return self.__stderr.decode(encoding)

    def raw_stdout(self) -> bytes:
        """
        :brief: returns the raw command output (stdout)
        :return: raw command output (bytes)
        """
        return self.__stdout

    def raw_stderr(self) -> bytes:
        """
        :brief: returns the raw command output (stderr)
        :return: raw command output (bytes)
        """
        return self.__stderr

    def exit_code(self) -> int:
        """
        :brief: returns the command exit code
        :return: exit code
        """
        return self.__exit_code


def execute(cmd: str,
            args: list[str] | None = None,
            cmd_input: bytes | None = None,
            timeout: float | None = None
            ) -> CommandResult:
    """
    :brief: execute a command as subprocess
    :param cmd: command to execute
    :param args: list of command arguments
    :param cmd_input: optional command input
    :param timeout: optional timeout in seconds
    :return: result as CommandResult object
    """
    with subprocess.Popen([cmd] + args if args else [cmd],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as process:
        try:
            stdout, stderr = process.communicate(input=cmd_input, timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(input=cmd_input, timeout=timeout)
            raise
        exit_code = process.returncode

    return CommandResult(cmd, args, stdout, stderr, exit_code)


if __name__ == '__main__':
    import sys
    import os

    print("Not a standalone module", file=sys.stderr)
    sys.exit(os.EX_SOFTWARE)
