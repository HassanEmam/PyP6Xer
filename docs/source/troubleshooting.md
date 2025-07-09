# Installation and Troubleshooting

This guide covers installation, common issues, and troubleshooting for PyP6Xer.

## Installation

### Requirements

- Python 3.7 or higher
- No external dependencies (PyP6Xer uses only Python standard library)

### Install from PyPI

```bash
pip install PyP6XER
```

### Install from Source

```bash
git clone https://github.com/yourusername/PyP6Xer.git
cd PyP6Xer
pip install -e .
```

### Verify Installation

```python
import xerparser
from xerparser.reader import Reader

# Test with a sample XER file
try:
    xer = Reader("sample.xer")
    print("PyP6Xer installed successfully!")
    print(f"Projects found: {len(xer.projects)}")
except Exception as e:
    print(f"Installation issue: {e}")
```

## Common Issues and Solutions

### File Loading Issues

#### Issue: FileNotFoundError
```
FileNotFoundError: [Errno 2] No such file or directory: 'project.xer'
```

**Solution:**
```python
import os

# Check if file exists
if os.path.exists("project.xer"):
    xer = Reader("project.xer")
else:
    print("File not found. Check the file path.")

# Use absolute path
xer = Reader(r"C:\path\to\your\project.xer")
```

#### Issue: UnicodeDecodeError
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x92 in position 1234
```

**Solution:**
This occurs with XER files that have special characters or were created with different encoding.

```python
# PyP6Xer handles this automatically, but if issues persist:
import codecs

# Try different encodings
encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

for encoding in encodings_to_try:
    try:
        with codecs.open("project.xer", 'r', encoding=encoding) as f:
            content = f.read()
        print(f"File readable with {encoding} encoding")
        break
    except UnicodeDecodeError:
        continue
```

#### Issue: Empty or Corrupted XER File
```
AttributeError: 'NoneType' object has no attribute 'strip'
```

**Solution:**
```python
def validate_xer_file(filename):
    """Validate XER file format."""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline()
            if not first_line.startswith('ERMHDR'):
                print("Warning: File doesn't appear to be a valid XER file")
                return False
        return True
    except Exception as e:
        print(f"File validation error: {e}")
        return False

# Use validation before loading
if validate_xer_file("project.xer"):
    xer = Reader("project.xer")
else:
    print("Invalid XER file")
```

### Memory Issues

#### Issue: MemoryError with Large Files
```
MemoryError: Unable to allocate array
```

**Solution:**
```python
import gc

# For very large XER files, monitor memory usage
def load_large_xer(filename):
    """Load large XER files with memory management."""
    
    print("Loading large XER file...")
    
    # Force garbage collection before loading
    gc.collect()
    
    try:
        xer = Reader(filename)
        print(f"Loaded successfully: {len(xer.activities)} activities")
        return xer
    except MemoryError:
        print("File too large for available memory")
        print("Consider:")
        print("- Splitting the XER file")
        print("- Using a machine with more RAM")
        print("- Processing subsets of data")
        return None

xer = load_large_xer("large_project.xer")
```

### Data Access Issues

#### Issue: AttributeError for Missing Properties
```
AttributeError: 'Task' object has no attribute 'some_property'
```

**Solution:**
```python
# Always check if properties exist before accessing
def safe_get_property(obj, property_name, default=None):
    """Safely get object property."""
    return getattr(obj, property_name, default)

# Example usage
for activity in xer.activities:
    duration = safe_get_property(activity, 'target_drtn_hr_cnt', 0)
    start_date = safe_get_property(activity, 'target_start_date')
    
    if start_date:
        print(f"Activity: {activity.task_name}, Start: {start_date}")
```

#### Issue: None Values in Calculations
```
TypeError: unsupported operand type(s) for +: 'NoneType' and 'float'
```

**Solution:**
```python
# Handle None values in calculations
def safe_sum(values):
    """Sum values, treating None as 0."""
    return sum(v for v in values if v is not None)

