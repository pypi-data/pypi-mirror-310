from pathlib import Path
import re
import os
import subprocess
import shlex
from datetime import datetime
from rich import print


def get_current_datetime() -> str:
	"""
	Gets the current datetime.

	:returns:	The current datetime.
	:rtype:		str
	"""
	return datetime.now().strftime("%H:%M:%S")


def print_header(msg_type: str, text: str):
	"""
	Prints a header.

	:param		msg_type:  The message type
	:type		msg_type:  str
	:param		text:	   The text
	:type		text:	   str
	"""
	print(
		f'[yellow]{"#" * len(text)}[/yellow]\n[blue]{get_current_datetime()} {msg_type.upper()}][/blue] {text}\n[yellow]{"#" * len(text)}[/yellow]\n'
	)


def print_step(msg_type: str, text: str):
	"""
	Prints a step.

	:param		msg_type:  The message type
	:type		msg_type:  str
	:param		text:	   The text
	:type		text:	   str
	"""
	print(
		f'[yellow]{"=" * 16}[/yellow] [blue][{get_current_datetime()} {msg_type.upper()}][/blue] {text}'
	)


def print_substep(msg_type: str, text: str):
	"""
	Prints a substep.

	:param		msg_type:  The message type
	:type		msg_type:  str
	:param		text:	   The text
	:type		text:	   str
	"""
	print(
		f'[cyan]{"=" * 8}[/cyan]\n[blue][{get_current_datetime()} {msg_type.upper()}][/blue] {text}'
	)


def print_message(msg_type: str, text: str):
	"""
	Prints a message.

	:param		msg_type:  The message type
	:type		msg_type:  str
	:param		text:	   The text
	:type		text:	   str
	"""
	print(f"[blue][{get_current_datetime()} {msg_type.upper()}][/blue] {text}")


class CommandManager:
	"""
	This class describes an command manager.
	"""

	@staticmethod
	def run_command(command: str) -> int:
		"""
		Run a command in the shell

		:param		command:	   The command
		:type		command:	   str

		:returns:	return code
		:rtype:		int

		:raises		RuntimeError:  command failed
		"""

		print_message(
			"info",
			f"[italic] Execute command: [/italic]: [white on black]{command}[/white on black]",
		)

		result = subprocess.run(
			shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE
		)

		if result.returncode != 0:
			raise RuntimeError(
				f'Command "{command}" failed with exit code {result.returncode}:\n{result.stderr.decode()}'
			)
		else:
			print(f'[green bold]Successfully run[/green bold] "{command}"'.strip())

		return result.returncode

	@staticmethod
	def change_directory(path: str):
		"""
		Change current directory

		:param		path:  The path
		:type		path:  str
		"""
		os.chdir(path)
		print_message("CHANGE DIRECTORY", f"[bold]Directory changed: {path}[/bold]")


def validate_project_name(project_name: str):
	"""
	Validate project name

	:param		project_name:  The project name
	:type		project_name:  str

	:raises		ValueError:	   invalid project name
	"""
	if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", project_name):
		raise ValueError(
			"Invalid project name. Must start with a letter or underscore and contain only letters, digits, and underscores."
		)


def create_directory(path: Path):
	"""
	Creates a directory if not exist.

	:param		path:  The path
	:type		path:  Path
	"""
	Path(path).mkdir(parents=True, exist_ok=True)
