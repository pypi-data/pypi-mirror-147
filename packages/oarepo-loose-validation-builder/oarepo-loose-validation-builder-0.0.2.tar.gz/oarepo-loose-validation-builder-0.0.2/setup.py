# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oarepo_loose_validation_builder',
 'oarepo_loose_validation_builder.builtin_models',
 'oarepo_loose_validation_builder.invenio',
 'oarepo_loose_validation_builder.model_preprocessors',
 'oarepo_loose_validation_builder.property_preprocessors']

package_data = \
{'': ['*'], 'oarepo_loose_validation_builder.invenio': ['templates/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'click>=7.1',
 'isort>=5.10.1,<6.0.0',
 'jsonpointer>=2.2,<3.0',
 'langcodes>=3.3.0',
 'libcst>=0.4.1,<0.5.0',
 'marshmallow>=3.14.1,<4.0.0',
 'oarepo-model-builder>=0.9.17',
 'tomlkit>=0.9.0,<0.10.0']

extras_require = \
{'json5': ['json5>=0.9.6,<0.10.0'], 'pyyaml': ['PyYAML>=6.0,<7.0']}

entry_points = \
{'oarepo.model_schemas': ['errors = '
                          'oarepo_loose_validation_builder:errors.json5'],
 'oarepo.models': ['validity = '
                   'oarepo_loose_validation_builder.builtin_models:validity.json'],
 'oarepo_model_builder.builders': ['0901-invenio_validity_component = '
                                   'oarepo_loose_validation_builder.invenio.invenio_validity_component:InvenioRecordSearchOptionsBuilderMultilingual',
                                   '0902-invenio_validation_marshmallow_imports '
                                   '= '
                                   'oarepo_loose_validation_builder.invenio.invenio_validation_marshmallow_imports:InvenioValidationMarshmallowImports',
                                   '1101-invenio_validation_poetry = '
                                   'oarepo_loose_validation_builder.invenio.invenio_validation_poetry:InvenioValidationPoetryBuilder'],
 'oarepo_model_builder.model_preprocessors': ['30-validation-model = '
                                              'oarepo_loose_validation_builder.model_preprocessors.validation_model:InvenioLooseModelPreprocessor'],
 'oarepo_model_builder.property_preprocessors': ['900-validity = '
                                                 'oarepo_loose_validation_builder.property_preprocessors.validity:ValidityPreprocessor']}

setup_kwargs = {
    'name': 'oarepo-loose-validation-builder',
    'version': '0.0.2',
    'description': '',
    'long_description': '# OARepo Loose Validation Builder\n\n',
    'author': 'Alzbeta Pokorna',
    'author_email': 'alzbeta.pokorna@cesnet.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
