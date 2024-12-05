"""Platform detection and command mapping utilities."""

import os
import platform
import shutil
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class PlatformInfo:
    """Information about the current platform and shell."""
    os_type: str
    shell_path: str
    shell_args: List[str]
    is_powershell: bool
    terminal_type: str

class CommandMapping:
    """Maps common operations to platform-specific commands."""
    
    # Commands that need shell execution on Windows
    WINDOWS_SHELL_COMMANDS = {
        'dir', 'type', 'copy', 'move', 'del', 'rd', 'md', 'echo', 'cls'
    }
    
    # Commands that need shell execution on Unix
    UNIX_SHELL_COMMANDS = {
        'ls', 'cat', 'cp', 'mv', 'rm', 'rmdir', 'mkdir', 'echo', 'clear'
    }
    
    UNIX_TO_WINDOWS = {
        'ls': 'dir',
        'cp': 'copy',
        'mv': 'move',
        'rm': 'del',
        'cat': 'type',
        'clear': 'cls',
        'touch': 'echo.',
        'mkdir': 'md',
        'rmdir': 'rd',
        'grep': 'findstr',
    }
    
    # Create reverse mapping
    WINDOWS_TO_UNIX = {v: k for k, v in UNIX_TO_WINDOWS.items()}
    
    @staticmethod
    def needs_shell(cmd: str, platform_info: 'PlatformInfo') -> bool:
        """Determine if a command needs shell execution."""
        cmd_lower = cmd.lower()
        if platform_info.os_type == 'windows':
            return cmd_lower in CommandMapping.WINDOWS_SHELL_COMMANDS
        return cmd_lower in CommandMapping.UNIX_SHELL_COMMANDS
    
    @staticmethod
    def get_command(cmd: str, platform_info: 'PlatformInfo') -> str:
        """Get the appropriate command for the current platform."""
        cmd_lower = cmd.lower()
        
        # Special handling for pwd/cd
        if cmd_lower == 'pwd':
            return 'cd' if platform_info.os_type == 'windows' else 'pwd'
        elif cmd_lower == 'cd':
            return 'cd'  # cd works the same on all platforms
            
        # Use standard mappings for other commands
        if platform_info.os_type == 'windows':
            return CommandMapping.UNIX_TO_WINDOWS.get(cmd_lower, cmd)
        return CommandMapping.WINDOWS_TO_UNIX.get(cmd_lower, cmd)

def get_platform_info() -> PlatformInfo:
    """
    Detect platform, shell, and terminal information.
    
    Returns:
        PlatformInfo: Object containing platform and shell details
    """
    os_type = platform.system().lower()
    
    # Detect PowerShell
    is_powershell = bool(os.getenv('PSModulePath'))
    
    # Detect terminal type
    terminal = os.getenv('TERM')
    if os_type == 'windows':
        if is_powershell:
            terminal_type = 'powershell'
        else:
            terminal_type = 'cmd'
    else:
        terminal_type = terminal if terminal else 'unknown'
    
    # Set shell information
    if os_type == 'windows':
        if is_powershell:
            shell_path = shutil.which('powershell') or 'powershell'
            shell_args = ['-Command']
        else:
            shell_path = shutil.which('cmd') or 'cmd.exe'
            shell_args = ['/c']
    else:
        # Try to detect the user's preferred shell
        shell_path = (
            os.getenv('SHELL') or 
            shutil.which('bash') or 
            shutil.which('sh') or 
            '/bin/sh'
        )
        shell_args = ['-c']
    
    return PlatformInfo(
        os_type=os_type,
        shell_path=shell_path,
        shell_args=shell_args,
        is_powershell=is_powershell,
        terminal_type=terminal_type
    )

def get_command_output_encoding(platform_info: PlatformInfo) -> str:
    """Get the appropriate encoding for command output based on platform."""
    if platform_info.os_type == 'windows':
        return 'cp1252' if platform_info.terminal_type == 'cmd' else 'utf-8'
    return 'utf-8'

def is_windows_path(path: str) -> bool:
    """Check if a path is a Windows-style path."""
    return '\\' in path or ':' in path

def normalize_path(path: str, platform_info: PlatformInfo) -> str:
    """Normalize path separators for the current platform."""
    if platform_info.os_type == 'windows':
        return path.replace('/', '\\')
    return path.replace('\\', '/')

# Dictionary of dangerous commands by platform
DANGEROUS_COMMANDS = {
    'windows': {
        'del', 'erase', 'format', 'rmdir', 'rd', 'ren',
        'move', 'attrib', 'diskpart', 'fsutil', 'reg',
        'sc', 'net', 'taskkill', 'shutdown', 'cipher'
    },
    'unix': {
        'rm', 'mv', 'dd', 'mkfs', 'fdisk', 'chmod',
        'chown', 'sudo', 'su', 'passwd', 'shutdown',
        'reboot', 'halt', 'kill', 'pkill'
    }
}

def is_dangerous_command(cmd: str, platform_info: PlatformInfo) -> bool:
    """Check if a command is considered dangerous on the current platform."""
    cmd_lower = cmd.lower()
    dangerous_cmds = (
        DANGEROUS_COMMANDS['windows'] 
        if platform_info.os_type == 'windows' 
        else DANGEROUS_COMMANDS['unix']
    )
    return cmd_lower in dangerous_cmds
