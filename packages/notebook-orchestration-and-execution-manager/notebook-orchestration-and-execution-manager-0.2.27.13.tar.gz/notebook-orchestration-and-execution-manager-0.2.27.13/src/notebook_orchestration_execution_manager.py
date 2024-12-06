import os
import papermill as pm
import logging
from IPython.display import display, HTML
import ast
import json

# Set up the logging configuration
logging.basicConfig(
    level=logging.INFO,  # You can change the level to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class NotebookOrchestrationExecutionManager:
    def __init__(self, processed_directory: str = "./processed_notebook") -> None:
        """
        Initializes the NotebookOrchestrationExecutionManager with a directory for processed notebooks.

        Args:
            processed_directory (str): Directory to store processed notebooks.
        """
        self.processed_directory = processed_directory

    def create_directory_if_not_exists(self, directory: str) -> None:
        """
        Ensures that the specified directory exists. If it doesn't, the directory is created.

        Parameters:
        directory (str): The path of the directory to check or create.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Directory {directory} created.")

    def run_notebook_with_parameters(self, notebook_input_path: str, notebook_output_path: str, params: dict):
        """
        Executes a Jupyter notebook with the provided parameters, removes any parameter cells from the output, 
        and provides a link to the result.

        This function performs the following steps:
        1. Ensures the directory for processed notebooks exists.
        2. Executes the notebook with the specified input path and parameters.
        3. Removes the parameter cells from the output notebook.
        4. Displays a hyperlink to the result of the executed notebook.

        Parameters:
        notebook_input_path (str): Path to the input Jupyter notebook that will be executed.
        notebook_output_path (str): Path where the output Jupyter notebook will be saved.
        params (dict): A dictionary of parameters to be passed to the notebook during execution.

        Returns:
        execution (pm.execute_notebook): The result of the notebook execution.
        """
        
        # Ensure the processed notebooks directory exists
        self.create_directory_if_not_exists(self.processed_directory)

        logging.info(f"Executing {notebook_input_path} with parameters ⚡ {params} ⚡ ...")
        
        execution = None  # Initialize execution variable to track the result
        
        try:
            # Execute the notebook with the provided parameters, storing the output even in case of error
            execution = pm.execute_notebook(
                input_path=notebook_input_path,
                output_path=notebook_output_path,
                parameters=params,
                store_error=True  # Ensures the notebook is saved even if there are errors during execution
            )

            # Create a hyperlink for the result and display it
            display(HTML(f"✅ Execution successful, check the result at the following link -> <a href='{notebook_output_path}' target='_blank'>{notebook_output_path}</a>"))
            logging.info(f"Execution of {notebook_input_path} was successful.")
        
        except Exception as e:
            # Log and display an error message if the execution fails
            logging.error(f"Error executing {notebook_input_path}: {e}")
            display(HTML(f"❌ Execution failed, check the error details and result at the following link -> <a href='{notebook_output_path}' target='_blank'>{notebook_output_path}</a>"))
        
        finally:
            # Always try to remove the parameter cells, even if the notebook execution failed
            try:
                self.remove_parameter_cells(notebook_output_path)
            except Exception as e:
                logging.error(f"Error removing parameter cells from {notebook_output_path}: {e}")

        # Log the completion of the execution process
        logging.info(f"Execution finished for {notebook_input_path}")

        return execution

    def remove_parameter_cells(self, notebook_output_path):
        """
        Removes all cells containing parameters from the Jupyter notebook.
        
        This function reads the notebook from the specified path, searches for all cells 
        that contain parameters (identified by specific metadata tags), deletes each of 
        those cells, and saves the modified notebook back to the same location.
        
        Parameters:
        notebook_output_path (str): The file path to the Jupyter notebook from which the 
                                    parameter cells will be removed.
        
        The function assumes that the notebook is a valid Jupyter notebook in JSON format, 
        and the parameter cells are marked with 'metadata' and 'tags' containing 'parameters'.
        
        After executing, the notebook will no longer contain any cells with parameters.
        """
        
        # Open the notebook file and load its content
        try:
            with open(notebook_output_path, 'r') as f:
                notebook_updated = json.load(f)
        except Exception as e:
            logging.error(f"Error reading the notebook {notebook_output_path}: {e}")
            return
        
        # Create a list of cells to be deleted
        cells_to_delete = []
        
        # Iterate through the cells in the notebook to find all cells with parameters
        for i, cell in enumerate(notebook_updated['cells']):
            if 'metadata' in cell and 'tags' in cell['metadata'] and 'parameters' in cell['metadata']['tags']:
                cells_to_delete.append(i)  # Collect indices of cells to delete

        if not cells_to_delete:
            logging.info("No parameter-containing cells were found.")
            return

        # Delete all identified parameter cells in reverse order to avoid index shifting
        for i in reversed(cells_to_delete):
            del notebook_updated['cells'][i]

        # Save the updated notebook back to the original path
        try:
            with open(notebook_output_path, 'w') as f:
                json.dump(notebook_updated, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving the updated notebook {notebook_output_path}: {e}")
            return
        
        # Log the number of cells removed
        logging.info(f"{len(cells_to_delete)} parameter-containing cells were removed from {notebook_output_path}.")

    def extract_variable_data_from_notebook_cells(self, notebook_data: dict) -> dict:
        """
        Extracts variable data from the notebook cells and outputs the variable name,
        the operation (source), and the value associated with each variable.

        Args:
            notebook_data (dict): The content of the notebook in dictionary format.

        Returns:
            dict: A dictionary with cell execution count as keys and a dictionary of 
                  'variable_operation', 'variable_name', and 'variable_value'.
        """
        output_values = {}
        metadata = {}

        if notebook_data and isinstance(notebook_data, dict):
            for cell in notebook_data.get('cells', []):
                if cell.get('cell_type') == 'code' and 'outputs' in cell:
                    for output in cell.get('outputs', []):
                        text_plain = output.get('data', {}).get('text/plain')
                        if text_plain:
                            source = cell.get('source', '').strip()

                            if "=" in source:
                                variable_names = [var.strip() for var in source.split("=")[0].split(",")]
                                values = [text_plain.strip()]

                                if len(variable_names) > 1:
                                    if text_plain.strip().startswith('[') or text_plain.strip().startswith('('):
                                        values = text_plain.strip()[1:-1].split(',')
                                    else:
                                        values = text_plain.strip().split(',')
                                    values = [val.strip() for val in values]

                                    for i, variable in enumerate(variable_names):
                                        key = f"cell_{cell.get('execution_count')}_{i + 1}"
                                        output_values[key] = {
                                            "execution_cell_number": f"cell_{cell.get('execution_count')}",
                                            "variable_operation": source,
                                            "variable_name": variable,
                                            "variable_value": values[i] if i < len(values) else None
                                        }
                                else:
                                    output_values[f"cell_{cell.get('execution_count')}"] = {
                                        "execution_cell_number": f"cell_{cell.get('execution_count')}",
                                        "variable_operation": source,
                                        "variable_name": variable_names[0],
                                        "variable_value": values[0]
                                    }
                            else:
                                variable_name = source.split()[0] if source else None
                                output_values[f"cell_{cell.get('execution_count')}"] = {
                                    "execution_cell_number": f"cell_{cell.get('execution_count')}",
                                    "variable_operation": source,
                                    "variable_name": variable_name,
                                    "variable_value": text_plain
                                }
            metadata = notebook_data.get('metadata', {}).get('papermill', {})
            output_values['metadata'] = metadata
        return output_values

    def display_notebook_variables_and_values_extracted_from_notebook(self, extracted_variables_data_from_notebook: dict) -> dict:
        """
        Displays the extracted variables and their values from the notebook.

        Args:
            extracted_variables_data_from_notebook (dict): The extracted variables data.

        Returns:
            dict: A dictionary of variables and their values.
        """
        # Initialize an empty dictionary to store variable names and values
        variables = {}
        
        # Extract metadata from the notebook, if it exists
        metadata = extracted_variables_data_from_notebook.get('metadata', {})
        
        # Check if the input is valid and contains metadata
        if extracted_variables_data_from_notebook and isinstance(extracted_variables_data_from_notebook, dict) and metadata:
            # Log relevant information from the metadata
            logging.info(f"📓 Notebook Name: {metadata.get('input_path', 'N/A').split('/')[-1]}")
            logging.info(f"⚙️ Default Parameters: {metadata.get('default_parameters', 'N/A')}")
            logging.info(f"🔧 Parameters: {metadata.get('parameters', 'N/A')}")
            logging.info(f"🌐 Environment Variables: {metadata.get('environment_variables', 'N/A')}")
            logging.info(f"📥 Input Path: {metadata.get('input_path', 'N/A')}")
            logging.info(f"📤 Output Path: {metadata.get('output_path', 'N/A')}")
            logging.info(f"⚠️ Exception: {metadata.get('exception', 'None')}")
            logging.info("")
            
            # Iterate through each item in the extracted variables from the notebook
            for key, value in extracted_variables_data_from_notebook.items():
                # If the key is not 'metadata' and the value is a dictionary, process it
                if key != 'metadata' and isinstance(value, dict):
                    # Retrieve the variable name and its corresponding value
                    variable_name = value.get('variable_name', None)
                    variable_value = value.get('variable_value', None)
                    
                    # Try to safely parse the variable value using ast.literal_eval
                    try:
                        # Attempt to evaluate the value as a Python literal (list, dict, int, float, etc.)
                        variable_value = ast.literal_eval(str(variable_value))
                    except (ValueError, SyntaxError) as e:
                        # If parsing fails, keep the value as a string and log the error
                        logging.warning(f"⚠️ Failed to parse value for variable '{variable_name}'. Keeping it as a string. Error: {e}")
                        variable_value = str(variable_value)  # Fallback to string representation
        
                    # Log the details of the execution cell and variable
                    logging.info(f"⚓ Execution Cell Number: {value.get('execution_cell_number', 'N/A')}")
                    logging.info(f"🌀 Operation in the Cell: {value.get('variable_operation', 'N/A')}")
                    logging.info(f"♻️ Variable Cell Name: {variable_name}")
                    logging.info(f"ℹ️ Result of the Cell: {variable_value}")
                    logging.info("")
                    
                    # Add the variable to the dictionary
                    if variable_name:
                        variables[variable_name] = variable_value
        else:
            # If the input is invalid or empty, log a warning
            logging.warning("⛔ Skipping invalid or empty notebook entry.")
            logging.info("")
        
        # Return the dictionary of extracted variables
        return variables