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
    
    # Create reverse mapping but exclude pwd/cd which need special handling
    WINDOWS_TO_UNIX = {v: k for k, v in UNIX_TO_WINDOWS.items()}
    
    @staticmethod
    def get_command(cmd: str, platform_info: PlatformInfo) -> str:
        """Get the appropriate command for the current platform."""
        # Special handling for pwd/cd
        if cmd == 'pwd':
            return 'cd' if platform_info.os_type == 'windows' else 'pwd'
        elif cmd == 'cd' and not platform_info.os_type == 'windows':
            return 'cd'  # Keep cd as cd on Unix
            
        # Use standard mappings for other commands
        if platform_info.os_type == 'windows':
            return CommandMapping.UNIX_TO_WINDOWS.get(cmd, cmd)
        return CommandMapping.WINDOWS_TO_UNIX.get(cmd, cmd)

def _find_unix_shell() -> tuple[str, List[str]]:
    """
    Find the appropriate shell on Unix-like systems.
    
    Returns:
        tuple: (shell_path, shell_args)
    """
    # First try user's preferred shell from env
    shell = os.getenv('SHELL')
    
    # If no SHELL env var, try common shells in order
    if not shell:
        for shell_name in ['bash', 'sh', 'dash']:
            shell = shutil.which(shell_name)
            if shell:
                break
    
    # If still no shell found, use /bin/sh as last resort
    if not shell:
        shell = '/bin/sh'
    
    # Determine shell type and set appropriate args
    shell_name = os.path.basename(shell)
    if shell_name == 'bash':
        # Use login shell for better environment setup
        return shell, ['--login', '-i', '-c']
    elif shell_name in ['sh', 'dash']:
        # Basic shells just need -c
        return shell, ['-c']
    else:
        # Default to -c for unknown shells
        return shell, ['-c']

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
        # For Unix, try to get more specific terminal info
        if terminal:
            terminal_type = terminal
        else:
            # Try to detect terminal from process hierarchy
            terminal_type = os.getenv('TERM_PROGRAM', 'unknown')
    
    # Set shell information
    if os_type == 'windows':
        if is_powershell:
            shell_path = shutil.which('powershell') or 'powershell'
            shell_args = ['-Command']
        else:
            shell_path = shutil.which('cmd') or 'cmd.exe'
            shell_args = ['/c']
    else:
        # Use enhanced Unix shell detection
        shell_path, shell_args = _find_unix_shell()
    
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
    
    # For Unix systems, try to detect encoding from locale
    try:
        import locale
        return locale.getpreferredencoding()
    except:
        return 'utf-8'  # Fallback to UTF-8

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
