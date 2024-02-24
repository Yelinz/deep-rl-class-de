import deepl
import nbformat
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
DEEPL_AUTH = os.getenv("DEEPL_AUTH_KEY")
INPUT_PATH = "notebooks"
OUTPUT_PATH = "translated_notebooks"

translator = deepl.Translator(DEEPL_AUTH)

# TODO a progress bar would be nice
# Walk through all .ipynb files in the specified directory and its subdirectories
for dirpath, dirnames, filenames in os.walk(INPUT_PATH):
    for filename in filenames:
        if filename.endswith(".ipynb"):
            input_filepath = os.path.join(dirpath, filename)
            # Read the notebook
            with open(input_filepath) as f:
                nb = nbformat.read(f, as_version=4)

            # Iterate over all cells in the notebook
            for i, cell in enumerate(nb.cells):
                # Only translate markdown cells
                if cell.cell_type == "markdown":
                    # TODO prevent half translated files if character limit is reached 
                    translated_text = translator.translate_text(cell.source, target_lang="DE")
                    # Replace the cell's content with the translated text
                    nb.cells[i].source = translated_text.text

            # Create the same directory structure in the output directory
            output_dirpath = dirpath.replace(INPUT_PATH, OUTPUT_PATH)
            os.makedirs(output_dirpath, exist_ok=True)

            # Write the translated notebook to the output directory
            output_filepath = os.path.join(output_dirpath, filename)
            with open(output_filepath, 'w') as f:
                nbformat.write(nb, f)