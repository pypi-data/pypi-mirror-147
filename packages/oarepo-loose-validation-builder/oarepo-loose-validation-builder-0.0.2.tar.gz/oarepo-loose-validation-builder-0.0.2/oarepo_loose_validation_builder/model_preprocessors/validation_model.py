from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class InvenioLooseModelPreprocessor(ModelPreprocessor):
    TYPE = "invenio"

    def transform(self, schema, settings):

        self.set(
            settings.python,
            "record-metadata-bases",
            lambda: [f"oarepo_loose_validation.model.LooseValidationModel"],
        )