from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.toml import TOMLOutput

class InvenioValidationPoetryBuilder(OutputBuilder):
    TYPE = "invenio_multilingual_poetry"

    def finish(self):
        super().finish()

        output: TOMLOutput = self.builder.get_output("toml", "pyproject.toml")

        output.setdefault(
            "tool.poetry.dependencies.oarepo-loose-validation",
            "version",
            "^0.0.6",
        )