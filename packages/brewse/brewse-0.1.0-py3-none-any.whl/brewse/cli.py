#!/usr/bin/env python3

import sys
import subprocess
import curses
from dataclasses import dataclass
from typing import List, Dict, Optional
import urllib.request
import json
from pathlib import Path
from datetime import datetime, timedelta
import threading
import time
import termios
import tty


@dataclass
class BrewPackage:
    name: str
    category: str  # 'Formulae' or 'Casks'
    installed: bool = False


@dataclass
class PackageInfo:
    name: str
    version: Optional[str] = None
    description: Optional[str] = None
    homepage: Optional[str] = None
    installed: bool = False
    analytics: Dict[str, int] = None
    artifacts: List[str] = None


class BrewInteractive:
    def __init__(self):
        self.packages: List[BrewPackage] = []
        self.selected_index = 0
        self.scroll_offset = 0  # Add scroll offset tracking
        self.view_mode = "search"
        self.current_package_info: Optional[PackageInfo] = None
        self.search_term = ""
        self.api_base_url = "https://formulae.brew.sh/api"
        # Add cache directory
        self.cache_dir = Path.home() / ".cache" / "brewse"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.is_data_loaded = False
        self.is_loading = False

    def _get_cache_path(self, url: str) -> Path:
        """Generate a cache file path from URL."""
        # Create a filename from the URL (replace special chars with _)
        filename = (
            url.replace("https://", "").replace("/", "_").replace(".", "_") + ".json"
        )
        return self.cache_dir / filename

    def _fetch_json(self, url: str) -> dict:
        """Helper method to fetch and parse JSON from URL with caching."""
        cache_path = self._get_cache_path(url)

        # Check if cache exists and is fresh (less than 24 hours old)
        if cache_path.exists():
            with open(cache_path) as f:
                cached_data = json.load(f)
                cached_time = datetime.fromtimestamp(cached_data["timestamp"])
                if datetime.now() - cached_time < timedelta(hours=24):
                    return cached_data["data"]

        # Only show loading message when actually fetching from network
        if hasattr(self, "stdscr") and self.search_term:
            height, width = self.stdscr.getmaxyx()
            loading_msg = "Loading data..."
            self.stdscr.clear()
            self.stdscr.addstr(
                height // 2, (width - len(loading_msg)) // 2, loading_msg
            )
            self.stdscr.refresh()

        # Fetch fresh data
        try:
            with urllib.request.urlopen(url, timeout=120) as response:
                data = json.loads(response.read())
        except urllib.error.URLError as e:
            raise Exception(
                f"Network error: {e.reason}. Check your internet connection."
            )
        except TimeoutError:
            raise Exception("Request timed out. Server may be slow or unreachable.")

        # Cache the data
        cache_data = {"timestamp": datetime.now().timestamp(), "data": data}
        with open(cache_path, "w") as f:
            json.dump(cache_data, f)

        return data

    def _background_load_data(self):
        """Load initial API data in background."""
        try:
            self.is_loading = True
            # Fetch both datasets
            self._fetch_json(f"{self.api_base_url}/formula.json")
            self._fetch_json(f"{self.api_base_url}/cask.json")
            self.is_data_loaded = True
        finally:
            self.is_loading = False

    def run_brew_search(self, term: str) -> None:
        """Search packages using the Homebrew API."""
        # Reset position when performing new search
        self.selected_index = 0
        self.scroll_offset = 0
        self.search_term = term
        # Wait for data to be loaded if necessary
        while not self.is_data_loaded:
            if not self.is_loading:
                # If not currently loading, start the load
                self.is_loading = True
                self._fetch_json(f"{self.api_base_url}/formula.json")
                self._fetch_json(f"{self.api_base_url}/cask.json")
                self.is_data_loaded = True
            else:
                # Show loading message while waiting
                height, width = self.stdscr.getmaxyx()
                loading_msg = "Downloading all package data... (this may take a while)"
                self.stdscr.clear()
                self.stdscr.addstr(
                    height // 2, (width - len(loading_msg)) // 2, loading_msg
                )
                self.stdscr.refresh()
                time.sleep(0.1)  # Small delay to prevent CPU spinning

        try:
            # Use cached data from the files
            formulae = self._fetch_json(f"{self.api_base_url}/formula.json")
            casks = self._fetch_json(f"{self.api_base_url}/cask.json")

            self.packages = []

            # Search formulae
            for formula in formulae:
                if term.lower() in formula["name"].lower():
                    self.packages.append(
                        BrewPackage(
                            name=formula["name"],
                            category="Formulae",
                            installed=self._is_installed(formula),
                        )
                    )

            # Search casks
            for cask in casks:
                if term.lower() in cask["token"].lower():
                    self.packages.append(
                        BrewPackage(
                            name=cask["token"],
                            category="Casks",
                            installed=self._is_installed(cask),
                        )
                    )

        except Exception as e:
            print(f"Error fetching search results: {str(e)}")

    def get_package_info(self, package: BrewPackage) -> PackageInfo:
        """Fetch package information using the Homebrew API."""
        try:
            # Determine if it's a formula or cask
            endpoint = "formula" if package.category == "Formulae" else "cask"
            url = f"{self.api_base_url}/{endpoint}/{package.name}.json"

            data = self._fetch_json(url)

            info = PackageInfo(name=package.name)

            if endpoint == "formula":
                info.version = data.get("versions", {}).get("stable")
                info.description = data.get("desc")
                info.homepage = data.get("homepage")
                info.installed = self._is_installed(data)

                # Helper function to safely parse analytics numbers
                def parse_analytics_value(value) -> int:
                    if isinstance(value, int):
                        return value
                    if isinstance(value, str):
                        return int(value.replace(",", ""))
                    return 0

                # Get analytics data
                analytics = data.get("analytics", {}).get("install", {})
                info.analytics = {
                    "30 days": parse_analytics_value(
                        analytics.get("30d", {}).get(package.name, 0)
                    ),
                    "90 days": parse_analytics_value(
                        analytics.get("90d", {}).get(package.name, 0)
                    ),
                    "365 days": parse_analytics_value(
                        analytics.get("365d", {}).get(package.name, 0)
                    ),
                }
            else:  # cask
                info.version = data.get("version")
                info.description = data.get("desc")
                info.homepage = data.get("homepage")
                info.installed = self._is_installed(data)

                # Helper function to safely parse analytics numbers
                def parse_analytics_value(value) -> int:
                    if isinstance(value, int):
                        return value
                    if isinstance(value, str):
                        return int(value.replace(",", ""))
                    return 0

                # Get analytics data
                analytics = data.get("analytics", {}).get("install", {})
                info.analytics = {
                    "30 days": parse_analytics_value(
                        analytics.get("30d", {}).get(package.name, 0)
                    ),
                    "90 days": parse_analytics_value(
                        analytics.get("90d", {}).get(package.name, 0)
                    ),
                    "365 days": parse_analytics_value(
                        analytics.get("365d", {}).get(package.name, 0)
                    ),
                }

            return info

        except Exception as e:
            return PackageInfo(
                name=package.name, description=f"Error fetching info: {str(e)}"
            )

    def _is_installed(self, package_data: dict) -> bool:
        """Helper method to check if a package is installed."""
        try:
            result = subprocess.run(
                [
                    "brew",
                    "list",
                    "--formula" if package_data.get("formula") else "--cask",
                ],
                capture_output=True,
                text=True,
            )
            installed_packages = result.stdout.splitlines()
            return (
                # package_data.get("name", package_data.get("token", "")).lower()
                package_data.get("token") in installed_packages
            )
        except subprocess.SubprocessError:
            return False

    def draw_screen(self, stdscr) -> None:
        """Draw the current screen based on view mode."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if self.view_mode == "search":
            self.draw_search_results(stdscr, height, width)
        else:  # info mode
            self.draw_package_info(stdscr, height, width)

        stdscr.refresh()

    def draw_header(self, stdscr, title: str, width: int) -> int:
        """Draw a consistent header and return the line number after the header."""
        # Draw title bar
        header_bar = "=" * width
        title_pos = (width - len(title)) // 2  # Center the title

        stdscr.addstr(0, 0, header_bar, curses.A_BOLD)
        stdscr.addstr(1, title_pos, title, curses.A_BOLD)
        stdscr.addstr(2, 0, header_bar, curses.A_BOLD)

        return 4  # Return the line number after the header

    def draw_search_results(self, stdscr, height: int, width: int) -> None:
        """Draw the search results screen."""
        current_line = self.draw_header(stdscr, "Brewse: Homebrew Search", width)

        # Draw search term and result count
        search_info = f"Search Results for '{self.search_term}'"
        count_info = f"({len(self.packages)} found)"

        stdscr.addstr(current_line, 2, search_info)
        # Add count in gray (using dim attribute)
        stdscr.addstr(current_line, 2 + len(search_info) + 1, count_info, curses.A_DIM)
        current_line += 2

        # Calculate available lines for results
        available_lines = height - current_line - 1  # -1 for footer

        # Sort all packages together alphabetically
        self.packages.sort(key=lambda p: p.name.lower())

        # Adjust scroll_offset to keep selected item visible
        visible_area = available_lines - 2  # Account for search term line
        if self.selected_index - self.scroll_offset >= visible_area:
            self.scroll_offset = self.selected_index - visible_area + 1
        elif self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index

        # Ensure scroll offset stays within valid range
        max_scroll = max(0, len(self.packages) - visible_area + 1)
        self.scroll_offset = min(max(0, self.scroll_offset), max_scroll)

        # Draw packages
        current_package_idx = 0
        visible_line = 0

        for package in self.packages:
            if visible_line >= self.scroll_offset:
                if current_line >= height - 1:
                    break
                prefix = "✔ " if package.installed else "  "
                # Make the category suffix gray
                category_suffix = (
                    "(formula)" if package.category == "Formulae" else "(cask)"
                )

                if current_package_idx == self.selected_index:
                    # Selected line
                    stdscr.addstr(
                        current_line, 4, prefix + package.name, curses.A_REVERSE
                    )
                    stdscr.addstr(
                        current_line,
                        4 + len(prefix + package.name) + 1,
                        category_suffix,
                        curses.A_REVERSE | curses.A_DIM,
                    )
                else:
                    # Normal line
                    stdscr.addstr(current_line, 4, prefix + package.name)
                    stdscr.addstr(
                        current_line,
                        4 + len(prefix + package.name) + 1,
                        category_suffix,
                        curses.A_DIM,
                    )

                current_line += 1
            current_package_idx += 1
            visible_line += 1

        # Update footer
        footer = (
            "↑/↓: Navigate | Enter: Show Info | q: Quit | i: Install | n: New Search"
        )
        try:
            stdscr.addstr(height - 1, 0, footer[: width - 1], curses.A_BOLD)
        except curses.error:
            pass

    def draw_package_info(self, stdscr, height: int, width: int) -> None:
        """Draw the package info screen."""
        if not self.current_package_info:
            return

        current_line = self.draw_header(stdscr, "Package Information", width)

        # Draw package name
        stdscr.addstr(current_line, 2, f"Package: {self.current_package_info.name}")
        current_line += 2

        # Draw info
        info = self.current_package_info

        def add_line(label: str, value: str) -> None:
            nonlocal current_line
            if current_line >= height - 2:
                return
            try:
                stdscr.addstr(current_line, 2, f"{label}: ", curses.A_BOLD)
                stdscr.addstr(f"{value}"[: width - len(label) - 5])
                current_line += 1
            except curses.error:
                pass

        # Add installed status at the top of the info
        add_line("Status", "✔ Installed" if info.installed else "Not installed")

        if info.version:
            add_line("Version", info.version)
        if info.homepage:
            add_line("Homepage", info.homepage)
        if info.description:
            add_line("Description", info.description)
        if info.analytics:
            current_line += 1
            add_line("Analytics", "")
            for period, count in info.analytics.items():
                add_line(f"  {period}", f"{count} installs")

        # Update the footer text to include uninstall option
        footer = "←: Back | i: Install | u: Uninstall | q: Quit"
        try:
            stdscr.addstr(height - 1, 0, footer[: width - 1], curses.A_BOLD)
        except curses.error:
            pass

    def install_package(self) -> None:
        """Install the currently selected package."""
        if self.view_mode == "search":
            package = self.packages[self.selected_index]
        else:
            package = next(
                p for p in self.packages if p.name == self.current_package_info.name
            )

        curses.endwin()  # End curses mode before running brew
        subprocess.run(["brew", "install", package.name])
        print("\nPress any key to exit...")
        # Save terminal settings
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            # Set terminal to raw mode
            tty.setraw(sys.stdin.fileno())
            # Read a single character
            sys.stdin.read(1)
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        sys.exit(0)

    def uninstall_package(self) -> None:
        """Uninstall the currently selected package."""
        if self.view_mode == "search":
            package = self.packages[self.selected_index]
        else:
            package = next(
                p for p in self.packages if p.name == self.current_package_info.name
            )

        curses.endwin()  # End curses mode before running brew
        subprocess.run(["brew", "uninstall", package.name])
        print("\nPress any key to exit...")
        # Save terminal settings
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            # Set terminal to raw mode
            tty.setraw(sys.stdin.fileno())
            # Read a single character
            sys.stdin.read(1)
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        sys.exit(0)

    def handle_input(self, stdscr) -> bool:
        """Handle user input. Returns False if should exit."""
        height, width = stdscr.getmaxyx()
        key = stdscr.getch()

        if key == ord("q"):
            return False
        elif key in (ord("\b"), curses.KEY_BACKSPACE, 127, 8):
            if self.view_mode == "info":
                self.view_mode = "search"
                self.current_package_info = None
            elif self.view_mode == "search":
                self.scroll_offset = 0
                stdscr.clear()
                stdscr.refresh()
                self.main(stdscr, None)
            return True
        elif key == ord("i"):
            self.install_package()  # This will now handle everything including exit
        elif key == ord("u"):
            self.uninstall_package()  # This will now handle everything including exit
        elif key == ord("/"):  # Quick search
            self.scroll_offset = 0
            self.main(stdscr, None)
            return True
        elif key == ord("h"):  # Show help
            self.view_mode = "help"
            return True
        elif key == ord(" "):  # Page down
            self.selected_index = min(
                len(self.packages) - 1, self.selected_index + (height - 5)
            )
        elif self.view_mode == "search" and key == ord("n"):
            self.scroll_offset = 0  # Reset scroll offset
            self.main(stdscr, None)
            return True
        elif self.view_mode == "search":
            if key == curses.KEY_UP and self.selected_index > 0:
                self.selected_index -= 1
            elif (
                key == curses.KEY_DOWN and self.selected_index < len(self.packages) - 1
            ):
                self.selected_index += 1
            elif key == curses.KEY_PPAGE:  # Page Up
                self.selected_index = max(0, self.selected_index - (height - 5))
            elif key == curses.KEY_NPAGE:  # Page Down
                self.selected_index = min(
                    len(self.packages) - 1, self.selected_index + (height - 5)
                )
            elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
                self.current_package_info = self.get_package_info(
                    self.packages[self.selected_index]
                )
                self.view_mode = "info"
        elif self.view_mode == "info":
            if key == curses.KEY_LEFT:  # Add left arrow for consistency
                self.view_mode = "search"
                self.current_package_info = None

        return True

    def main(self, stdscr, search_term: Optional[str]) -> None:
        """Main application loop."""
        self.stdscr = stdscr
        self.search_term = search_term
        # Reset position when starting new search
        self.selected_index = 0
        self.scroll_offset = 0

        # Setup curses
        curses.curs_set(0)
        stdscr.keypad(1)

        # Initialize colors here, after curses is started
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()

        # Start background loading if not already loaded
        if not self.is_data_loaded and not self.is_loading:
            thread = threading.Thread(target=self._background_load_data)
            thread.daemon = True
            thread.start()

        if search_term is None:
            height, width = stdscr.getmaxyx()
            title = "Brewse: Homebrew Search"
            input_width = 30  # Define fixed input width

            while True:
                stdscr.clear()

                # Draw fancy border
                self.draw_header(stdscr, title, width)

                # Center the content vertically
                content_start = (height - 6) // 2

                # Draw prompt with a box around it
                prompt = "Search anywhere in name:"
                prompt_x = (width - len(prompt)) // 2  # Center the prompt
                input_x = (width - input_width) // 2  # Center the input field

                # Initialize input variables
                search_input = ""

                # Define instructions
                instructions = ["Press Enter to search", "Press Ctrl+C to quit"]

                # Draw prompt above the input field
                stdscr.addstr(content_start, prompt_x, prompt)

                while True:
                    # Redraw the input field with a line of spacing
                    stdscr.addstr(
                        content_start + 2,
                        input_x,
                        " " * input_width,
                        curses.A_UNDERLINE,
                    )

                    # Center the text within the input field
                    if search_input:
                        text_start = input_x + (input_width - len(search_input)) // 2
                        stdscr.addstr(content_start + 2, text_start, search_input)
                        cursor_x = text_start + len(search_input)
                    else:
                        cursor_x = input_x + (input_width // 2)

                    # Draw instructions centered
                    for i, instruction in enumerate(instructions):
                        instr_x = (width - len(instruction)) // 2
                        stdscr.addstr(content_start + 4 + i, instr_x, instruction)

                    # Move cursor to correct position
                    stdscr.move(content_start + 2, cursor_x)
                    stdscr.refresh()

                    # Get input
                    try:
                        ch = stdscr.getch()
                    except KeyboardInterrupt:
                        return

                    if ch in (curses.KEY_ENTER, 10, 13):  # Enter key
                        if search_input:
                            break
                    elif ch in (curses.KEY_BACKSPACE, 127, 8):  # Backspace
                        if search_input:
                            search_input = search_input[:-1]
                    elif ch == curses.KEY_RESIZE:
                        height, width = stdscr.getmaxyx()
                        stdscr.clear()
                    elif 32 <= ch <= 126:  # Printable characters
                        if len(search_input) < input_width - 2:  # Leave some padding
                            search_input += chr(ch)

                curses.noecho()
                curses.curs_set(0)

                if search_input:
                    self.run_brew_search(search_input)
                    break
        else:
            self.run_brew_search(search_term)

        # Continue with the rest of the UI loop
        while True:
            self.draw_screen(stdscr)
            if not self.handle_input(stdscr):
                break


def main():
    """Entry point for the CLI."""
    app = BrewInteractive()
    if len(sys.argv) < 2:
        curses.wrapper(lambda stdscr: app.main(stdscr, None))
    else:
        search_term = sys.argv[1]
        curses.wrapper(lambda stdscr: app.main(stdscr, search_term))


if __name__ == "__main__":
    main()
