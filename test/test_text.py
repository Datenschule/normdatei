import unittest

from normdatei.text import fingerprint


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