import csv
import json
import os
import tempfile


from django.test import SimpleTestCase
from django.test import Client
from django.test.utils import override_settings

from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import Mock

from django.conf import settings
from django.core.management import call_command
from django.test import SimpleTestCase


def fixture_path(filename):
    return os.path.join(settings.BASE_DIR, 'frontend/tests/fixtures/', filename)

def expected_path(filename):
    return os.path.join(settings.BASE_DIR, 'frontend/tests/expected/', filename)

def generated(key):
    path = fixture_path(TEST_SETTINGS[key])
    return json.load(open(path))

def expected(fname):
    return json.load(open(expected_path(fname)))

def temp_path():
    return tempfile.mkstemp()[1]

def temp_headline_history():
    """Make a valid empty JSON file and return the path
    """
    p = temp_path()
    f = open(p, 'w')
    f.write('{}')
    f.close()
    return p

TEST_SETTINGS={
    'SOURCE_CSV_FILE': fixture_path('trials.csv'),
    'SOURCE_META_FILE': fixture_path('trials.csv.json'),
    'NORMALIZE_FILE': fixture_path('normalized_sponsor_names.xlsx'),
    'OUTPUT_HEADLINE_FILE': temp_path(),
    'OUTPUT_HEADLINE_HISTORY': temp_headline_history(),
    'OUTPUT_ALL_SPONSORS_FILE': temp_path(),
    'OUTPUT_ALL_TRIALS_FILE': temp_path(),
    'OUTPUT_NEW_NORMALIZE_FILE': temp_path(),
    'MAJOR_SPONSORS_THRESHOLD': 1
}

NEW_TRIALS_SETTINGS = TEST_SETTINGS.copy()
NEW_TRIALS_SETTINGS['SOURCE_CSV_FILE'] = fixture_path('non_matching_trials.csv')
NEW_TRIALS_SETTINGS['OUTPUT_NEW_NORMALIZE_FILE'] = temp_path()


class UpdateTrialsJSONTestCase(SimpleTestCase):
    maxDiff = 15000
    @classmethod
    @override_settings(**TEST_SETTINGS)
    def setUpClass(cls):
        call_command('update_trials_json')

    def test_all_trials(self):
        self.assertEqual(
            generated('OUTPUT_ALL_TRIALS_FILE'),
            expected('all_trials.json'))

    def test_headline(self):
        self.assertEqual(
            generated('OUTPUT_HEADLINE_FILE'),
            expected('headline.json'))

    def test_headline_history(self):
        self.assertEqual(
            generated('OUTPUT_HEADLINE_HISTORY'),
            expected('headline-history.json'))

    def test_all_sponsors(self):
        self.assertEqual(
            generated('OUTPUT_ALL_SPONSORS_FILE'),
            expected('all_sponsors.json'))

    def test_no_trials_to_normalize(self):
        self.assertEqual(
            open(TEST_SETTINGS['OUTPUT_NEW_NORMALIZE_FILE']).read(),
            '')

    @override_settings(**NEW_TRIALS_SETTINGS)
    def test_new_trials_to_normalize(self):
        with self.assertRaises(SystemExit):
            call_command('update_trials_json')
        normalize_file = list(csv.DictReader(open(NEW_TRIALS_SETTINGS['OUTPUT_NEW_NORMALIZE_FILE'])))
        self.assertEqual(normalize_file[0]['name_of_sponsor'], 'unmatched')
        self.assertEqual(normalize_file[0]['normalized_name'], '')
        self.assertEqual(normalize_file[1]['name_of_sponsor'], 'Lilly S.A')
        self.assertEqual(normalize_file[1]['normalized_name'], 'Lilly')
        self.assertEqual(normalize_file[1]['normalized_parent_name'], 'Lilly Megacorp')

    @classmethod
    def tearDownClass(cls):
        for p in [x for x in TEST_SETTINGS.keys()
                  if x.startswith('OUTPUT_')]:
            os.remove(TEST_SETTINGS[p])
