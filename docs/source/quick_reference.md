# Quick Reference

This page provides quick code snippets for common PyP6Xer operations. For detailed explanations, see the [Getting Started Guide](getting_started.md).

## Installation

```bash
pip install PyP6XER
```

## Basic Usage

### Import and Load XER File

```python
from xerparser.reader import Reader

# Load XER file
xer = Reader("project.xer")
```

### Access Projects

```python
# Get all projects
for project in xer.projects:
    print(f"Project: {project.proj_short_name}")
    print(f"Activities: {len(project.activities)}")
```

### Access Activities

```python
# Get first project
project = xer.projects[0]

# Iterate through activities
for activity in project.activities:
    print(f"Activity: {activity.task_name}")
    print(f"Duration: {activity.duration} days")
    print(f"Start: {activity.early_start_date}")
    print(f"Finish: {activity.early_end_date}")
```

### Access Resources

```python
# Get all resources
for resource in xer.resources:
    print(f"Resource: {resource.rsrc_name}")
    print(f"Type: {resource.rsrc_type}")
```

### Access Calendars

```python
# Get all calendars
for calendar in xer.calendars:
    print(f"Calendar: {calendar.clndr_name}")
    print(f"Hours per day: {calendar.day_hr_cnt}")
```

## One-Liners

```python
# Count total activities across all projects
total_activities = sum(len(p.activities) for p in xer.projects)

# Get all activity names
activity_names = [act.task_name for p in xer.projects for act in p.activities]

# Find activities by status
active_tasks = [act for p in xer.projects for act in p.activities 
                if act.status_code == "TK_Active"]

# Get all resource assignments
assignments = [ra for ra in xer.taskrsrcs]

# Find critical path activities (zero total float)
critical_activities = [act for p in xer.projects for act in p.activities 
                      if act.total_float_hr_cnt == 0]
```

## Common Patterns

### Error Handling

```python
from xerparser.reader import Reader

try:
    xer = Reader("project.xer")
    print(f"Successfully loaded {len(xer.projects)} projects")
except Exception as e:
    print(f"Error loading XER file: {e}")
```

### Data Export

```python
import csv

# Export activities to CSV
with open('activities.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Project', 'Activity', 'Duration', 'Start', 'Finish'])
    
    for project in xer.projects:
        for activity in project.activities:
            writer.writerow([
                project.proj_short_name,
                activity.task_name,
                activity.duration,
                activity.early_start_date,
                activity.early_end_date
            ])
```

### Filtering and Analysis

```python
# Filter activities by date range
from datetime import datetime

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

filtered_activities = [
    act for p in xer.projects for act in p.activities
    if act.early_start_date and start_date <= act.early_start_date <= end_date
]
```

## Editing Relationships

```python
from xerparser.write import writeXER

# Add a finish-to-start relationship (tasks validated, IDs auto-allocated)
rel = xer.relations.add_relationship(
    task_id=1003, pred_task_id=1002, pred_type="PR_FS", lag_hr_cnt=8.0)

# Re-route or remove
xer.relations.replace_relationship(rel, pred_task_id=1001, pred_type="PR_SS")
xer.relations.remove_relationship(rel)     # by object or by task_pred_id

writeXER(xer, "rescheduled.xer")

# Query from Tasks (unambiguous direction)
xer.activities.get_predecessors(1002)      # relationships feeding 1002
xer.activities.get_successors(1002)        # relationships leaving 1002
```

## Any-Table Access

```python
# Every table in the file, modelled or not, lossless
steps = xer.tables["WBSSTEP"]
print(sorted(xer.tables.keys()))
```

## DCMA 14-Point Analysis

```python
from xerparser.dcma14.analysis import DCMA14

# Perform DCMA analysis
analysis = DCMA14(xer)
results = analysis.analysis()

# Print summary
print(f"Activities with no predecessors: {results['analysis']['predecessors']['cnt']}")
print(f"Activities with no successors: {results['analysis']['successors']['cnt']}")
print(f"Critical activities: {results['analysis']['critical']['cnt']}")
print(f"CPLI: {results['analysis']['cpli']['cpli']}")
print(f"BEI: {results['analysis']['bei']['bei']}")
```

## Running the Tests

```bash
python -m pytest tests/ -q          # full suite, 280+ tests
```

For more detailed examples and advanced usage, see:
- [Examples](examples.md)
- [Getting Started Guide](getting_started.md)
- [API Reference](api/xerparser/index.rst)
