import unittest
import sys
import os
import tempfile
from unittest.mock import MagicMock, patch, mock_open
from io import StringIO

# Add the parent directory to the path so we can import xerparser
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xerparser.write import writeXER
from xerparser.model.schedoptions import SchedOptions


class TestWriteXERScheduleOptionsFixes(unittest.TestCase):
    """Test cases for writeXER function SCHEDOPTIONS fixes"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_reader = MagicMock()
        
        # Set up default mock returns for required attributes
        self.mock_reader.currencies.get_tsv.return_value = []
        self.mock_reader.fintmpls.get_tsv.return_value = []
        self.mock_reader.nonworks.get_tsv.return_value = []
        self.mock_reader.obss.get_tsv.return_value = []
        self.mock_reader.pcattypes.get_tsv.return_value = []
        self.mock_reader.resourcecurves.get_tsv.return_value = []
        self.mock_reader.udftypes.get_tsv.return_value = []
        self.mock_reader.accounts.get_tsv.return_value = []
        self.mock_reader.pcatvals.get_tsv.return_value = []
        self.mock_reader.projects.get_tsv.return_value = []
        self.mock_reader.calendars.get_tsv.return_value = []
        self.mock_reader.projpcats.get_tsv.return_value = []
        self.mock_reader.wbss.get_tsv.return_value = []
        self.mock_reader.resources.get_tsv.return_value = []
        self.mock_reader.acttypes.get_tsv.return_value = []
        self.mock_reader.resourcerates.get_tsv.return_value = []
        self.mock_reader.activities.get_tsv.return_value = []
        self.mock_reader.actvcodes.get_tsv.return_value = []
        self.mock_reader.relations.get_tsv.return_value = []
        self.mock_reader.taskprocs.get_tsv.return_value = []
        self.mock_reader.activityresources.get_tsv.return_value = []
        self.mock_reader.activitycodes.get_tsv.return_value = []
        self.mock_reader.udfvalues.get_tsv.return_value = []
    
    def test_write_xer_with_valid_scheduleoptions(self):
        """Test writeXER when scheduleoptions exists and has data"""
        # Set up scheduleoptions with data
        mock_schedoptions = MagicMock()
        mock_schedoptions.__len__.return_value = 2  # Has data
        mock_schedoptions.get_tsv.return_value = [
            ['%T', 'SCHEDOPTIONS'],
            ['%F', 'schedoptions_id', 'proj_id'],
            ['%R', '1', '1']
        ]
        self.mock_reader.scheduleoptions = mock_schedoptions
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Call writeXER
            writeXER(self.mock_reader, temp_filename)
            
            # Verify scheduleoptions was called
            mock_schedoptions.get_tsv.assert_called_once()
            
            # Read the file and verify SCHEDOPTIONS was written
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn('SCHEDOPTIONS', content)
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_write_xer_with_empty_scheduleoptions(self):
        """Test writeXER when scheduleoptions exists but is empty"""
        # Set up empty scheduleoptions
        mock_schedoptions = MagicMock()
        mock_schedoptions.__len__.return_value = 0  # Empty
        mock_schedoptions.get_tsv.return_value = []
        self.mock_reader.scheduleoptions = mock_schedoptions
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Call writeXER
            writeXER(self.mock_reader, temp_filename)
            
            # Verify scheduleoptions.get_tsv was NOT called (since it's empty)
            mock_schedoptions.get_tsv.assert_not_called()
            
            # Read the file and verify SCHEDOPTIONS was NOT written
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertNotIn('SCHEDOPTIONS', content)
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_write_xer_with_none_scheduleoptions(self):
        """Test writeXER when scheduleoptions is None"""
        # Set scheduleoptions to None
        self.mock_reader.scheduleoptions = None
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Call writeXER - should not raise an error
            writeXER(self.mock_reader, temp_filename)
            
            # Read the file and verify SCHEDOPTIONS was NOT written
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertNotIn('SCHEDOPTIONS', content)
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_write_xer_without_scheduleoptions_attribute(self):
        """Test writeXER when reader doesn't have scheduleoptions attribute"""
        # Remove scheduleoptions attribute
        if hasattr(self.mock_reader, 'scheduleoptions'):
            delattr(self.mock_reader, 'scheduleoptions')
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Call writeXER - should not raise an error
            writeXER(self.mock_reader, temp_filename)
            
            # Read the file and verify SCHEDOPTIONS was NOT written
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertNotIn('SCHEDOPTIONS', content)
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_write_xer_with_scheduleoptions_error(self):
        """Test writeXER when scheduleoptions.get_tsv() raises a specific error"""
        # Set up scheduleoptions that raises an AttributeError (realistic scenario)
        mock_schedoptions = MagicMock()
        mock_schedoptions.__len__.return_value = 1  # Has data
        mock_schedoptions.get_tsv.side_effect = AttributeError("'NoneType' object has no attribute 'get_tsv'")
        self.mock_reader.scheduleoptions = mock_schedoptions
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Call writeXER - should not raise an error due to try-catch
            writeXER(self.mock_reader, temp_filename)
            
            # Read the file and verify SCHEDOPTIONS was NOT written
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertNotIn('SCHEDOPTIONS', content)
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_write_xer_with_scheduleoptions_type_error(self):
        """Test writeXER when scheduleoptions.get_tsv() raises a TypeError"""
        # Set up scheduleoptions that raises a TypeError (realistic scenario)
        mock_schedoptions = MagicMock()
        mock_schedoptions.__len__.return_value = 1  # Has data
        mock_schedoptions.get_tsv.side_effect = TypeError("object is not iterable")
        self.mock_reader.scheduleoptions = mock_schedoptions
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Call writeXER - should not raise an error due to try-catch
            writeXER(self.mock_reader, temp_filename)
            
            # Read the file and verify SCHEDOPTIONS was NOT written
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertNotIn('SCHEDOPTIONS', content)
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_write_xer_header_and_footer(self):
        """Test that writeXER still writes proper header and footer"""
        # Set scheduleoptions to None
        self.mock_reader.scheduleoptions = None
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Call writeXER
            writeXER(self.mock_reader, temp_filename)
            
            # Read the file and verify header and footer
            with open(temp_filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                # Check header
                self.assertTrue(lines[0].startswith('ERMHDR'))
                
                # Check footer
                self.assertEqual(lines[-1].strip(), '%E')
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_write_xer_other_sections_still_written(self):
        """Test that other sections are still written when scheduleoptions is missing"""
        # Set scheduleoptions to None
        self.mock_reader.scheduleoptions = None
        
        # Set up some mock data for other sections
        self.mock_reader.projects.get_tsv.return_value = [
            ['%T', 'PROJECT'],
            ['%F', 'proj_id', 'proj_short_name'],
            ['%R', '1', 'Test Project']
        ]
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Call writeXER
            writeXER(self.mock_reader, temp_filename)
            
            # Read the file and verify other sections were written
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Should have PROJECT section
                self.assertIn('PROJECT', content)
                self.assertIn('Test Project', content)
                
                # Should NOT have SCHEDOPTIONS
                self.assertNotIn('SCHEDOPTIONS', content)
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


class TestScheduleOptionsBackwardCompatibility(unittest.TestCase):
    """Test cases to ensure backward compatibility for scheduleoptions"""
    
    def test_schedoptions_normal_operation(self):
        """Test that normal SchedOptions operation still works"""
        schedoptions = SchedOptions()
        
        # Test that it can be created and has expected methods
        self.assertTrue(hasattr(schedoptions, 'add'))
        self.assertTrue(hasattr(schedoptions, 'get_tsv'))
        self.assertTrue(hasattr(schedoptions, '__len__'))
        
        # Test initial state
        self.assertEqual(len(schedoptions), 0)
        self.assertEqual(schedoptions.get_tsv(), [])


if __name__ == '__main__':
    unittest.main()
