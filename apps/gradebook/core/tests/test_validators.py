# -*- coding: utf-8 -*-
import unittest

from django.core.exceptions import ValidationError

from gradebook.core.validators import external_id_validator

class TestExternalIDsValidator(unittest.TestCase):

    def test_accepts_valid_ids(self):
        valid_ids = [
            "some_id",
            "some-id",
            "some.id",
            "s0me.id",
            "1234",
            "1234.4",
            "edu.mit.eecs.6.002x.2013-2014.spring_A"
        ]
        for ext_id in valid_ids:
            # If it failed to validate, it'd throw a ValidationError
            external_id_validator(ext_id)

    def test_rejects_invalid_ids(self):
        invalid_ids = ["hello;", "hello!there" u"안녕하세요"]
        for ext_id in invalid_ids:
            self.assertRaises(ValidationError, external_id_validator, ext_id)
