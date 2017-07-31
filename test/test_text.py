# -!- coding:utf-8 -!-
import unittest
import pytest

from normdatei.text import fingerprint, clean_name, extract_agenda_numbers

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
        "Bundeskanzler Jakob Mierscheid",
        "Bundeskanzlerin Jakob Mierscheid",
        u"Jakob Mierscheid, Wehrbeauftragter des Deutschen Bundestages",
        u"Jakob Mierscheid, Beauftragter der Bundesregierung für die neuen Bundesländer",
        u"Jakob Mierscheid, Beauftragte der Bundesregierung für die neuen Bundesländer",
        u"Jakob Mierscheid, Erster Bürgermeister (Hamburg)",
    ])
    def test_remove_suffix(self, test_input):
        assert clean_name(test_input) == "Jakob Mierscheid"

    @pytest.mark.parametrize("test_input", [
        "Volker Kauder [CDU/CSU]",
        "Volker Kauder (CDU/CSU)",
    ])
    def test_remove_party(self, test_input):
        assert clean_name(test_input) == "Volker Kauder"


class TestExtractAgendaNumbers(object):
    @parametrize("test_text, result", [
        (u'5 auf', ['5']),
        (u'7 sowie 8 und 9', ['7', '8', '9']),
    ])
    def test_simple_arabic(self, test_text, result):
        assert extract_agenda_numbers(test_text) == result

    @parametrize("test_text, result", [
        (u'VI auf', ['VI']),
        (u'II und Tagesordnungspunkt III', ['II', 'III']),
    ])
    def test_simple_roman(self, test_text, result):
        assert extract_agenda_numbers(test_text) == result

    @parametrize("test_text, result", [
        (u'5 und 5 a', ['5', '5 a']),
        (u'5 a und 6 c', ['5 a', '6 c']),
        (u'22 h:', ['22 h']),  # <- this contains a non breaking space character
        (u' 5 c:', ['5 c']),
    ])
    def test_extended_arabic(self, test_text, result):
        assert extract_agenda_numbers(test_text) == result

    @parametrize("test_text, result", [
        # (u'V a bis V d auf', ['V a', 'V b', 'V c', 'V d']),
        (u'V c', ['V c']),
        (u'V c und V d', ['V c', 'V d']),
    ])
    def test_extended_roman(self, test_text, result):
        assert extract_agenda_numbers(test_text) == result

    @parametrize("test_text, result", [
        (u'II.18 auf', ['II.18']),
        (u'II.19 auf und II.20', ['II.19', 'II.20']),
    ])
    def test_extended_roman(self, test_text, result):
        assert extract_agenda_numbers(test_text) == result

    @parametrize("test_text, result", [
        (u'ist der Herr Ingo Müller', []),
        (u'redet jetzt noch Victor Hugo', []),
        (u'Drucksache 18/608', []),
        (u'vom Bündnis 90/Die Grünen', []),
    ])
    def test_nomatch_roman(self, test_text, result):
        assert extract_agenda_numbers(test_text) == result
