# medchemfilters

## Overview
`medchemfilters` is a Python-based utility designed to streamline virtual screening in drug discovery. It features `MCFilter`, a comprehensive module for calculating molecular properties and filtering compounds according to well-established pharmaceutical guidelines such as Ro5, Pfizer, and GSK rules.

## Installation

To install and set up `medchemfilters`, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/medchemfilters.git
   cd medchemfilters


2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### In a Jupyter Notebook
For interactive use, such as in a Jupyter notebook, follow this example to utilize the `MCFilter`:

```python
from medchemfilters.ADMET.filters import MCFilter

# Initialize MCFilter with default settings
filter = MCFilter()

# Calculate molecular descriptors for a SMILES string
smiles = "CCO"
results = filter.calculate_des(smiles)
print(results)
```

### Command-Line Interface
`MCFilter` can also be executed from the command line to process either individual SMILES strings or batches from a CSV file:

- **Processing a Single SMILES String:**
  ```bash
  python main.py "CCO"
  ```

- **Processing SMILES from a CSV File:**
  ```bash
  python main.py path/to/input.csv --smiles_column column_name --output path/to/output.csv
  ```

#### Command-Line Options
- `input`: A single SMILES string or the path to a CSV file containing SMILES strings.
- `-c, --smiles_column`: Specifies the column name in the CSV that contains SMILES strings (default: smiles).
- `-o, --output`: Specifies the output file path for processed results. If not provided, results will be displayed in the terminal.
- `-j, --jobs`: The number of parallel jobs for processing (default: 1).
- `-v, --verbose`: Sets the verbosity level of the output (default: 0, silent).

## Requirements
Python 3.9 or higher is required.
All dependencies are listed in the requirements.txt file.

## License
`medchemfilters` is open-source software licensed under the MIT License. See the LICENSE file for more details.

