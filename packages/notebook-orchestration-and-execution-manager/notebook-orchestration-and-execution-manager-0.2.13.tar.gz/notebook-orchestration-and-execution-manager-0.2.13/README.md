# notebook-orchestration-and-execution-manager
Orchestrate Jupyter notebooks by passing parameters dynamically between them. This solution enables seamless execution, where the output of one notebook becomes the input for the next. Includes automated execution, parameter injection, logging, and output management for streamlined workflows.


# Notebook Execution and Variable Extraction

This project provides a Python class and workflow to manage the execution of Jupyter notebooks with parameters, extract variables and their values from executed notebooks, and display the results in a structured format.

## Features
- **Execute Jupyter Notebooks**: Run Jupyter notebooks with specified parameters using `papermill`.
- **Dynamic Parameter Passing**: Pass custom parameters to notebooks during execution.
- **Variable Extraction**: Extract variable data (name, operation, and value) from executed notebook cells.
- **Logging**: Track execution steps with detailed logs.
- **Directory Management**: Automatically manage output directories for processed notebooks.


## Requirements
- Python 3.6+
- Libraries: `os`, `papermill`, `logging`, `ast`, `IPython`

Install dependencies via pip:
```bash
pip install notebook-orchestration-and-execution-manager
```

---

## Usage

### 1. Initialize the NotebookOrchestationExecutionManager
Create an instance of `NotebookOrchestationExecutionManager`, specifying the directory for processed notebooks.

```python
from notebook_orchestation_execution_manager import NotebookOrchestationExecutionManager

processor = NotebookOrchestationExecutionManager(processed_directory="./processed_notebook")
```

### 1.1 Parameters Definition

The recommended practice is to define parameters in the first cell of the notebook. This ensures a clear structure, makes them easy to locate, and provides a centralized configuration that can be used throughout the notebook's execution.

Parameters can be defined in a Markdown, Raw, or Code cell, or even without explicitly defining a cell for this purpose. Parameter injection will automatically take place above the first code cell in the notebook. This provides greater flexibility when working with parameterization tools like Papermill or automating notebook execution in configurable environments.

#### In Mardown Cell
![Execute Notebooks](https://raw.githubusercontent.com/JorgeCardona/notebook-orchestration-and-execution-manager/refs/heads/main/images/orchestration_1.png)

#### In Code Cell
![Execute Notebooks](https://raw.githubusercontent.com/JorgeCardona/notebook-orchestration-and-execution-manager/refs/heads/main/images/orchestration_3.png)

#### No Definition Cell
![Execute Notebooks](https://raw.githubusercontent.com/JorgeCardona/notebook-orchestration-and-execution-manager/refs/heads/main/images/orchestration_5.png)


### 1.2 Parameters Injection
![Execute Notebooks](https://raw.githubusercontent.com/JorgeCardona/notebook-orchestration-and-execution-manager/refs/heads/main/images/orchestration_2.png)

![Execute Notebooks](https://raw.githubusercontent.com/JorgeCardona/notebook-orchestration-and-execution-manager/refs/heads/main/images/orchestration_4.png)

![Execute Notebooks](https://raw.githubusercontent.com/JorgeCardona/notebook-orchestration-and-execution-manager/refs/heads/main/images/orchestration_6.png)


### 2. Define Notebooks and Parameters
Provide a list of notebooks with input paths, output paths, and parameter dictionaries.

![Notebooks](https://raw.githubusercontent.com/JorgeCardona/notebook-orchestration-and-execution-manager/refs/heads/main/images/notebooks.png)

```python
notebooks_with_parameters = [
    ("./sample_notebooks/1_Add.ipynb", "./processed_notebook/add_executed.ipynb", {"params": [10, 5, 7]}),
    ("./sample_notebooks/4_Divide.ipynb", "./processed_notebook/divide_executed.ipynb", {"x": 20, "y": 0}),
    ("./sample_notebooks/2_Subtract.ipynb", "./processed_notebook/subtract_executed.ipynb", {"x": 10, "y": 3}),
    ("./sample_notebooks/3_Multiply.ipynb", "./processed_notebook/multiply_executed.ipynb", {"inject_values": {"x": [2, 3], "y": [4, 5]}}),
    ("./sample_notebooks/5_No_parameters.ipynb", "./processed_notebook/no_parameters_executed.ipynb", {"inject_values": {"x": [2, 3], "y": [4, 5]}}),
]
```

### 3. Execute Notebooks
Run each notebook with parameters and save the results.

```python
notebook_execution_results = []
for input_path, output_path, params in notebooks_with_parameters:
    notebook_results = processor.run_notebook_with_parameters(input_path, output_path, params)
    notebook_execution_results.append(notebook_results)
```
![Execute Notebooks](https://raw.githubusercontent.com/JorgeCardona/notebook-orchestration-and-execution-manager/refs/heads/main/images/pass_notebook_parameters.png)

### 4. Extract Variables from Notebooks
Extract variable data and display it in a structured format.

```python
for notebook_result in notebook_execution_results:
    if notebook_result:
        extracted_data = processor.extract_variable_data_from_notebook_cells(notebook_result)
        processor.display_notebook_variables_and_values_extracted_from_notebook(extracted_data)
```
![Extract Variables](https://raw.githubusercontent.com/JorgeCardona/notebook-orchestration-and-execution-manager/refs/heads/main/images/extract_notebook_variables.png)

---

## Code Breakdown

### 1. NotebookOrchestationExecutionManager Class
Handles the execution of notebooks, directory creation, and variable extraction.

#### Methods
- **`create_directory_if_not_exists(directory: str)`**: Ensures the specified directory exists.
- **`run_notebook_with_parameters(notebook_input_path: str, notebook_output_path: str, params: dict)`**: Executes a Jupyter notebook with parameters.
- **`extract_variable_data_from_notebook_cells(notebook_data: dict)`**: Extracts variable data from notebook cells.
- **`display_notebook_variables_and_values_extracted_from_notebook(extracted_variables_data_from_notebook: dict)`**: Displays extracted variable data in logs.

---

## Example Workflow

### Input Notebook
- File: `1_Add.ipynb`
- Parameters: `{"params": [10, 5, 7]}`

### Output
- File: `./processed_notebook/add_executed.ipynb`
- Logs: Execution details and extracted variables.

---

## Logging
Logs include:
- Notebook execution status.
- Variable extraction details.
- Metadata from executed notebooks.

---

## License
This project is licensed under the MIT License.
```