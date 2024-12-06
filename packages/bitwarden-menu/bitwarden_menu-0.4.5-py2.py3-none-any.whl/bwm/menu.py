"""Launcher functions

"""
import shlex
import sys
from subprocess import run

import bwm


def dmenu_cmd(num_lines, prompt):
    """Parse config.ini for dmenu options

    Args: args - num_lines: number of lines to display
                 prompt: prompt to show
    Returns: command invocation (as a list of strings) for
                ["dmenu", "-l", "<num_lines>", "-p", "<prompt>", "-i", ...]

    """
    commands = {"bemenu": ["-p", str(prompt), "-l", str(num_lines)],
                "dmenu": ["-p", str(prompt), "-l", str(num_lines)],
                "rofi": ["-dmenu", "-p", str(prompt), "-l", str(num_lines)],
                "wofi": ["--dmenu", "-p", str(prompt), "-L", str(num_lines + 1)]}
    command = shlex.split(bwm.CONF.get('dmenu', 'dmenu_command', fallback='dmenu'))
    command.extend(commands.get(command[0], []))
    pwprompts = ("Password", "password", "client_secret", "Verify password", "Enter Password")
    obscure = bwm.CONF.getboolean('dmenu_passphrase', 'obscure', fallback=True)
    if any(i == prompt for i in pwprompts) and obscure is True:
        pass_prompts = {"dmenu": dmenu_pass(command[0]),
                        "rofi": ['-password'],
                        "bemenu": ['-x', 'indicator', '*'],
                        "wofi": ['-P']}
        command.extend(pass_prompts.get(command[0], []))
    return command


def dmenu_pass(command):
    """Check if dmenu passphrase patch is applied and return the correct command
    line arg list

    Args: command - string
    Returns: list or None

    """
    if command != 'dmenu':
        return None
    try:
        # Check for dmenu password patch
        dm_patch = b'P' in run(["dmenu", "-h"],
                               capture_output=True,
                               check=False).stderr
    except FileNotFoundError:
        dm_patch = False
    color = bwm.CONF.get('dmenu_passphrase', 'obscure_color', fallback="#222222")
    return ["-P"] if dm_patch else ["-nb", color, "-nf", color]


def dmenu_select(num_lines, prompt="Entries", inp=""):
    """Call dmenu and return the selected entry

    Args: num_lines - number of lines to display
          prompt - prompt to show
          inp - string to pass to dmenu via STDIN

    Returns: sel - string

    """
    cmd = dmenu_cmd(num_lines, prompt)
    res = run(cmd,
              capture_output=True,
              check=False,
              input=inp,
              encoding=bwm.ENC,
              env=bwm.ENV)
    return res.stdout.rstrip('\n') if res.stdout is not None else None


def dmenu_err(prompt):
    """Pops up a dmenu prompt with an error message

    """
    try:
        prompt = prompt.decode(bwm.ENC)
    except AttributeError:
        pass
    return dmenu_select(len(prompt.splitlines()), "Error", inp=prompt)

# vim: set et ts=4 sw=4 :
