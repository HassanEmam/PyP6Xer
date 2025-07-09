import unittest
import sys
import os
import tempfile
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import xerparser
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xerparser.reader import Reader
from xerparser.model.classes.project import Project
from xerparser.model.classes.data import Data
from xerparser.write import writeXER


class TestIntegrationFixes(unittest.TestCase):
    """Integration tests to ensure fixes work with the complete library"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.dirname(self.test_data_dir)
    
    def test_project_creation_integration(self):
        """Test project creation with various date scenarios in integration context"""
        data = Data()
        
        # Test cases covering the fix scenarios
        test_cases = [
            # (params, expected_add_date_type)
            ({'proj_id': '1', 'add_date': ''}, type(None)),
            ({'proj_id': '2', 'add_date': '2023-01-01 12:00'}, type(None)),  # Will be datetime after fix
            ({'proj_id': '3'}, type(None)),
            ({'proj_id': '4', 'add_date': 'invalid'}, type(None)),
        ]
        
        for params, expected_type in test_cases:
            with self.subTest(params=params):
                project = Project(params, data)
                
                # Ensure project is created successfully
                self.assertIsNotNone(project)
                self.assertEqual(project.proj_id, int(params['proj_id']))
                
                # For valid datetime strings, check if they were parsed
                if params.get('add_date') == '2023-01-01 12:00':
                    from datetime import datetime
                    self.assertIsInstance(project.add_date, datetime)
                else:
                    # For empty, missing, or invalid dates
                    self.assertIsNone(project.add_date)
    
    def test_reader_mock_with_missing_scheduleoptions(self):
        """Test Reader-like object without scheduleoptions"""
        # Create a mock reader that simulates missing scheduleoptions
        mock_reader = MagicMock()
        
        # Set up all required attributes except scheduleoptions
        for attr in ['currencies', 'fintmpls', 'nonworks', 'obss', 'pcattypes', 
                     'resourcecurves', 'udftypes', 'accounts', 'pcatvals', 
                     'projects', 'calendars', 'projpcats', 'wbss', 'resources', 
                     'acttypes', 'resourcerates', 'activities', 'actvcodes', 
                     'relations', 'taskprocs', 'activityresources', 'activitycodes', 
                     'udfvalues']:
            getattr(mock_reader, attr).get_tsv.return_value = []
        
        # Don't set scheduleoptions - simulate it's missing
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # This should not raise an error
            writeXER(mock_reader, temp_filename)
            
            # Verify file was created
            self.assertTrue(os.path.exists(temp_filename))
            
            # Verify content doesn't contain SCHEDOPTIONS
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertNotIn('SCHEDOPTIONS', content)
                self.assertIn('%E', content)  # Should have proper ending
        
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_reader_mock_with_empty_scheduleoptions(self):
        """Test Reader-like object with empty scheduleoptions"""
        mock_reader = MagicMock()
        
        # Set up all required attributes
        for attr in ['currencies', 'fintmpls', 'nonworks', 'obss', 'pcattypes', 
                     'resourcecurves', 'udftypes', 'accounts', 'pcatvals', 
                     'projects', 'calendars', 'projpcats', 'wbss', 'resources', 
                     'acttypes', 'resourcerates', 'activities', 'actvcodes', 
                     'relations', 'taskprocs', 'activityresources', 'activitycodes', 
                     'udfvalues']:
            getattr(mock_reader, attr).get_tsv.return_value = []
        
        # Set up empty scheduleoptions
        mock_reader.scheduleoptions = MagicMock()
        mock_reader.scheduleoptions.__len__.return_value = 0
        mock_reader.scheduleoptions.get_tsv.return_value = []
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # This should not raise an error
            writeXER(mock_reader, temp_filename)
            
            # Verify file was created
            self.assertTrue(os.path.exists(temp_filename))
            
            # Verify scheduleoptions.get_tsv was not called (empty)
            mock_reader.scheduleoptions.get_tsv.assert_not_called()
        
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_project_tsv_output_integration(self):
        """Test that project TSV output works correctly with date fixes"""
        data = Data()
        
        # Test with valid add_date
        params_valid = {
            'proj_id': '1',
            'proj_short_name': 'Test Project',
            'add_date': '2023-06-15 09:30'
        }
        project_valid = Project(params_valid, data)
        tsv_valid = project_valid.get_tsv()
        
        # Verify TSV structure
        self.assertEqual(tsv_valid[0], '%R')  # TSV marker
        self.assertEqual(tsv_valid[1], 1)     # proj_id
        
        # Find add_date in TSV (should be at index 32 based on get_tsv method)
        add_date_index = 32
        self.assertEqual(tsv_valid[add_date_index], '2023-06-15 09:30')
        
        # Test with None add_date
        params_none = {
            'proj_id': '2',
            'proj_short_name': 'Test Project 2',
            'add_date': ''
        }
        project_none = Project(params_none, data)
        tsv_none = project_none.get_tsv()
        
        # Verify None add_date in TSV
        self.assertIsNone(tsv_none[add_date_index])
    
    def test_error_handling_resilience(self):
        """Test that the library is resilient to various error conditions"""
        data = Data()
        
        # Test various problematic scenarios
        problematic_params = [
            {'proj_id': None},  # None proj_id
            {'proj_id': '', 'add_date': ''},  # Empty strings
            {'proj_id': '1', 'add_date': '2023-13-45 25:70'},  # Invalid date
            {'proj_id': '1', 'add_date': '2023'},  # Incomplete date
            {'proj_id': '1', 'add_date': 'not-a-date'},  # Non-date string
        ]
        
        for params in problematic_params:
            with self.subTest(params=params):
                try:
                    project = Project(params, data)
                    # Should not raise an exception
                    self.assertIsNotNone(project)
                    
                    # add_date should be None for all problematic cases
                    self.assertIsNone(project.add_date)
                    
                    # TSV generation should also work
                    tsv = project.get_tsv()
                    self.assertIsNotNone(tsv)
                    
                except Exception as e:
                    self.fail(f"Project creation failed for params {params}: {e}")
    
    def test_backward_compatibility_complete_data(self):
        """Test that existing functionality works with complete, valid data"""
        data = Data()
        
        # Complete valid parameters
        params = {
            'proj_id': '12345',
            'proj_short_name': 'Complete Test Project',
            'add_date': '2023-01-01 00:00',
            'last_recalc_date': '2023-06-01',
            'plan_start_date': '2023-01-15',
            'plan_end_date': '2023-12-31',
            'fy_start_month_num': '1',
            'rsrc_self_add_flag': 'Y',
            'allow_complete_flag': 'Y',
            'project_flag': 'Y'
        }
        
        project = Project(params, data)
        
        # Verify all fields are set correctly
        self.assertEqual(project.proj_id, 12345)
        self.assertEqual(project.proj_short_name, 'Complete Test Project')
        self.assertIsNotNone(project.add_date)  # Should be parsed as datetime
        self.assertEqual(project.last_recalc_date, '2023-06-01')
        self.assertEqual(project.plan_start_date, '2023-01-15')
        self.assertEqual(project.plan_end_date, '2023-12-31')
        
        # Test TSV generation
        tsv = project.get_tsv()
        self.assertIsNotNone(tsv)
        self.assertTrue(len(tsv) > 30)  # Should have many fields
        
        # Test string representation
        self.assertEqual(str(project), 'Complete Test Project')


class TestRegressionPrevention(unittest.TestCase):
    """Tests to prevent regression of the fixes"""
    
    def test_add_date_parsing_regression(self):
        """Ensure add_date parsing continues to work correctly"""
        from datetime import datetime
        data = Data()
        
        # These should all work without throwing exceptions
        test_cases = [
            ('', None),
            (None, None),
            ('   ', None),
            ('2023-01-01 12:00', datetime(2023, 1, 1, 12, 0)),
            ('invalid-date', None),
            ('2023-01-01', None),  # Missing time
        ]
        
        for add_date_input, expected_result in test_cases:
            with self.subTest(add_date=add_date_input):
                params = {'proj_id': '1'}
                if add_date_input is not None:
                    params['add_date'] = add_date_input
                
                project = Project(params, data)
                
                if expected_result is None:
                    self.assertIsNone(project.add_date)
                else:
                    self.assertEqual(project.add_date, expected_result)
    
    def test_scheduleoptions_handling_regression(self):
        """Ensure scheduleoptions handling continues to work correctly"""
        mock_reader = MagicMock()
        
        # Set up minimal required attributes
        for attr in ['currencies', 'fintmpls', 'nonworks', 'obss', 'pcattypes', 
                     'resourcecurves', 'udftypes', 'accounts', 'pcatvals', 
                     'projects', 'calendars', 'projpcats', 'wbss', 'resources', 
                     'acttypes', 'resourcerates', 'activities', 'actvcodes', 
                     'relations', 'taskprocs', 'activityresources', 'activitycodes', 
                     'udfvalues']:
            getattr(mock_reader, attr).get_tsv.return_value = []
        
        # Test cases for scheduleoptions
        test_cases = [
            # (scheduleoptions_setup, should_raise_error)
            (None, False),  # Missing scheduleoptions
            ('empty', False),  # Empty scheduleoptions
            ('valid', False),  # Valid scheduleoptions
            ('error', False),  # Scheduleoptions that throws error
        ]
        
        for schedoptions_type, should_raise in test_cases:
            with self.subTest(schedoptions_type=schedoptions_type):
                # Set up scheduleoptions based on test case
                if schedoptions_type is None:
                    # Remove scheduleoptions attribute
                    if hasattr(mock_reader, 'scheduleoptions'):
                        delattr(mock_reader, 'scheduleoptions')
                elif schedoptions_type == 'empty':
                    mock_reader.scheduleoptions = MagicMock()
                    mock_reader.scheduleoptions.__len__.return_value = 0
                    mock_reader.scheduleoptions.get_tsv.return_value = []
                elif schedoptions_type == 'valid':
                    mock_reader.scheduleoptions = MagicMock()
                    mock_reader.scheduleoptions.__len__.return_value = 1
                    mock_reader.scheduleoptions.get_tsv.return_value = [['%T', 'SCHEDOPTIONS']]
                elif schedoptions_type == 'error':
                    mock_reader.scheduleoptions = MagicMock()
                    mock_reader.scheduleoptions.__len__.return_value = 1
                    mock_reader.scheduleoptions.get_tsv.side_effect = Exception("Test error")
                
                # Create temporary file
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
                    temp_filename = temp_file.name
                
                try:
                    if should_raise:
                        with self.assertRaises(Exception):
                            writeXER(mock_reader, temp_filename)
                    else:
                        # Should not raise any exception
                        writeXER(mock_reader, temp_filename)
                        self.assertTrue(os.path.exists(temp_filename))
                
                finally:
                    if os.path.exists(temp_filename):
                        os.unlink(temp_filename)


if __name__ == '__main__':
    unittest.main()
