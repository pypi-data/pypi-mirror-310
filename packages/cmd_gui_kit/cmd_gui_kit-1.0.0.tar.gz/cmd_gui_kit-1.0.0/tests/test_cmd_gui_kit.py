import time
from cmd_gui_kit import CmdGUI

def test_progress_bar():
    print("\nTesting Progress Bar:")
    gui = CmdGUI()
    start_time = time.time()
    for i in range(101):
        gui.progress_bar(i, text="Progressing...", show_time=True, start_time=start_time)
        time.sleep(0.03)
    print("\nProgress Bar Test Completed.\n")


def test_spinner():
    print("\nTesting Spinner:")
    gui = CmdGUI()
    gui.spinner(duration=3, message="Loading Spinner Test", color="yellow")
    print("Spinner Test Completed.\n")


def test_status():
    print("\nTesting Status Indicators:")
    gui = CmdGUI()
    gui.status("Operation was successful.", status="success")
    gui.status("There was an error in the process.", status="error")
    gui.status("This is a warning message.", status="warning")
    gui.status("Some additional information.", status="info")
    print("Status Indicators Test Completed.\n")


def test_heatmap():
    print("\nTesting Heatmap:")
    gui = CmdGUI()
    test_string = "heatmap example"
    print("Input String:", test_string)
    gui.heatmap(test_string)
    test_values = [1, 2, 3, 10, 50, 100, 255]
    print("Input Values:", test_values)
    gui.heatmap(test_values)
    print("Heatmap Test Completed.\n")


def test_ascii_table():
    print("\nTesting ASCII Table:")
    gui = CmdGUI()
    headers = ["Name", "Age", "Score"]
    data = [
        ["Alice", 30, 95],
        ["Bob", 25, 80],
        ["Charlie", 35, 100],
    ]
    colors = [
        ["yellow", "green", "blue"],
        ["red", "cyan", "magenta"],
        ["white", "green", "yellow"],
    ]
    gui.ascii_table(data, headers=headers, colors=colors)
    print("ASCII Table Test Completed.\n")


def test_logging():
    print("\nTesting Logging:")
    gui = CmdGUI()
    gui.log("This is an informational message.", level="info")
    gui.log("This is a warning message.", level="warn")
    gui.log("This is an error message.", level="error")
    print("Logging Test Completed.\n")


def main():
    print("\n=== CmdGUI Test Suite ===\n")
    test_progress_bar()
    test_spinner()
    test_status()
    test_heatmap()
    test_ascii_table()
    test_logging()
    print("\n=== All Tests Completed Successfully ===\n")


if __name__ == "__main__":
    main()
