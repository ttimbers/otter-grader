"""Assignment configurations for Otter Assign"""

import fica
import os
import pathlib

from typing import Any, Dict, List, Optional, Union

from ..run.run_autograder.autograder_config import AutograderConfig
from ..utils import Loggable


# TODO: add detection/warnings/errors for when a user provides an invalid key? (to be added to fica)
class Assignment(fica.Config, Loggable):
    """
    Configurations for the assignment.
    """

    name: Optional[str] = fica.Key(
        description="a name for the assignment (to validate that students submit to the correct " \
            "autograder)",
        default=None,
    )

    requirements: Optional[str] = fica.Key(
        description="the path to a requirements.txt file or a list of packages",
        default=None,
    )

    overwrite_requirements: bool = fica.Key(
        description="whether to overwrite Otter's default requirement.txt in Otter Generate",
        default=False,
    )

    environment: Optional[str] = fica.Key(
        description="the path to a conda environment.yml file",
        default=None,
    )

    run_tests: bool = fica.Key(
        description="whether to run the assignment tests against the autograder notebook",
        default=True,
    )

    solutions_pdf: bool = fica.Key(
        description="whether to generate a PDF of the solutions notebook",
        default=False,
    )

    template_pdf: bool = fica.Key(
        description="whether to generate a filtered Gradescope assignment template PDF",
        default=False,
    )

    init_cell: bool = fica.Key(
        description="whether to include an Otter initialization cell in the output notebooks",
        default=True,
    )

    check_all_cell: bool = fica.Key(
        description="whether to include an Otter check-all cell in the output notebooks",
        default=False,
    )

    class ExportCellValue(fica.Config):

        instructions: str = fica.Key(
            description="additional submission instructions to include in the export cell",
            default="",
        )

        pdf: bool = fica.Key(
            description="whether to include a PDF of the notebook in the generated zip file",
            default=True,
        )

        filtering: bool = fica.Key(
            description="whether the generated PDF should be filtered",
            default=True,
        )

        force_save: bool = fica.Key(
            description="whether to force-save the notebook with JavaScript (only works in " \
                "classic notebook)",
            default=False,
        )

        run_tests: bool = fica.Key(
            description="whether to run student submissions against local tests during export",
            default=True,
        )

    export_cell: ExportCellValue = fica.Key(
        description="whether to include an Otter export cell in the output notebooks",
        subkey_container=ExportCellValue,
    )

    class SeedValue(fica.Config):

        variable: Optional[str] = fica.Key(
            description="a variable name to override with the autograder seed during grading",
            default=None,
        )

        autograder_value: Optional[int] = fica.Key(
            description="the value of the autograder seed",
            default=None,
        )

        student_value: Optional[int] = fica.Key(
            description="the value of the student seed",
            default=None,
        )

    seed: SeedValue = fica.Key(
        description="intercell seeding configurations",
        default=None,
        subkey_container=SeedValue,
    )

    generate: Union[bool, AutograderConfig] = fica.Key(
        description="grading configurations to be passed to Otter Generate as an " \
            "otter_config.json; if false, Otter Generate is disabled",
        default=False,
        subkey_container=AutograderConfig,
    )

    save_environment: bool = fica.Key(
        description="whether to save the student's environment in the log",
        default=False,
    )

    variables: Optional[Dict[str, str]] = fica.Key(
        description="a mapping of variable names to type strings for serializing environments",
        default=None,
    )

    ignore_modules: List[str] = fica.Key(
        description="a list of modules to ignore variables from during environment serialization",
        default=[],
    )

    files: List[str] = fica.Key(
        description="a list of other files to include in the output directories and autograder",
        default=[],
    )

    autograder_files: List[str] = fica.Key(
        description="a list of other files only to include in the autograder",
        default=[],
    )

    plugins: List[str] = fica.Key(
        description="a list of plugin names and configurations",
        default=[],
    )

    class TestsValue(fica.Config):

        files: bool = fica.Key(
            description="whether to store tests in separate files, instead of the notebook " \
                "metadata",
            default=False,
        )

        ok_format: bool = fica.Key(
            description="whether the test cases are in OK-format (instead of the exception-based " \
                "format)",
            default=True,
        )

        url_prefix: Optional[str] = fica.Key(
            description="a URL prefix for where test files can be found for student use",
            default=None,
        )

    tests: TestsValue = fica.Key(
        description="information about the structure and storage of tests",
        subkey_container=TestsValue,
        enforce_subkeys=True,
    )

    show_question_points: bool = fica.Key(
        description="whether to add the question point values to the last cell of each question",
        default=False,
    )

    runs_on: str = fica.Key(
        description= "the interpreter this notebook will be run on if different from the " \
            "default interpreter (one of {'default', 'colab', 'jupyterlite'})",
        default="default",
        validator=fica.validators.choice(["default", "colab", "jupyterlite"])
    )

    python_version: Optional[Union[str, int, float]] = fica.Key(
        description="the version of Python to use in the grading image (must be 3.6+)",
        default=None,
    )

    lang: Optional[str] = None
    """the language of the assignment"""

    master: pathlib.Path = None
    """the path to the master notebook"""

    result: pathlib.Path = None
    """the path to the output directory"""

    seed_required: bool = False
    """whether a seeding configuration is required for Otter Generate"""

    # TODO: rename this
    _temp_test_dir: Optional[str] = None
    """the path to a directory of test files for Otter Generate"""

    notebook_basename: Optional[str] = None
    """the basename of the master notebook file"""

    def __init__(self, user_config: Dict[str, Any] = {}, **kwargs) -> None:
        self._logger.debug(f"Initializing with config: {user_config}")
        super().__init__(user_config, **kwargs)

        # convert a boolean to a config object for self.generate if indicated
        if self.generate is True:
            self.generate = AutograderConfig()

    def update(self, user_config: Dict[str, Any]):
        self._logger.debug(f"Updating config: {user_config}")
        ret = super().update(user_config)
        if self.generate is True:
            self.generate = AutograderConfig()
        return ret

    @property
    def is_r(self):
        """
        Whether the language of the assignment is R
        """
        return self.lang == "r"

    @property
    def is_python(self):
        """
        Whether the language of the assignment is Python
        """
        return self.lang == "python"

    @property
    def is_rmd(self):
        """
        Whether the input file is an RMarkdown document
        """
        return self.master.suffix.lower() == ".rmd"

    @property
    def generate_enabled(self):
        """
        Whether Otter Generate is enabled for this assignment
        """
        return self.generate is not False

    def get_otter_config(self):
        """
        Get the contents of ``otter_config.json`` for this assignment.

        Returns:
            ``dict[str, object]``: the ``otter_config.json`` file as a ``dict``
        """
        if not self.generate_enabled:
            raise ValueError("Otter Generate is not configured for this assignment")

        otter_config = self.generate

        if self.is_r:
            otter_config.lang = "r"

        # TODO: move this config out of the assignment metadata and into the generate key
        if self.variables:
            otter_config.serialized_variables = str(self.variables)

        if self.name:
            otter_config.assignment_name = self.name

        return otter_config.get_user_config()

    @property
    def notebook_basename(self):
        """the basename of the notebook"""
        return os.path.basename(str(self.master))

    @property
    def ag_notebook_path(self):
        """the path to the autograder notebook"""
        return self.get_ag_path(self.notebook_basename)

    def get_ag_path(self, path=""):
        """
        Get the path to the autograder output directory or a file in that directory.

        Args:
            path (``str | pathlib.Path``): a path to append to the autograder output directory path

        Returns:
            ``pathlib.Path``: the path to the autograder directory or the specified file within it
        """
        return self.result / "autograder" / path

    def get_stu_path(self, path=""):
        """
        Get the path to the student output directory or a file in that directory.

        Args:
            path (``str | pathlib.Path``): a path to append to the student output directory path

        Returns:
            ``pathlib.Path``: the path to the student directory or the specified file within it
        """
        return self.result / "student" / path

    def get_python_version(self) -> Optional[str]:
        """
        Returns the Python version indicated as a string (to avoid issues with YAML interpreting it
        as a number) if one is present.

        Returns:
            ``str | None``: the version string or ``None`` if none is present
        """
        return str(self.python_version) if self.python_version is not None else None
