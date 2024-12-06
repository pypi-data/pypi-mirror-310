# <img src="./img/valdata_logo.png" width="30" height="23"> valdata README

`valdata` is a robust Python package developed to streamline data validation and consistency checks across various data structures and environments, particularly those used in financial and risk analysis. By providing structured data insights, comparisons, and file management capabilities, `valdata` simplifies data analysis and improves data quality assurance processes.

## Features

- **Compatibility with Pandas and Spark DataFrames**: Ensures easy integration with common data structures.
- **Detailed Data Insights**: View unique values, data types, and column composition for better data understanding.
- **Data Consistency Checks**: Compare multiple DataFrames for equality, validate variables, and analyze column-specific occurrences and concentrations.
- **Flexible File Management**: Seamlessly work with directories and modules, allowing for more efficient data processing.
- **System Compatibility**: Detects versions of relevant software, such as Hadoop, Spark, and PySpark, to help ensure compatibility in distributed computing environments.

## Use Cases

- **Financial Analysis**: Validate data from multiple sources, ensuring consistent and accurate datasets for risk assessments or portfolio analysis.
- **Data Audits**: Identify and troubleshoot discrepancies in datasets, especially for large data teams.
- **Risk Management**: Monitor data for anomalies, rare occurrences, or threshold-based concentrations in high-risk datasets.
- **Data Pipeline Debugging**: Detect and correct schema mismatches or data quality issues within ETL (Extract, Transform, Load) processes.

## Installation

All required dependencies are installed automatically when you install `valdata` using `pip`. You don’t need to worry about manually installing them, as `pip` will handle this for you. Simply run:

```bash
pip install valdata
```

Then to load the package you can use:

```bash
import valdata as vd
```

## Requirements
Since Spark-based operations are part of the library functionality, you **must** have a pre-configured and working PySpark and Hadoop environment. While the `pyspark` library is included as a dependency, the actual setup of Spark and Hadoop (e.g., installing and configuring the Spark cluster) is not handled by `valdata`.

## Resources and Documentation

Explore the following resources to learn more about **valdata**:

- 📦 **Package Installer**: [PyPI](https://pypi.org/project/valdata/)  
  Find the package, installation instructions, and release history.

- 📖 **Documentation**: [Read the Docs](https://valdata.readthedocs.io/en/latest/index.html)  
  Comprehensive guides and usage examples.

- 📓 **Jupyter Notebook Example**: [jupyter_testing.ipynb](https://github.com/GabrielGod1/valdata/blob/master/jupyter_testing.ipynb)  
  Interactive examples showcasing the main features and capabilities of the library.

## Modules Overview

### Auxiliary
This module provides utility functions for type checking, path correction, and timezone-aware datetime retrieval. These functions are particularly useful within the library, enabling seamless integration with other module components.

- `check_type()`: Checks the type of an object.
- `now_timedelta()`: Provides a timezone-aware current datetime.
- `path_correction()`: Corrects file paths for compatibility across systems.

### Utils
This module includes utility functions for managing directories, displaying system information, and integrating with Spark. It provides tools for checking and creating directories, listing contents, managing Python module paths, and retrieving version details for Hadoop, Spark, and PySpark.

- `add_module_path()`: Adds a module path dynamically.
- `check_directory()`: Verifies the existence of a directory and creates it if necessary.
- `get_directories()`: Lists all directories in a given path.
- `get_hadoop_version()`: Retrieves the current Hadoop version.
- `get_modules()`: Lists Python modules in a specified directory.
- `read_file()`: Reads the content of a file. *(Todo!!!)*
- `save_file()`: Saves content to a file. *(Todo!!!)*

### **Validation**
This module is designed for DataFrame analysis and comparison, supporting both Pandas and Spark DataFrames (in some functions, lists are supported). It includes functions to track execution time, print DataFrame summaries, compare DataFrames, and tabulate various statistics. Operations such as counting unique values, checking variable consistency, and comparing DataFrames element-wise or by structure are also supported.

- `check_variables()`: Validates the consistency of variables in a DataFrame.
- `equal_df()`: Compares two DataFrames for equality.
- `equal_df_mult()`: Compares multiple DataFrames against a reference DataFrame.
- `get_overview()`: Provides an overview of a DataFrame, including column statistics.
- `get_pandas_schemaStr()`: Returns the schema of a Pandas DataFrame in a readable format.
- `now()`: Returns the current timestamp.
- `show_pandas_as_table()`: Displays a Pandas DataFrame as a formatted table.
- `tblt_concentrations()`: Analyzes data concentrations above given thresholds.
- `tblt_ocurrences()`: Counts occurrences of specific values in columns.
- `tms_0()`: Tracks start time for operations.
- `tms_1()`: Tracks end time for operations and calculates elapsed time.
- `unique_values()`: Lists unique values for each column in a DataFrame.

### Visuals
This module defines various utility functions and styles for text formatting and Jupyter Notebook customization. It includes a variety of text styles for better visual representation of outputs.

- `TextStyle`: A class providing pre-defined text styles.
  - `TextStyle.BLACK`, `TextStyle.BLUE`, `TextStyle.BOLD`, `TextStyle.CYAN`, `TextStyle.GREEN`, `TextStyle.ITALIC`, `TextStyle.MAGENTA`, `TextStyle.RED`, `TextStyle.RESET`, `TextStyle.UNDERLINE`, `TextStyle.WHITE`, `TextStyle.YELLOW`.
- `b()`: Formats text in bold.
- `b_bl()`: Formats text in bold and blue.
- `b_gr()`: Formats text in bold and green.
- `b_re()`: Formats text in bold and red.
- `set_start()`: Initializes a custom in-house Jupyter Notebook visuals template, displays a personalized message, and prints the current timestamp. This function is designed to streamline the setup process at the beginning of any Python notebook, providing a standardized and efficient starting point.

*A detailed application of every function can be found in the ipynb file jupyter_testing.ipynb.*

## Known Issues
None at the moment. Please report any issues you find on the GitHub repository.

## Release Notes

### 0.0.1
**Initial Release**:
The first version of `valdata` introduces key functionality divided into four main modules:

- **Auxiliary**: Offers essential utility functions for type checking, path correction, and timezone-aware datetime handling, ensuring smooth integration with other components.
- **Utils**: Provides tools for managing directories, checking system configurations, and integrating with Spark, including directory creation, module path management, and version retrieval for Hadoop and Spark.
- **Validation**: Delivers robust DataFrame analysis and comparison tools, supporting both Pandas and Spark DataFrames. Key features include data consistency checks, variable validation, summary statistics, and concentration analysis.
- **Visuals**: Enhances output presentation with customizable text styles and templates for Jupyter Notebooks, enabling visually appealing and organized data representations.

## Contact
- **Author**: GabrielGod1
- **GitHub**: [GabrielGod1](https://github.com/GabrielGod1)
- **Email**: altGeneric@hotmail.com








