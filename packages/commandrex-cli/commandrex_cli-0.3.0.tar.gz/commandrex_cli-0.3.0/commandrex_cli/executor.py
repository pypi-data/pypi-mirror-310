"""Cross-platform command execution module."""

import subprocess
import threading
import os
import signal
import time
import logging
import io
from typing import List, Optional, Union, IO

from rich.console import Console

from .platform_utils import (
    get_platform_info,
    get_command_output_encoding,
    is_dangerous_command,
    CommandMapping,
    PlatformInfo
)
from .schemas import Command, CommandResult
from .config import Config

console = Console()

# Initialize logger
logger = logging.getLogger(__name__)

class CommandExecutor:
    """Safely executes translated commands across different platforms."""
    
    # Commands that should be executed directly without shell wrapping
    DIRECT_EXECUTE_COMMANDS = {
        'ps', 'ls', 'ping', 'netstat', 'top', 'htop',
        'df', 'du', 'free', 'who', 'w', 'uptime'
    }

    # Commands that are typically continuous and need special handling
    CONTINUOUS_COMMANDS = {
        'ping': {'max_packets': 4},  # Stop ping after 4 packets
        'top': {'timeout': 10},      # Run top for 10 seconds
        'htop': {'timeout': 10},     # Run htop for 10 seconds
    }
    
    def __init__(self):
        self.platform_info = get_platform_info()
        logger.info(f"Platform info: {self.platform_info}")
        self.command_mapping = CommandMapping()
        self.encoding = get_command_output_encoding(self.platform_info)
        logger.info(f"Using encoding: {self.encoding}")
        self.current_process = None
        self._previous_dir = None
        self._stop_streaming = False

    def _handle_output_line(self, line: str, lines: list, is_error: bool):
        """Handle a single line of output."""
        if line:
            lines.append(line)
            if is_error:
                console.print(f"[red]{line}[/red]")
                logger.error(f"Process error output: {line}")
            else:
                console.print(line)
                logger.debug(f"Process output: {line}")

    def _stream_output(self, process: subprocess.Popen, output_lines: list, error_lines: list):
        """Stream output from process in real-time."""
        self._stop_streaming = False
        
        def read_stream(stream: IO[Union[str, bytes]], lines: list, is_error: bool = False):
            """Read from a stream and process lines."""
            try:
                # Log the stream type for debugging
                logger.debug(f"Stream type: {type(stream)}")
                
                while not self._stop_streaming:
                    if isinstance(stream, io.TextIOBase):
                        # For text mode streams
                        line = stream.readline()
                        if not line:
                            if process.poll() is not None:
                                break
                            continue
                        
                        # Remove trailing newline
                        line = line.rstrip('\n')
                        self._handle_output_line(line, lines, is_error)
                    else:
                        # For binary mode streams
                        chunk = stream.read1(4096)
                        if not chunk:
                            if process.poll() is not None:
                                break
                            continue
                            
                        try:
                            text = chunk.decode(self.encoding)
                            for line in text.splitlines():
                                self._handle_output_line(line, lines, is_error)
                        except UnicodeDecodeError:
                            try:
                                text = chunk.decode('utf-8', errors='replace')
                                for line in text.splitlines():
                                    self._handle_output_line(line, lines, is_error)
                            except:
                                logger.error("Failed to decode process output")
                                continue
                                
            except (OSError, IOError) as e:
                logger.error(f"Stream error: {str(e)}")
                logger.error(f"Stream type was: {type(stream)}")
        
        # Create separate threads for stdout and stderr
        if process.stdout:
            stdout_thread = threading.Thread(
                target=read_stream,
                args=(process.stdout, output_lines)
            )
            stdout_thread.daemon = True
            stdout_thread.start()
        
        if process.stderr:
            stderr_thread = threading.Thread(
                target=read_stream,
                args=(process.stderr, error_lines, True)
            )
            stderr_thread.daemon = True
            stderr_thread.start()
        
        # Wait for both streams to complete
        if process.stdout:
            stdout_thread.join()
        if process.stderr:
            stderr_thread.join()

    def execute(self, command: Command) -> CommandResult:
        """
        Execute a command safely with real-time output streaming.
        
        Args:
            command: Command object to execute
            
        Returns:
            CommandResult: Result of command execution
        """
        logger.info(f"Executing command: {command.executable} {' '.join(command.args)}")
        try:
            # Special handling for directory change commands
            if command.executable.lower() in ['cd', 'chdir'] or (
                self.platform_info.is_powershell and 
                command.executable.lower() == 'set-location'
            ):
                # If it's Set-Location, modify the command to use the directory argument
                if command.executable.lower() == 'set-location':
                    modified_command = Command(
                        executable='cd',
                        args=command.args,
                        is_dangerous=is_dangerous_command('cd', self.platform_info)
                    )
                    return self._handle_cd_command(modified_command)
                return self._handle_cd_command(command)
            
            # Additional safety check using is_dangerous_command function
            if is_dangerous_command(command.executable, self.platform_info):
                confirm = console.input(
                    "[yellow]This command may be dangerous. "
                    "Are you sure you want to proceed? (y/N): [/yellow]"
                ).lower()
                
                if confirm != 'y':
                    return CommandResult(
                        success=False,
                        output="Command cancelled by user.",
                        error=None,
                        exit_code=1
                    )
            
            # Prepare command
            cmd_list = self._prepare_command(command)
            
            # Execute command with real-time output streaming
            output_lines = []
            error_lines = []
            
            # Determine if we should use shell
            use_shell = command.executable.lower() not in self.DIRECT_EXECUTE_COMMANDS
            
            try:
                # Set up process with proper input/output handling
                if self.platform_info.os_type == 'windows':
                    logger.debug(f"Starting Windows process: {cmd_list}")
                    process = subprocess.Popen(
                        cmd_list,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=use_shell,  # Use shell based on command type
                        cwd=os.getcwd(),
                        text=False  # Binary mode for Windows
                    )
                else:
                    # For Unix-like systems, always use shell=True and pass command as string
                    logger.debug(f"Starting Unix process: {cmd_list[0]}")
                    process = subprocess.Popen(
                        cmd_list[0],  # Use the combined command string
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True,  # Always use shell on Unix
                        executable='/bin/bash',  # Explicitly use bash
                        preexec_fn=os.setsid,  # Create new process group
                        cwd=os.getcwd(),
                        text=True,  # Text mode for Unix
                        bufsize=1,  # Line buffered
                        encoding=self.encoding  # Use detected encoding
                    )
                
            except Exception as e:
                logger.error(f"Failed to start process: {str(e)}")
                return CommandResult(
                    success=False,
                    output="",
                    error=f"Failed to start process: {str(e)}",
                    exit_code=1
                )
            
            # Store current process
            self.current_process = process
            
            # Create and start output streaming thread
            stream_thread = threading.Thread(
                target=self._stream_output,
                args=(process, output_lines, error_lines)
            )
            stream_thread.daemon = True
            stream_thread.start()
            
            try:
                # For continuous commands, wait with timeout
                if command.executable.lower() in self.CONTINUOUS_COMMANDS:
                    config = self.CONTINUOUS_COMMANDS[command.executable.lower()]
                    timeout = config.get('timeout', 10)  # Default timeout of 10 seconds
                    try:
                        exit_code = process.wait(timeout=timeout)
                    except subprocess.TimeoutExpired:
                        self.stop_current_process()
                        exit_code = 0  # Consider timeout as normal completion
                else:
                    # Wait for process to complete or user interrupt
                    exit_code = process.wait()
                logger.info(f"Process completed with exit code: {exit_code}")
            except KeyboardInterrupt:
                logger.info("Process interrupted by user")
                self.stop_current_process()
                exit_code = 0  # Consider interrupt as normal termination
            finally:
                self._stop_streaming = True
                stream_thread.join(timeout=1.0)  # Wait for streaming to complete with timeout
                
                # Clear current process
                self.current_process = None
            
            # Combine output and error lines
            output = '\n'.join(output_lines)
            error = '\n'.join(error_lines) if error_lines else None
            
            return CommandResult(
                success=exit_code == 0,
                output=output,
                error=error,
                exit_code=exit_code
            )
            
        except subprocess.SubprocessError as e:
            logger.error(f"Subprocess error: {str(e)}")
            return CommandResult(
                success=False,
                output="",
                error=str(e),
                exit_code=1
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return CommandResult(
                success=False,
                output="",
                error=f"Unexpected error: {str(e)}",
                exit_code=1
            )

    def _prepare_command(self, command: Command) -> List[str]:
        """
        Prepare command for execution.
        
        Args:
            command: Command object to prepare
            
        Returns:
            List[str]: Command and arguments ready for execution
        """
        # Map command to platform-specific version
        executable = self.command_mapping.get_command(
            command.executable,
            self.platform_info
        )
        logger.debug(f"Mapped command '{command.executable}' to '{executable}'")

        # Handle continuous commands like ping
        if executable == 'ping':
            # Add count parameter based on platform
            if self.platform_info.os_type == 'windows':
                cmd_list = [executable, '-n', '4', *command.args]  # Windows uses -n
            else:
                cmd_list = [executable, '-c', '4', *command.args]  # Unix uses -c
            logger.debug(f"Prepared ping command: {cmd_list}")
            return cmd_list
        
        # For direct execute commands, return the command and args directly
        if command.executable.lower() in self.DIRECT_EXECUTE_COMMANDS:
            cmd_list = [executable, *command.args]
            logger.debug(f"Prepared direct execute command: {cmd_list}")
            return cmd_list
        
        # For Unix-like systems, combine command into a single string
        if self.platform_info.os_type != 'windows':
            cmd_str = f"{executable} {' '.join(command.args)}"
            logger.debug(f"Prepared Unix command string: {cmd_str}")
            return [cmd_str]
        
        # For Windows, use standard shell wrapping
        cmd_list = [
            self.platform_info.shell_path,
            *self.platform_info.shell_args
        ]
        
        # Create the command string
        if self.platform_info.is_powershell:
            # PowerShell needs special handling for some commands
            cmd_str = f"& {executable} {' '.join(command.args)}"
        else:
            cmd_str = f"{executable} {' '.join(command.args)}"
        
        cmd_list.append(cmd_str)
        logger.debug(f"Prepared Windows command: {cmd_list}")
        return cmd_list

    def _handle_cd_command(self, command: Command) -> CommandResult:
        """
        Special handling for cd command to make directory changes persist.
        
        Args:
            command: Command object containing cd command
            
        Returns:
            CommandResult: Result of directory change
        """
        try:
            # Get the target directory from command args
            if not command.args:
                # cd without args should go to home directory
                target_dir = os.path.expanduser("~")
            else:
                # Expand any ~ in the path first
                target_dir = os.path.expanduser(command.args[0])
            
            # Handle special cases
            if target_dir == "-":
                # cd - to go to previous directory
                if not self._previous_dir:
                    return CommandResult(
                        success=False,
                        output="",
                        error="No previous directory",
                        exit_code=1
                    )
                target_dir = self._previous_dir
            
            # Store current directory before changing
            self._previous_dir = os.getcwd()
            
            # Handle relative paths
            if not os.path.isabs(target_dir):
                target_dir = os.path.abspath(os.path.join(os.getcwd(), target_dir))
            
            # Change directory in the main process
            os.chdir(target_dir)
            
            # Get and display new working directory
            new_dir = os.getcwd()
            logger.info(f"Changed directory to: {new_dir}")
            return CommandResult(
                success=True,
                output=f"Current directory: {new_dir}",
                error=None,
                exit_code=0
            )
            
        except Exception as e:
            logger.error(f"Directory change failed: {str(e)}")
            return CommandResult(
                success=False,
                output="",
                error=str(e),
                exit_code=1
            )

    def stop_current_process(self):
        """Stop the currently running process if any."""
        if self.current_process:
            self._stop_streaming = True
            if self.platform_info.os_type == 'windows':
                self.current_process.terminate()
            else:
                try:
                    os.killpg(os.getpgid(self.current_process.pid), signal.SIGINT)
                except Exception as e:
                    logger.error(f"Failed to stop process: {str(e)}")

__all__ = ['CommandExecutor']