# Example: Calculate total cost
total_cost = safe_sum([
    assignment.target_cost for assignment in xer.activityresources
])

# Or use default values
for assignment in xer.activityresources:
    cost = assignment.target_cost or 0  # Use 0 if None
    hours = assignment.target_qty or 0
```

### Date Handling Issues

#### Issue: Date Parsing Errors
```
ValueError: time data '2023-13-45 25:70' does not match format '%Y-%m-%d %H:%M'
```

**Solution:**
```python
from datetime import datetime

def safe_parse_date(date_string, format_string='%Y-%m-%d %H:%M'):
    """Safely parse date strings."""
    if not date_string or date_string.strip() == '':
        return None
    
    try:
        return datetime.strptime(date_string.strip(), format_string)
    except ValueError as e:
        print(f"Date parsing error: {date_string} - {e}")
        return None

# Use with activities
for activity in xer.activities:
    if hasattr(activity, 'target_start_date') and activity.target_start_date:
        # PyP6Xer handles this automatically, but for custom parsing:
        start_date = safe_parse_date(str(activity.target_start_date))
```

### Performance Issues

#### Issue: Slow Processing of Large Projects

**Solution:**
```python
import time

def optimize_large_project_processing(xer):
    """Optimize processing for large projects."""
    
    start_time = time.time()
    
    # Create lookup dictionaries for faster access
    activity_lookup = {a.task_id: a for a in xer.activities}
    resource_lookup = {r.rsrc_id: r for r in xer.resources}
    
    print(f"Created lookups in {time.time() - start_time:.2f} seconds")
    
    # Use lookups instead of iterating
    def find_activity(task_id):
        return activity_lookup.get(task_id)
    
    def find_resource(rsrc_id):
        return resource_lookup.get(rsrc_id)
    
    return activity_lookup, resource_lookup

# Usage
activity_lookup, resource_lookup = optimize_large_project_processing(xer)
```

### Export Issues

#### Issue: Writing Modified XER Files
```
Exception: You have to provide the filename
```

**Solution:**
```python
# Always provide filename for export
try:
    xer.write("modified_project.xer")
    print("Export successful")
except Exception as e:
    print(f"Export failed: {e}")

# Validate export
def validate_export(original_file, exported_file):
    """Validate exported XER file."""
    try:
        original = Reader(original_file)
        exported = Reader(exported_file)
        
        print(f"Original activities: {len(original.activities)}")
        print(f"Exported activities: {len(exported.activities)}")
        
        if len(original.activities) == len(exported.activities):
            print("✅ Export validation passed")
        else:
            print("⚠️ Activity count mismatch")
            
    except Exception as e:
        print(f"Export validation failed: {e}")

# Usage
xer.write("output.xer")
validate_export("input.xer", "output.xer")
```

## Performance Tips

### Memory Optimization

```python
import gc

def process_large_xer_efficiently(filename):
    """Process large XER files efficiently."""
    
    # Load file
    xer = Reader(filename)
    
    # Process in chunks if needed
    chunk_size = 1000
    activities = xer.activities
    
    for i in range(0, len(activities), chunk_size):
        chunk = activities[i:i + chunk_size]
        
        # Process chunk
        for activity in chunk:
            # Your processing here
            pass
        
        # Force garbage collection after each chunk
        gc.collect()
    
    return xer
