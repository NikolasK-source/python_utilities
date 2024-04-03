#!/usr/bin/env python3

__author__ = "Nikolas Koesling"
__copyright__ = "Copyright 2024, Nikolas Koesling"
__license__ = "LGPLv3"
__version__ = "1.0.0"
__email__ = "nikolas@koesling.info"

import subprocess
import unittest
from src.exec_cmd import execute


class TestExecCmd(unittest.TestCase):
    def test_uname(self):
        cmd = "uname"
        result = execute(cmd)
        self.assertEqual(result.command(), cmd, "command in CommandResult object is not command passed to exec_cmd")
        self.assertEqual(result.exit_code(), 0, "uname exit code is not 0")
        self.assertEqual(result.decode_stdout().strip(), "Linux", "uname result is not 'Linux'")
        self.assertEqual(len(result.decode_stderr().strip()), 0, "stderr not empty")

    def test_timeout(self):
        cmd = "sleep"
        args = ["1"]
        timeout = 0.1
        with self.assertRaises(subprocess.TimeoutExpired):
            execute(cmd, args, timeout=timeout)

    def test_timeout_ok(self):
        cmd = "sleep"
        args = ["0.1"]
        timeout = 0.2
        result = execute(cmd, args, timeout=timeout)
        self.assertEqual(result.exit_code(), 0)

    def test_input_ascii(self):
        cmd = "cat"
        cmd_input = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        cmd_input = cmd_input + cmd_input.lower() + '\n'
        cmd_input = cmd_input.encode('utf-8')
        result = execute(cmd, cmd_input=cmd_input)
        self.assertEqual(result.raw_stdout(), cmd_input)

    def test_input_utf8(self):
        cmd = "cat"
        cmd_input = "äåéëþüúíóö«»áßðfghïœø¶æœ©®·ñµç\n".encode('utf-8')
        result = execute(cmd, cmd_input=cmd_input)
        self.assertEqual(result.raw_stdout(), cmd_input)

    def test_non_existent_cmd(self):
        cmd = "nonexistent_command_iexwnmclcfygytdhtlnpddoarbtsqyvy"
        with self.assertRaises(FileNotFoundError):
            execute(cmd)

    def test_successful_cmd(self):
        cmd = "true"
        result = execute(cmd)
        self.assertEqual(result.exit_code(), 0)

    def test_failing_cmd(self):
        cmd = "false"
        result = execute(cmd)
        self.assertNotEqual(result.exit_code(), 0)

    def test_stderr(self):
        cmd = "uname"
        args = ["-x"]
        result = execute(cmd, args)
        self.assertNotEqual(result.exit_code(), 0)
        self.assertGreater(len(result.raw_stderr()), 0)
        self.assertGreater(len(result.decode_stderr()), 0)

    def test_stdout(self):
        cmd = "hexdump"
        args = ["-C", "-n", "8", "/dev/zero"]
        result = execute(cmd, args)
        self.assertEqual(result.exit_code(), 0)
        self.assertEqual(len(result.raw_stderr()), 0)
        self.assertGreater(len(result.raw_stdout()), 0)
        self.assertGreater(len(result.decode_stdout()), 0)
        self.assertEqual(result.decode_stdout().split('\n')[0][-1], '|')
        self.assertEqual(result.decode_stdout().split('\n')[1][-1], '8')

    def test_command_string(self):
        cmd = "hexdump"
        args = ["-C", "-n", "8", "/dev/zero"]
        result = execute(cmd, args)
        self.assertEqual(result.command_string(), "hexdump -C -n 8 /dev/zero")


if __name__ == '__main__':
    unittest.main()
