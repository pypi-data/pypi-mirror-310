import sys
import time
from termcolor import colored
from itertools import cycle
import shutil


class CmdGUI:
    """
    A comprehensive command-line GUI toolkit for enhanced visualization.
    Includes utilities for progress bars, spinners, heatmaps, tables, status updates, and more.
    """

    def __init__(self, enable_color=True):
        """
        Initialize CmdGUI with options to enable or disable colored output.
        Args:
            enable_color (bool): Whether to enable colored output (default is True).
        """
        self.enable_color = enable_color
        self.terminal_width = shutil.get_terminal_size().columns

    def _apply_color(self, text, color, on_color=None, attrs=None):
        """Apply color to text if coloring is enabled."""
        if self.enable_color:
            return colored(text, color, on_color, attrs)
        return text

    ### PROGRESS BAR ###
    def progress_bar(self, percentage, length=30, color='green', text='', show_percentage=True, show_time=False, start_time=None):
        """
        Display a customizable progress bar.
        Args:
            percentage (float): Percentage of progress (0-100).
            length (int): Total length of the progress bar.
            color (str): Color for the progress bar (using termcolor colors).
            text (str): Additional text to display next to the progress bar.
            show_percentage (bool): Whether to show percentage progress (default True).
            show_time (bool): Whether to display elapsed time.
            start_time (float): Start time (required if show_time=True).
        """
        bar_length = int((percentage / 100) * length)
        bar = self._apply_color("█" * bar_length, color) + '-' * (length - bar_length)
        percentage_text = f"{percentage:.2f}%" if show_percentage else ""
        time_text = ""
        if show_time and start_time:
            elapsed = time.time() - start_time
            time_text = f" Elapsed: {elapsed:.1f}s"
        sys.stdout.write(f"\r[{bar}] {percentage_text} {text}{time_text}")
        sys.stdout.flush()

    ### SPINNER ###
    def spinner(self, duration=5, message='Loading', color='cyan', interval=0.1, multi_line=False):
        """
        Display a spinner animation for a specified duration.
        Args:
            duration (int): Duration in seconds for the spinner to run.
            message (str): Message to display next to the spinner.
            color (str): Color of the spinner (using termcolor colors).
            interval (float): Time in seconds between spinner updates.
            multi_line (bool): Whether to display multiple spinners for concurrent tasks.
        """
        spinner_cycle = cycle(['|', '/', '-', '\\'])
        end_time = time.time() + duration
        while time.time() < end_time:
            if multi_line:
                sys.stdout.write(f"\r{self._apply_color(next(spinner_cycle), color)} Task 1\n")
                sys.stdout.write(f"{self._apply_color(next(spinner_cycle), color)} Task 2\n")
            else:
                sys.stdout.write(f"\r{self._apply_color(next(spinner_cycle), color)} {message}")
            sys.stdout.flush()
            time.sleep(interval)
        if multi_line:
            sys.stdout.write("\r" + ' ' * (self.terminal_width) + '\n' * 2)  # Clear lines
        else:
            sys.stdout.write("\r" + ' ' * (len(message) + 4) + '\r')  # Clear line
        sys.stdout.flush()

    ### STATUS INDICATORS ###
    def status(self, message, status="success"):
        """
        Display a status update with an icon.
        Args:
            message (str): The status message.
            status (str): The status type (e.g., 'success', 'error', 'warning').
        """
        icons = {
            "success": self._apply_color("✔", "green"),
            "error": self._apply_color("✘", "red"),
            "warning": self._apply_color("⚠", "yellow"),
            "info": self._apply_color("ℹ", "blue")
        }
        icon = icons.get(status, self._apply_color("?", "white"))
        print(f"{icon} {message}")

    ### HEATMAP ###
    def heatmap(self, data, min_value=None, max_value=None, colors=None):
        """Display a heatmap for a list of values or a string."""
        if isinstance(data, str):
            data = [ord(char) for char in data]
        min_value = min_value if min_value is not None else min(data)
        max_value = max_value if max_value is not None else max(data)

        colors = colors or ['on_red', 'on_yellow', 'on_green', 'on_cyan', 'on_blue', 'on_magenta', 'on_white']
        range_step = (max_value - min_value) / (len(colors) - 1)

        def get_color(value):
            index = int((value - min_value) / range_step)
            return colors[min(index, len(colors) - 1)]

        heatmap = ""
        for value in data:
            color = get_color(value)
            heatmap += self._apply_color(f"{value}", 'white', color) + ' '
        print(heatmap)

    ### ASCII TABLE ###
    def ascii_table(self, data, headers=None, col_width=15, colors=None):
        """Display a table in the terminal with ASCII styling and optional colors."""
        def format_row(row, row_colors=None):
            formatted = ""
            for idx, cell in enumerate(row):
                color = row_colors[idx] if row_colors else 'white'
                formatted += self._apply_color(str(cell).ljust(col_width), color) + "|"
            return formatted

        border = "+" + ("-" * col_width + "+") * (len(headers) if headers else len(data[0]))
        if headers:
            print(border)
            print(format_row(headers))
        print(border)
        for row_idx, row in enumerate(data):
            row_colors = colors[row_idx] if colors else None
            print(format_row(row, row_colors))
        print(border)

    ### LOGGING ###
    def log(self, message, level="info"):
        """
        Display a log message with a timestamp and level.
        Args:
            message (str): The log message.
            level (str): Log level (e.g., 'info', 'warn', 'error').
        """
        levels = {
            "info": ("INFO", "blue"),
            "warn": ("WARN", "yellow"),
            "error": ("ERROR", "red")
        }
        level_text, color = levels.get(level, ("LOG", "white"))
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{self._apply_color(f'[{timestamp}] {level_text}:', color)} {message}")
