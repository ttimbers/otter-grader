"""
Miscellaneous cell generators for Otter Assign
"""

import copy
import nbformat

from .utils import get_source, lock

def gen_init_cell():
    """
    Generates a cell to initialize Otter in the notebook. The code cell has the following contents:

    .. code-block:: python

        # Initialize Otter
        import otter
        grader = otter.Notebook()
    
    Returns:
        ``nbformat.NotebookNode``: the init cell
    """
    cell = nbformat.v4.new_code_cell("# Initialize Otter\nimport otter\ngrader = otter.Notebook()")
    lock(cell)
    return cell

def gen_markdown_response_cell():
    """
    Generates a Markdown response cell with the following contents:

    .. code-block:: markdown

        _Type your answer here, replacing this text._

    Returns:
        ``nbformat.NotebookNode``: the response cell
    """
    return nbformat.v4.new_markdown_cell("_Type your answer here, replacing this text._")

def gen_export_cells(instruction_text, pdf=True, filtering=True):
    """
    Generates export cells that instruct the student the run a code cell calling 
    ``otter.Notebook.export`` to generate and download their submission. The Markdown cell contains:

    .. code-block:: markdown

        ## Submission
        
        Make sure you have run all cells in your notebook in order before running the cell below, so 
        that all images/graphs appear in the output. The cell below will generate a zipfile for you 
        to submit. **Please save before exporting!**

    Additional instructions can be appended to this cell by passing a string to ``instruction_text``.

    The code cell contains:

    .. code-block:: python

        # Save your notebook first, then run this cell to export your submission.
        grader.export()
    
    The call to ``grader.export()`` contains different arguments based on the values passed to ``pdf``
    and ``filtering``. 
    
    Args:
        instruction_text (``str``): extra instructions for students when exporting
        pdf (``bool``, optional): whether a PDF is needed
        filtering (``bool``, optional): whether PDF filtering is needed
    
    Returns:
        ``list`` of ``nbformat.NotebookNode``: generated export cells
    """
    instructions = nbformat.v4.new_markdown_cell()
    instructions.source = "## Submission\n\nMake sure you have run all cells in your notebook in order before \
    running the cell below, so that all images/graphs appear in the output. The cell below will generate \
    a zipfile for you to submit. **Please save before exporting!**"
    
    if instruction_text:
        instructions.source += '\n\n' + instruction_text

    export = nbformat.v4.new_code_cell()
    source_lines = ["# Save your notebook first, then run this cell to export your submission."]
    if filtering and pdf:
        source_lines.append(f"grader.export()")
    elif not filtering:
        source_lines.append(f"grader.export(filtering=False)")
    else:
        source_lines.append(f"grader.export(pdf=False)")
    export.source = "\n".join(source_lines)

    lock(instructions)
    lock(export)

    return [instructions, export, nbformat.v4.new_markdown_cell(" ")]     # last cell is buffer

def gen_check_all_cell():
    """
    Generates a check-all cell and a Markdown cell with instructions to run all tests in the notebook. 
    The Markdown cell has the following contents:

    .. code-block:: markdown

        ---
        
        To double-check your work, the cell below will rerun all of the autograder tests.

    The code cell has the following contents:

    .. code-block:: python

        grader.check_all()
    
    Returns:
        ``list`` of ``nbformat.NotebookNode``: generated check-all cells
    """
    instructions = nbformat.v4.new_markdown_cell()
    instructions.source = "---\n\nTo double-check your work, the cell below will rerun all of the autograder tests."

    check_all = nbformat.v4.new_code_cell("grader.check_all()")

    lock(instructions)
    lock(check_all)

    return [instructions, check_all]

def gen_close_export_cell():
    """
    Generates a Markdown cell to end question export for PDF filtering. The cell contains:

    .. code-block:: markdown

        <!-- END QUESTION -->
    
    Returns:
        ``nbformat.NotebookNode``: new Markdown cell with ``<!-- END QUESTION -->``
    """
    cell = nbformat.v4.new_markdown_cell("<!-- END QUESTION -->")
    lock(cell)
    return cell

def add_close_export_to_cell(cell):
    """Adds an HTML comment to close question export for PDF filtering to the top of ``cell``. ``cell``
    should be a Markdown cell. This adds ``<!-- END QUESTION-->`` as the first line of the cell.
    
    Args:
        cell (``nbformat.NotebookNode``): the cell to add the close export to

    Returns:
        ``nbformat.NotebookNode``: the cell with the close export comment at the top
    """
    cell = copy.deepcopy(cell)
    source = get_source(cell)
    source = ["<!-- END QUESTION -->\n", "\n"] + source
    cell['source'] = "\n".join(source)
    return cell

