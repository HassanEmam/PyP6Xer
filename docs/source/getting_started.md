# Getting Started

This guide will help you get up and running with PyP6Xer quickly.

## Installation

### From PyPI (Recommended)

```bash
pip install PyP6XER
```

### From Source

```bash
git clone https://github.com/HassanEmam/PyP6Xer.git
cd PyP6Xer
pip install -e .
```

## Basic Concepts

### XER Files

XER (eXchange ERport) files are tab-delimited text files exported from Primavera P6. They contain comprehensive project data including:

- Project metadata and settings
- Work Breakdown Structure (WBS)
- Activities and their properties
- Resource definitions and assignments
- Calendar definitions
- Activity relationships
- Custom codes and fields

### PyP6Xer Architecture

PyP6Xer follows an object-oriented design where each XER element type is represented by a Python class:

- **Reader**: Main entry point for parsing XER files
- **Project**: Represents a P6 project
- **Task**: Represents project activities
- **Resource**: Represents resources (labor, material, etc.)
- **WBS**: Work Breakdown Structure elements
- **Calendar**: Working time definitions

## Your First PyP6Xer Program

Here's a simple example that loads an XER file and displays basic project information:

```python
from xerparser.reader import Reader

# Load the XER file
xer_file = Reader("sample.xer")

# Display basic information
print(f"Found {xer_file.projects.count} project(s)")

# Iterate through projects
for project in xer_file.projects:
    print(f"\nProject: {project.proj_short_name}")
    print(f"Project Name: {project.proj_name}")
    print(f"Start Date: {project.plan_start_date}")
    print(f"Finish Date: {project.plan_end_date}")
    print(f"Number of Activities: {len(project.activities)}")
```

## Working with Projects

### Accessing Project Properties

```python
project = xer_file.projects[0]  # Get first project

# Basic properties
print(f"Project ID: {project.proj_id}")
print(f"Short Name: {project.proj_short_name}")
print(f"Full Name: {project.proj_name}")
print(f"Manager: {project.proj_mgr}")

# Dates
print(f"Data Date: {project.last_recalc_date}")
print(f"Planned Start: {project.plan_start_date}")
print(f"Planned Finish: {project.plan_end_date}")

# Status
print(f"Project Status: {project.status_code}")
```

### Project Activities

```python
# Get all activities in a project
activities = project.activities

print(f"Total Activities: {len(activities)}")

# Filter activities by status
active_activities = [act for act in activities if act.status_code == "TK_Active"]
print(f"Active Activities: {len(active_activities)}")

# Find critical path activities
critical_activities = [act for act in activities if act.driving_path_flag == "Y"]
print(f"Critical Activities: {len(critical_activities)}")
```

## Working with Activities

### Basic Activity Information

```python
for activity in project.activities[:5]:  # First 5 activities
    print(f"\nActivity: {activity.task_name}")
    print(f"  ID: {activity.task_code}")
    print(f"  Duration: {activity.target_drtn_hr_cnt} hours")
    print(f"  Status: {activity.status_code}")
    print(f"  % Complete: {activity.phys_complete_pct}%")
    print(f"  Start: {activity.act_start_date}")
    print(f"  Finish: {activity.act_end_date}")
```

### Activity Relationships

```python
# Get all relationships
relationships = xer_file.relations

print(f"Total Relationships: {len(relationships)}")

# Find predecessors for a specific activity
activity_id = 12345
predecessors = [rel for rel in relationships if rel.task_id == activity_id]

for pred in predecessors:
    print(f"Predecessor: {pred.pred_task_id} -> {pred.task_id}")
    print(f"  Type: {pred.pred_type}")
    print(f"  Lag: {pred.lag_hr_cnt} hours")
```

## Working with Resources

### Resource Information

```python
# Access all resources
resources = xer_file.resources

print(f"Total Resources: {len(resources)}")

for resource in resources[:5]:  # First 5 resources
    print(f"\nResource: {resource.rsrc_name}")
    print(f"  ID: {resource.rsrc_id}")
    print(f"  Type: {resource.rsrc_type}")
    print(f"  Short Name: {resource.rsrc_short_name}")
```

### Resource Assignments

```python
# Get activity-resource assignments
assignments = xer_file.activityresources

for assignment in assignments[:5]:  # First 5 assignments
    activity = assignment.task_id
    resource = assignment.rsrc_id
    print(f"Activity {activity} -> Resource {resource}")
    print(f"  Budgeted Units: {assignment.target_qty}")
    print(f"  Actual Units: {assignment.act_reg_qty}")
```

## Working with WBS

```python
# Access Work Breakdown Structure
wbs_elements = xer_file.wbss

print(f"Total WBS Elements: {len(wbs_elements)}")

# Find root WBS elements (no parent)
root_elements = [wbs for wbs in wbs_elements if not wbs.parent_wbs_id]

for wbs in root_elements:
    print(f"Root WBS: {wbs.wbs_name}")
    print(f"  Short Name: {wbs.wbs_short_name}")
    print(f"  Project Node: {wbs.proj_node_flag}")
```

## Working with Calendars

```python
# Access calendars
calendars = xer_file.calendars

for calendar in calendars:
    print(f"Calendar: {calendar.clndr_name}")
    print(f"  Type: {calendar.clndr_type}")
    print(f"  Hours per Day: {calendar.day_hr_cnt}")
    print(f"  Hours per Week: {calendar.week_hr_cnt}")
```

## Error Handling

Always wrap file operations in try-catch blocks:

```python
try:
    xer_file = Reader("project.xer")
    print("File loaded successfully")
except FileNotFoundError:
    print("XER file not found")
except Exception as e:
    print(f"Error loading file: {e}")
```

## Next Steps

- Explore the [Examples](examples.md) for more advanced usage patterns
- Check the [API Reference](api/xerparser/index.rst) for complete class documentation
- Learn about [filtering and querying](examples.md#filtering-data) techniques
