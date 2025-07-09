#!/usr/bin/env python3
"""
Verification script to test the specific fixes implemented for:
1. KeyError when SCHEDOPTIONS is missing from XER files
2. ValueError when add_date or other date fields are missing or empty in PROJECT data
"""

import tempfile
import os
from unittest.mock import MagicMock
from xerparser.write import writeXER
from xerparser.model.classes.project import Project
from xerparser.model.classes.data import Data


def test_scheduleoptions_missing():
    """Test that writeXER doesn't crash when SCHEDOPTIONS is missing"""
    print("Testing SCHEDOPTIONS missing scenario...")
    
    # Create a mock reader without scheduleoptions attribute
    mock_reader = MagicMock()
    
    # Set up minimal required attributes for writeXER
    required_attrs = [
        'currencies', 'fintmpls', 'nonworks', 'obss', 'pcattypes',
        'resourcecurves', 'udftypes', 'accounts', 'pcatvals',
        'projects', 'calendars', 'projpcats', 'wbss', 'resources',
        'acttypes', 'resourcerates', 'activities', 'actvcodes',
        'relations', 'taskprocs', 'activityresources', 'activitycodes',
        'udfvalues'
    ]
    
    for attr in required_attrs:
        setattr(mock_reader, attr, MagicMock())
        getattr(mock_reader, attr).get_tsv.return_value = []
    
    # Make sure scheduleoptions attribute doesn't exist
    if hasattr(mock_reader, 'scheduleoptions'):
        delattr(mock_reader, 'scheduleoptions')
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # This should not raise a KeyError
        writeXER(mock_reader, temp_filename)
        print("✓ SCHEDOPTIONS missing test passed - no KeyError raised")
        
        # Verify file was created
        assert os.path.exists(temp_filename), "Output file should be created"
        print("✓ Output file created successfully")
        
    except Exception as e:
        print(f"✗ SCHEDOPTIONS missing test failed: {e}")
        raise
    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_scheduleoptions_empty():
    """Test that writeXER doesn't crash when SCHEDOPTIONS is empty"""
    print("\nTesting SCHEDOPTIONS empty scenario...")
    
    # Create a mock reader with empty scheduleoptions
    mock_reader = MagicMock()
    
    # Set up minimal required attributes for writeXER
    required_attrs = [
        'currencies', 'fintmpls', 'nonworks', 'obss', 'pcattypes',
        'resourcecurves', 'udftypes', 'accounts', 'pcatvals',
        'projects', 'calendars', 'projpcats', 'wbss', 'resources',
        'acttypes', 'resourcerates', 'activities', 'actvcodes',
        'relations', 'taskprocs', 'activityresources', 'activitycodes',
        'udfvalues'
    ]
    
    for attr in required_attrs:
        setattr(mock_reader, attr, MagicMock())
        getattr(mock_reader, attr).get_tsv.return_value = []
    
    # Set up empty scheduleoptions
    mock_reader.scheduleoptions = MagicMock()
    mock_reader.scheduleoptions.__len__.return_value = 0
    mock_reader.scheduleoptions.get_tsv.return_value = []
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xer') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # This should not raise any error
        writeXER(mock_reader, temp_filename)
        print("✓ SCHEDOPTIONS empty test passed - no errors raised")
        
        # Verify file was created
        assert os.path.exists(temp_filename), "Output file should be created"
        print("✓ Output file created successfully")
        
    except Exception as e:
        print(f"✗ SCHEDOPTIONS empty test failed: {e}")
        raise
    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_project_empty_add_date():
    """Test that Project creation doesn't crash with empty add_date"""
    print("\nTesting Project with empty add_date scenario...")
    
    data = Data()
    
    # Test cases for problematic add_date values
    test_cases = [
        {"proj_id": "1", "add_date": ""},           # Empty string
        {"proj_id": "2", "add_date": "   "},        # Whitespace only
        {"proj_id": "3"},                           # Missing add_date
        {"proj_id": "4", "add_date": None},         # None value
        {"proj_id": "5", "add_date": "invalid"},    # Invalid date format
    ]
    
    for i, params in enumerate(test_cases):
        try:
            project = Project(params, data)
            print(f"✓ Test case {i+1} passed: {params}")
            
            # Test that get_tsv() works without crashing
            tsv = project.get_tsv()
            print(f"  ✓ get_tsv() worked, add_date field: {tsv[32]}")
            
        except Exception as e:
            print(f"✗ Test case {i+1} failed with {params}: {e}")
            raise


def test_project_valid_add_date():
    """Test that Project creation still works correctly with valid add_date"""
    print("\nTesting Project with valid add_date scenario...")
    
    data = Data()
    
    params = {
        "proj_id": "1", 
        "proj_short_name": "Test Project",
        "add_date": "2023-06-15 09:30"
    }
    
    try:
        project = Project(params, data)
        print("✓ Project created successfully with valid add_date")
        
        # Verify the add_date was parsed correctly
        assert project.add_date is not None, "add_date should be parsed"
        print(f"  ✓ add_date parsed as: {project.add_date}")
        
        # Test that get_tsv() formats the date correctly
        tsv = project.get_tsv()
        formatted_date = tsv[32]  # add_date is at index 32
        assert formatted_date == "2023-06-15 09:30", f"Expected '2023-06-15 09:30', got '{formatted_date}'"
        print(f"  ✓ get_tsv() formatted add_date correctly: {formatted_date}")
        
    except Exception as e:
        print(f"✗ Valid add_date test failed: {e}")
        raise


def main():
    """Run all verification tests"""
    print("Running PyP6Xer fixes verification...")
    print("=" * 50)
    
    try:
        test_scheduleoptions_missing()
        test_scheduleoptions_empty()
        test_project_empty_add_date()
        test_project_valid_add_date()
        
        print("\n" + "=" * 50)
        print("✓ All verification tests passed!")
        print("The fixes are working correctly and maintain backward compatibility.")
        
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"✗ Verification failed: {e}")
        raise


if __name__ == "__main__":
    main()
