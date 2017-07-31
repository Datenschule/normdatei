# coding: utf-8
import re

import normality
from normality import normalize

FP_REMOVE = re.compile(u'(^.*Dr\.?( h\.? ?c\.?)?| (von( der)?)| [A-Z]\. )')

NAME_REMOVE = [u'\\[.*\\]|\\(.*\\)', u'( de[sr])? Abg.? ',
               u'Vizepräsidentin', u'Vizepräsident', u'Präsident',
               u'Präsidentin', u'Alterspräsident', u'Alterspräsidentin',
               u'Liedvortrag', u'Bundeskanzler(in)?', u', Parl\\. .*',
               u', Staatsmin.*', u', Bundesmin.*', u', Ministe.*',
               u'Staatsministers', 'Bundesministers',
               u'Parl. Staatssekretärin', u', Wehrbeauftragter.*',
               u', Beauftragter? der .*', u', Erster Bürgermeister.*',
               u'Ge ?genruf', 'Weiterer Zuruf', 'Zurufe?', 'Weiterer',
               u', zur.*', u', auf die', u' an die', u', an .*', u'gewandt']
NAME_REMOVE = re.compile(u'(%s)' % '|'.join(NAME_REMOVE), re.U)
DE_HYPHEN = re.compile(r'([a-z])-([a-z])', re.U)


def clean_text(text):
    text = text.replace('\r', '\n')
    text = text.replace(u'\xa0', ' ')
    text = text.replace(u'\x96', '-')
    text = text.replace(u'\u2014', '-')
    text = text.replace(u'\u2013', '-')
    return text


def clean_name(name):
    if name is None:
        return name
    name = NAME_REMOVE.sub('', name)
    name = DE_HYPHEN.sub(r'\1\2', name)
    name = name.strip('-')
    return name.strip()


def fingerprint(name):
    if not name:
        return
    name = FP_REMOVE.sub(' ', name.strip())
    return normalize(name).replace(' ', '-')


def _remove_non_top_numbers(text):
    slash_pattern = re.compile('\d+\/(\S+)')

    # sometimes there are non breaking spaces. We replace those
    # with regular spaces to later ease the matching
    text = normality.collapse_spaces(text)

    # remove numbers that come from a Drucksache such as 18/603
    # or from The Greens (Bündnis 90/die Grünen)
    text = slash_pattern.sub('', text)
    return text


def extract_agenda_numbers(text):
    roman_number = re.compile("[XIV]+(?:\.\d+)(?!\w)", re.UNICODE)
    roman = re.compile("([XIV]+)(?!\w)", re.UNICODE)
    arabic_letter = re.compile("\d+(?:\s\w(?!\w))?", re.UNICODE)

    text = _remove_non_top_numbers(text)

    roman_number_matches = roman_number.findall(text)
    text = roman_number.sub('', text)

    roman_matches = roman.findall(text)

    arabic_letter_matches = arabic_letter.findall(text)

    return roman_number_matches + arabic_letter_matches + roman_matches