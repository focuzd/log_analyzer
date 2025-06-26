# Log Analyzer

A flexible, CLI-based log analysis tool built in Python. Designed for developers, sysadmins, and automation engineers who need to parse, filter, and summarize structured log files quickly and cleanly.

---

## 🚀 Features

- ✅ Filter logs by level (`ERROR`, `INFO`, `DEBUG`, etc.)
- 📊 Output parsed summaries in either CSV or human-readable `.log` format
- 🔍 Extract key metadata: timestamp, level, message, and user (if present)
- 🗃️ Save filtered log lines to `triage.log`
- 🌱 Optional ENV_TAG injection from environment variables (e.g. `dev`, `prod`)
- 📈 Auto-generates `level_summary.log` to show distribution of log levels
- ⚙️ Supports limiting number of lines in summary output

## How to Use It

### Prerequisites

You'll need Python 3 installed on your system.

### Running the Analyzer

1.  **Clone the Repository (or download the files):**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2.  **Run the `analyzer.py` script from your terminal:**

    ```bash
    python analyzer.py --file <path_to_your_log_file> [options]
    ```

### Command-line Arguments

Here are the arguments you can use:

* `--file <path>` (Required): Specifies the path to your input log file.
* `--level <level(s)>` (Optional): Filters the log by specific levels. You can provide a single level (e.g., `INFO`) or multiple levels separated by commas (e.g., `ERROR,WARNING`). If omitted, it will process all lines.
* `--format <format>` (Optional): Sets the output format for the summary. Choose between `log` or `csv`. If not specified, it defaults to `csv`.
* `--tag_env` (Optional): A flag to add an `ENV_TAG` (environment tag) to your output file.
* `--max_lines <number>` (Optional): Limits the number of lines written to the summary file. The default is a very large number (1,000,000).

### Examples

1.  **Analyze a log file and get a CSV summary of all levels:**
    ```bash
    python analyzer.py --file my_application.log --format csv
    ```

2.  **Filter for `ERROR` and `WARNING` messages and output to a custom log format:**
    ```bash
    python analyzer.py --file server.log --level ERROR,WARNING --format log
    ```

3.  **Get a CSV summary of `INFO` messages, include an environment tag, and limit to 500 lines:**
    ```bash
    python analyzer.py --file debug.log --level INFO --format csv --tag_env --max_lines 500
    ```

## Output

The script creates an `output` directory in the same location where you run the script. Inside, you'll find:

* `triage.log`: Contains the lines filtered by the specified `--level`.
* `summary.csv` or `summary.log`: The summarized log information in your chosen format.
* `level_summary.log`: A file listing the counts of each log level found in the original log file.

## Project Structure

* `analyzer.py`: The main script that handles command-line arguments and orchestrates the log analysis.
* `parser.py`: Contains the `LogAnalyzer` class, which handles file reading, filtering, detail extraction, and writing summaries. This is where most of the log parsing logic resides.
* `utils.py`: A small utility file for common functions like ensuring the output directory exists and retrieving environment tags.

## What I Learned

This project was a great way to practice:

* **File I/O**: Reading from and writing to different file formats.
* **Regular Expressions**: Using `re` module for pattern matching and extracting specific information from log lines. This was a fun challenge!
* **Command-line Arguments**: Using `argparse` to make my script more flexible and user-friendly.
* **Modular Programming**: Breaking down the problem into smaller, manageable functions and classes across different files.
* **Error Handling**: Basic checks for file existence and argument validation.

## Future Enhancements (Ideas for later!)

* **More Robust Error Parsing**: Right now, it's pretty basic. I'd like to improve how it extracts different types of errors.
* **JSON Output**: Add an option to output summaries in JSON format.
* **Interactive Mode**: Maybe a simple command-line interface for selecting options.
* **Date/Time Filtering**: Filter logs based on a date range.
* **Configuration File**: Allow users to specify default settings in a config file.

