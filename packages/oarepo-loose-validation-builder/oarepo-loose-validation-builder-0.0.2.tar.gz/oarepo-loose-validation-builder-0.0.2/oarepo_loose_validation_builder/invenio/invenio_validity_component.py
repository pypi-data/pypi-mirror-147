from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioTestBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_dumper"
    class_config = "record-service-config-class"
    template = "record-test"
