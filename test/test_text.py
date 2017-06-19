# -!- coding:utf-8 -!-
import unittest
import pytest

from normdatei.text import fingerprint, clean_name
parametrize = pytest.mark.parametrize

class TestFingerprint(unittest.TestCase):
    def test_none(self):
        result = fingerprint(None)
        assert result is None

    def test_empty_string(self):
        result = fingerprint("")
        assert result is None

    def test_remove_title(self):
        names = ["Dr Jakob Maria Mierscheid",
                 "Dr. h.c. Jakob Maria Mierscheid",
                 "Jakob Maria Mierscheid"]
        normalized = {fingerprint(name) for name in names}
        self.assertEqual(normalized, {"jakob-maria-mierscheid"})


class TestCleanText(object):
    @parametrize("test_input", [
        "Zuruf",
        "Zurufe",
    ])
    def test_remove_poi(self, test_input):
        assert clean_name(test_input) == ""

    @pytest.mark.parametrize("test_input", [
        "Bundeskanzler Jakob Mierscheid",
        "Bundeskanzlerin Jakob Mierscheid",
        u"Parl. Staatssekretärin Jakob Mierscheid",
        u"Alterspräsident Jakob Mierscheid",
    ])
    def test_remove_title(self, test_input):
        assert clean_name(test_input) == "Jakob Mierscheid"

    @pytest.mark.parametrize("test_input", [
        "Volker Kauder [CDU/CSU]",
        "Volker Kauder (CDU/CSU)",
    ])
    def test_remove_party(self, test_input):
        assert clean_name(test_input) == "Volker Kauder"