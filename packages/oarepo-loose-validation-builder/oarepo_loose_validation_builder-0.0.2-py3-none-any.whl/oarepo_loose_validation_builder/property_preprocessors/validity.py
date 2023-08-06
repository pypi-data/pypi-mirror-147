from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.utils.deepmerge import deepmerge


class ValidityPreprocessor(PropertyPreprocessor):


    @process(
        model_builder=JSONSchemaBuilder,
        path="**/properties/*",
    )
    def modify_json_schema(self, data, stack: ModelBuilderStack, **kwargs):
        try:
            if 'required' in data:
                data.pop('required')
            if 'minLength' in data:
                data.pop('minLength')
            if 'maxLength' in data:
                data.pop('maxLength')
            if 'minimum' in data:
                data.pop('minimum')
            if 'maximum' in data:
                data.pop('maximum')
            if 'exclusiveMinimum' in data:
                data.pop('exclusiveMinimum')
            if 'exclusiveMaximum' in data:
                data.pop('exclusiveMaximum')
            if 'enum' in data:
                data.pop('enum')
                data['oarepo:jsonschema'].pop('enum')
            if 'minContains' in data:
                data.pop('minContains')
            if 'maxContains' in data:
                data.pop('maxContains')
        except:
            pass
        return data


    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="**/properties/*",
    )
    def modify_validators_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):

        try:
            loose_validators = []
            errors = []
            if 'oarepo:validity' in data and 'non-structural' in data['oarepo:validity']:
                errors = data['oarepo:validity']['non-structural']

            if 'oarepo:marshmallow' in data and 'required' in data['oarepo:marshmallow'] and data['oarepo:marshmallow']['required']:
                if 'required' in errors:
                    data['oarepo:marshmallow']['required'] = 'OarepoError("required", struct=False)'
                else:
                    data['oarepo:marshmallow']['required'] = 'OarepoError("required", struct=True)'

            if 'oarepo:marshmallow' in data and 'oarepo:validity' in data and 'validators' in data['oarepo:marshmallow']:
                for v in data['oarepo:marshmallow']['validators']:
                    if v.startswith('ma_valid.Length') and 'length' in errors:
                        v = v.replace('ma_valid.', 'loose_valid.')
                    elif v.startswith('ma_valid.Range') and 'range' in errors:
                        v = v.replace('ma_valid.', 'loose_valid.')
                    elif v.startswith('ma_valid.OneOf') and 'enum' in errors:
                        v = v.replace('ma_valid.', 'loose_valid.')
                    loose_validators.append(v)
                data['oarepo:marshmallow']['validators'] = loose_validators
        except:
            pass
        return data
