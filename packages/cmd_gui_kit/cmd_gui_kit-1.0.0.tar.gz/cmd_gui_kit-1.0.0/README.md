
# cmd-gui-kit

`cmd-gui-kit` is a Python toolkit for creating enhanced CLI visualizations, including progress bars, spinners, heatmaps, tables, and status indicators. It provides a flexible and modular interface for building visually appealing command-line applications.

## Features
- **Progress Bars:** Dynamic, colored progress bars with percentage and elapsed time.
- **Spinners:** Animated spinners for task progress.
- **Heatmaps:** Visualize character frequencies or numerical data with a heatmap.
- **ASCII Tables:** Create styled tables with custom headers and cell colors.
- **Status Indicators:** Show success, error, warning, and info statuses with icons.
- **Logging:** Real-time logs with levels (INFO, WARN, ERROR) and timestamps.

## Installation

You can install `cmd-gui-kit` via pip:

```bash
pip install cmd-gui-kit
```

## Usage

### Import the Package
```python
from cmd_gui_kit import CmdGUI
gui = CmdGUI()
```

### Progress Bar
```python
import time
for i in range(101):
    gui.progress_bar(i, text="Processing...")
    time.sleep(0.05)
```

### Spinner
```python
gui.spinner(duration=3, message="Loading...")
```

### Heatmap
```python
gui.heatmap("hello world")
```

### ASCII Table
```python
data = [["Alice", 90], ["Bob", 85], ["Charlie", 95]]
headers = ["Name", "Score"]
gui.ascii_table(data, headers=headers)
```

### Status Indicators
```python
gui.status("Operation completed successfully.", status="success")
gui.status("An error occurred.", status="error")
```

### Logging
```python
gui.log("This is an informational message.", level="info")
gui.log("This is a warning message.", level="warn")
gui.log("This is an error message.", level="error")
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
- **Author:** cagatay-softgineer
- **Email:** cagatayalkan.b@gmail.com
- **GitHub:** [https://github.com/cagatay-softgineer/cmd-gui-kit](https://github.com/cagatay-softgineer/cmd-gui-kit)
