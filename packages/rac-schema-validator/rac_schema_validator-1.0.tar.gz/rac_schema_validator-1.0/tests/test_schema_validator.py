import json
import unittest
from os.path import abspath, dirname, join

from jsonschema.exceptions import SchemaError

from rac_schema_validator import _is_date, is_valid
from rac_schema_validator.exceptions import ValidationError

base_path = dirname(dirname(abspath(__file__)))

fixtures_dir = join(base_path, "fixtures")


class TestSchemas(unittest.TestCase):

    def test_is_date(self):
        for valid_date in ['2022', '2022-10', '2022-10-12']:
            self.assertTrue(_is_date(None, valid_date))
        for invalid_date in [None, 2022, "2022/10", "October 2022"]:
            self.assertFalse(_is_date(None, invalid_date))

    def test_schema_validation(self):
        with self.assertRaises(SchemaError):
            is_valid({}, {"format": ["foo"]})

    def test_validation(self):
        """Validates fixtures against schemas.

        Uses a variety of fixtures to ensure that validation (and invalidation)
        takes place as expected.
        """

        with open(join(fixtures_dir, 'base_schema.json'), 'r') as base_file:
            base_schema = json.load(base_file)
            with open(join(fixtures_dir, 'object_schema.json'), 'r') as object_file:
                object_schema = json.load(object_file)

                with open(join(fixtures_dir, 'valid_object.json'), 'r') as data_file:
                    object = json.load(data_file)
                    self.assertTrue(
                        is_valid(
                            object,
                            object_schema,
                            base_schema))

                with open(join(fixtures_dir, 'invalid_object.json'), 'r') as data_file:
                    object = json.load(data_file)
                    with self.assertRaises(ValidationError):
                        is_valid(object, object_schema, base_schema)

    def test_args(self):
        """Checks TypeError exception is raised when args are not dicts."""
        for data in ["string", ["this", "is", "a", "list"]]:
            with self.assertRaises(TypeError):
                is_valid(data, {})

            with self.assertRaises(TypeError):
                is_valid({}, data)

            with self.assertRaises(TypeError):
                is_valid({}, {}, data)
