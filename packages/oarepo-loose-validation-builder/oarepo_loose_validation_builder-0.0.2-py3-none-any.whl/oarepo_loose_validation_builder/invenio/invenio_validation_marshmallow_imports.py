from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioValidationMarshmallowImports(InvenioBaseClassPythonBuilder):
    class_config = "record-schema-class"
    template = "record-validation-imports"
    def finish(self):
        super().finish()