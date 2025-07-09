import unittest
import sys
import os
from datetime import datetime
from unittest.mock import MagicMock

# Add the parent directory to the path so we can import xerparser
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xerparser.model.classes.project import Project
from xerparser.model.classes.data import Data


class TestProjectDateParsing(unittest.TestCase):
    """Test cases for Project class date parsing fixes"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.data = Data()
    
    def test_add_date_empty_string(self):
        """Test that empty add_date string is handled correctly"""
        params = {
            'proj_id': '1',
            'add_date': ''
        }
        project = Project(params, self.data)
        self.assertIsNone(project.add_date)
    
    def test_add_date_none(self):
        """Test that None add_date is handled correctly"""
        params = {
            'proj_id': '1',
            'add_date': None
        }
        project = Project(params, self.data)
        self.assertIsNone(project.add_date)
    
    def test_add_date_missing(self):
        """Test that missing add_date field is handled correctly"""
        params = {
            'proj_id': '1'
        }
        project = Project(params, self.data)
        self.assertIsNone(project.add_date)
    
    def test_add_date_whitespace_only(self):
        """Test that whitespace-only add_date is handled correctly"""
        params = {
            'proj_id': '1',
            'add_date': '   '
        }
        project = Project(params, self.data)
        self.assertIsNone(project.add_date)
    
    def test_add_date_valid_datetime(self):
        """Test that valid add_date string is parsed correctly"""
        params = {
            'proj_id': '1',
            'add_date': '2023-01-01 00:00'
        }
        project = Project(params, self.data)
        self.assertIsInstance(project.add_date, datetime)
        self.assertEqual(project.add_date.year, 2023)
        self.assertEqual(project.add_date.month, 1)
        self.assertEqual(project.add_date.day, 1)
    
    def test_add_date_invalid_format(self):
        """Test that invalid add_date format is handled gracefully"""
        params = {
            'proj_id': '1',
            'add_date': 'invalid-date-format'
        }
        project = Project(params, self.data)
        self.assertIsNone(project.add_date)
    
    def test_add_date_partial_datetime(self):
        """Test that partial datetime strings are handled gracefully"""
        params = {
            'proj_id': '1',
            'add_date': '2023-01-01'  # Missing time part
        }
        project = Project(params, self.data)
        self.assertIsNone(project.add_date)
    
    def test_get_tsv_with_add_date(self):
        """Test that get_tsv() correctly formats add_date"""
        params = {
            'proj_id': '1',
            'add_date': '2023-01-01 12:30'
        }
        project = Project(params, self.data)
        tsv = project.get_tsv()
        
        # Find the add_date in the TSV output
        # Based on the get_tsv method, add_date should be at index 32
        add_date_index = 32
        formatted_date = tsv[add_date_index]
        self.assertEqual(formatted_date, '2023-01-01 12:30')
    
    def test_get_tsv_with_none_add_date(self):
        """Test that get_tsv() correctly handles None add_date"""
        params = {
            'proj_id': '1',
            'add_date': ''
        }
        project = Project(params, self.data)
        tsv = project.get_tsv()
        
        # Find the add_date in the TSV output
        add_date_index = 31
        formatted_date = tsv[add_date_index]
        self.assertIsNone(formatted_date)
    
    def test_project_creation_with_minimal_params(self):
        """Test that project can be created with minimal parameters"""
        params = {
            'proj_id': '1'
        }
        project = Project(params, self.data)
        self.assertEqual(project.proj_id, 1)
        self.assertIsNone(project.add_date)
    
    def test_project_creation_with_all_date_fields(self):
        """Test project creation with various date fields"""
        params = {
            'proj_id': '1',
            'add_date': '2023-01-01 00:00',
            'last_recalc_date': '2023-01-02',
            'plan_start_date': '2023-01-03',
            'plan_end_date': '2023-01-04'
        }
        project = Project(params, self.data)
        
        # add_date should be parsed as datetime
        self.assertIsInstance(project.add_date, datetime)
        
        # Other date fields should remain as strings (existing behavior)
        self.assertEqual(project.last_recalc_date, '2023-01-02')
        self.assertEqual(project.plan_start_date, '2023-01-03')
        self.assertEqual(project.plan_end_date, '2023-01-04')


class TestProjectBackwardCompatibility(unittest.TestCase):
    """Test cases to ensure backward compatibility is maintained"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.data = Data()
    
    def test_existing_project_functionality(self):
        """Test that existing project functionality still works"""
        params = {
            'proj_id': '123',
            'proj_short_name': 'Test Project',
            'fy_start_month_num': '1',
            'rsrc_self_add_flag': 'Y',
            'allow_complete_flag': 'Y'
        }
        project = Project(params, self.data)
        
        self.assertEqual(project.proj_id, 123)
        self.assertEqual(project.proj_short_name, 'Test Project')
        self.assertEqual(project.fy_start_month_num, '1')
        self.assertEqual(project.rsrc_self_add_flag, 'Y')
        self.assertEqual(project.allow_complete_flag, 'Y')
    
    def test_project_id_property(self):
        """Test that the id property works correctly"""
        params = {
            'proj_id': '456'
        }
        project = Project(params, self.data)
        self.assertEqual(project.id, 456)
    
    def test_project_repr(self):
        """Test that the __repr__ method works correctly"""
        params = {
            'proj_id': '789',
            'proj_short_name': 'Repr Test'
        }
        project = Project(params, self.data)
        self.assertEqual(str(project), 'Repr Test')
    
    def test_project_with_none_values(self):
        """Test project creation with None values for optional fields"""
        params = {
            'proj_id': '1',
            'proj_short_name': None,
            'add_date': None,
            'last_recalc_date': None
        }
        project = Project(params, self.data)
        
        self.assertEqual(project.proj_id, 1)
        self.assertIsNone(project.proj_short_name)
        self.assertIsNone(project.add_date)
        self.assertIsNone(project.last_recalc_date)


if __name__ == '__main__':
    unittest.main()