```

### Efficient Data Access

```python
def create_efficient_lookups(xer):
    """Create efficient lookup structures."""
    
    lookups = {
        'activities_by_project': {},
        'activities_by_wbs': {},
        'resources_by_type': {},
        'assignments_by_activity': {},
        'assignments_by_resource': {}
    }
    
    # Group activities by project
    for activity in xer.activities:
        proj_id = activity.proj_id
        if proj_id not in lookups['activities_by_project']:
            lookups['activities_by_project'][proj_id] = []
        lookups['activities_by_project'][proj_id].append(activity)
    
    # Group activities by WBS
    for activity in xer.activities:
        wbs_id = activity.wbs_id
        if wbs_id not in lookups['activities_by_wbs']:
            lookups['activities_by_wbs'][wbs_id] = []
        lookups['activities_by_wbs'][wbs_id].append(activity)
    
    # Group resources by type
    for resource in xer.resources:
        rsrc_type = resource.rsrc_type
        if rsrc_type not in lookups['resources_by_type']:
            lookups['resources_by_type'][rsrc_type] = []
        lookups['resources_by_type'][rsrc_type].append(resource)
    
    # Group assignments
    for assignment in xer.activityresources:
        # By activity
        task_id = assignment.task_id
        if task_id not in lookups['assignments_by_activity']:
            lookups['assignments_by_activity'][task_id] = []
        lookups['assignments_by_activity'][task_id].append(assignment)
        
        # By resource
        rsrc_id = assignment.rsrc_id
        if rsrc_id not in lookups['assignments_by_resource']:
            lookups['assignments_by_resource'][rsrc_id] = []
        lookups['assignments_by_resource'][rsrc_id].append(assignment)
    
    return lookups

# Usage
lookups = create_efficient_lookups(xer)

# Fast access to project activities
project_activities = lookups['activities_by_project'].get(project_id, [])
```

## Debugging Tips

### Enable Debug Information

```python
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

def debug_xer_loading(filename):
    """Load XER with debug information."""
    
    print(f"Loading XER file: {filename}")
    
    try:
        # Check file size
        import os
        file_size = os.path.getsize(filename)
        print(f"File size: {file_size:,} bytes")
        
        # Load and report progress
        start_time = time.time()
        xer = Reader(filename)
        load_time = time.time() - start_time
        
        print(f"Loaded in {load_time:.2f} seconds")
        print(f"Projects: {len(xer.projects)}")
        print(f"Activities: {len(xer.activities)}")
        print(f"Resources: {len(xer.resources)}")
        print(f"Relationships: {len(xer.relations)}")
        
        return xer
        
    except Exception as e:
        print(f"Error loading XER: {e}")
        import traceback
        traceback.print_exc()
        return None

# Usage
xer = debug_xer_loading("project.xer")
```

### Data Validation

```python
def validate_xer_data(xer):
    """Validate XER data integrity."""
    
    issues = []
    
    # Check for orphaned activities
    project_ids = {p.proj_id for p in xer.projects}
    for activity in xer.activities:
        if activity.proj_id not in project_ids:
            issues.append(f"Orphaned activity: {activity.task_id}")
    
    # Check for missing resources
    resource_ids = {r.rsrc_id for r in xer.resources}
    for assignment in xer.activityresources:
        if assignment.rsrc_id not in resource_ids:
            issues.append(f"Missing resource: {assignment.rsrc_id}")
    
    # Check for circular dependencies
    # (Simplified check - full implementation would be more complex)
    
    if issues:
        print("Data validation issues found:")
        for issue in issues[:10]:  # Show first 10
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more issues")
    else:
        print("✅ Data validation passed")
    
    return len(issues) == 0

# Usage
if xer:
    validate_xer_data(xer)
```

## Getting Help

### Community Resources

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Latest documentation and examples
- **Stack Overflow**: Use tag `pyp6xer` for questions

### Reporting Issues

When reporting issues, please include:

1. **Python version**: `python --version`
2. **PyP6Xer version**: `pip show PyP6XER`
3. **Error message**: Full traceback
4. **Sample XER file**: If possible (remove sensitive data)
5. **Operating system**: Windows, macOS, Linux

### Performance Profiling

```python
import cProfile
import pstats

def profile_xer_processing(filename):
    """Profile XER processing performance."""
    
    def process_xer():
        xer = Reader(filename)
        # Your processing code here
        for activity in xer.activities:
            duration = activity.duration
        return xer
    
    # Profile the code
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = process_xer()
    
    profiler.disable()
    
    # Print results
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions
    
    return result

# Usage
# xer = profile_xer_processing("large_project.xer")
```
