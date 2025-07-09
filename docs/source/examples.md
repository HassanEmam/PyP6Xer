# Examples

This section provides practical examples of using PyP6Xer for common project management tasks.

## File Operations

### Loading Multiple XER Files

```python
from xerparser.reader import Reader
import glob

# Load all XER files in a directory
xer_files = []
for filename in glob.glob("*.xer"):
    try:
        xer = Reader(filename)
        xer_files.append(xer)
        print(f"Loaded: {filename}")
    except Exception as e:
        print(f"Failed to load {filename}: {e}")
```

### Writing XER Files

```python
from xerparser.reader import Reader

# Load and modify data
xer = Reader("input.xer")

# Make modifications to the data...
# (See modification examples below)

# Write to a new file
xer.write("output.xer")
print("XER file written successfully")
```

## Project Analysis

### Project Summary Report

```python
def project_summary(xer_file):
    """Generate a comprehensive project summary."""
    
    for project in xer_file.projects:
        print(f"\n{'='*50}")
        print(f"PROJECT SUMMARY: {project.proj_short_name}")
        print(f"{'='*50}")
        
        # Basic info
        print(f"Project Name: {project.proj_name}")
        print(f"Project Manager: {project.proj_mgr}")
        print(f"Status: {project.status_code}")
        
        # Dates
        print(f"\nSCHEDULE:")
        print(f"Data Date: {project.last_recalc_date}")
        print(f"Planned Start: {project.plan_start_date}")
        print(f"Planned Finish: {project.plan_end_date}")
        
        # Activity statistics
        activities = project.activities
        total_activities = len(activities)
        
        not_started = len([a for a in activities if a.status_code == "TK_NotStart"])
        in_progress = len([a for a in activities if a.status_code == "TK_Active"])
        completed = len([a for a in activities if a.status_code == "TK_Complete"])
        
        print(f"\nACTIVITIES:")
        print(f"Total: {total_activities}")
        print(f"Not Started: {not_started}")
        print(f"In Progress: {in_progress}")
        print(f"Completed: {completed}")
        
        # Progress calculation
        if total_activities > 0:
            completion_pct = (completed / total_activities) * 100
            print(f"Completion: {completion_pct:.1f}%")

# Usage
xer = Reader("project.xer")
project_summary(xer)
```

### Critical Path Analysis

```python
def critical_path_analysis(project):
    """Analyze the critical path of a project."""
    
    activities = project.activities
    critical_activities = [a for a in activities if a.driving_path_flag == "Y"]
    
    print(f"CRITICAL PATH ANALYSIS")
    print(f"{'='*30}")
    print(f"Total Activities: {len(activities)}")
    print(f"Critical Activities: {len(critical_activities)}")
    
    if critical_activities:
        print(f"\nCRITICAL PATH ACTIVITIES:")
        print(f"{'ID':<15} {'Name':<40} {'Duration':<12} {'Float'}")
        print(f"{'-'*80}")
        
        for activity in critical_activities:
            print(f"{activity.task_code:<15} "
                  f"{activity.task_name[:40]:<40} "
                  f"{activity.target_drtn_hr_cnt or 0:<12} "
                  f"{activity.total_float_hr_cnt or 0}")

# Usage
project = xer.projects[0]
critical_path_analysis(project)
```

## Filtering Data

(filtering-data)=

### Activity Filtering

```python
def filter_activities(activities, **filters):
    """Filter activities based on various criteria."""
    
    filtered = activities
    
    # Filter by status
    if 'status' in filters:
        filtered = [a for a in filtered if a.status_code == filters['status']]
    
    # Filter by date range
    if 'start_after' in filters:
        start_date = filters['start_after']
        filtered = [a for a in filtered 
                   if a.act_start_date and a.act_start_date >= start_date]
    
    # Filter by duration
    if 'min_duration' in filters:
        min_dur = filters['min_duration']
        filtered = [a for a in filtered 
                   if a.target_drtn_hr_cnt and a.target_drtn_hr_cnt >= min_dur]
    
    # Filter by WBS
    if 'wbs_name' in filters:
        wbs_name = filters['wbs_name']
        filtered = [a for a in filtered 
                   if wbs_name.lower() in (a.wbs_name or "").lower()]
    
    return filtered

# Usage examples
project = xer.projects[0]
activities = project.activities

# Get all active activities
active = filter_activities(activities, status="TK_Active")

# Get long-duration activities (> 40 hours)
long_activities = filter_activities(activities, min_duration=40)

# Get activities in specific WBS
design_activities = filter_activities(activities, wbs_name="Design")
```

### Resource Utilization

```python
def resource_utilization_report(xer_file):
    """Generate a resource utilization report."""
    
    resources = xer_file.resources
    assignments = xer_file.activityresources
    
    print(f"RESOURCE UTILIZATION REPORT")
    print(f"{'='*50}")
    
    for resource in resources:
        # Find all assignments for this resource
        resource_assignments = [a for a in assignments 
                              if a.rsrc_id == resource.rsrc_id]
        
        total_budget = sum(a.target_qty or 0 for a in resource_assignments)
        total_actual = sum(a.act_reg_qty or 0 for a in resource_assignments)
        
        print(f"\nResource: {resource.rsrc_name}")
        print(f"  Type: {resource.rsrc_type}")
        print(f"  Assignments: {len(resource_assignments)}")
        print(f"  Budgeted Hours: {total_budget}")
        print(f"  Actual Hours: {total_actual}")
        
        if total_budget > 0:
            utilization = (total_actual / total_budget) * 100
            print(f"  Utilization: {utilization:.1f}%")

# Usage
resource_utilization_report(xer)
```

## Data Export

### Export to CSV

```python
import csv

def export_activities_to_csv(activities, filename):
    """Export activities to CSV format."""
    
    fieldnames = [
        'task_id', 'task_code', 'task_name', 'status_code',
        'target_drtn_hr_cnt', 'act_start_date', 'act_end_date',
        'phys_complete_pct', 'total_float_hr_cnt'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for activity in activities:
            row = {}
            for field in fieldnames:
                row[field] = getattr(activity, field, None)
            writer.writerow(row)
    
    print(f"Exported {len(activities)} activities to {filename}")

# Usage
project = xer.projects[0]
export_activities_to_csv(project.activities, "activities.csv")
```

### Export to JSON

```python
import json
from datetime import datetime

def activity_to_dict(activity):
    """Convert activity to dictionary for JSON export."""
    
    def serialize_date(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj
    
    return {
        'task_id': activity.task_id,
        'task_code': activity.task_code,
        'task_name': activity.task_name,
        'status_code': activity.status_code,
        'duration_hours': activity.target_drtn_hr_cnt,
        'start_date': serialize_date(activity.act_start_date),
        'end_date': serialize_date(activity.act_end_date),
        'percent_complete': activity.phys_complete_pct,
        'total_float': activity.total_float_hr_cnt,
        'wbs_id': activity.wbs_id
    }

def export_project_to_json(project, filename):
    """Export project data to JSON."""
    
    project_data = {
        'project_info': {
            'id': project.proj_id,
            'short_name': project.proj_short_name,
            'name': project.proj_name,
            'status': project.status_code
        },
        'activities': [activity_to_dict(a) for a in project.activities]
    }
    
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(project_data, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"Exported project to {filename}")

# Usage
project = xer.projects[0]
export_project_to_json(project, "project_data.json")
```

## Schedule Analysis

### Float Analysis

```python
def float_analysis(activities):
    """Analyze float (slack) in project activities."""
    
    # Filter activities with float data
    float_activities = [a for a in activities if a.total_float_hr_cnt is not None]
    
    if not float_activities:
        print("No float data available")
        return
    
    # Calculate statistics
    floats = [a.total_float_hr_cnt for a in float_activities]
    critical = [a for a in float_activities if a.total_float_hr_cnt <= 0]
    near_critical = [a for a in float_activities if 0 < a.total_float_hr_cnt <= 8]
    
    print(f"FLOAT ANALYSIS")
    print(f"{'='*30}")
    print(f"Total Activities: {len(float_activities)}")
    print(f"Critical (0 float): {len(critical)}")
    print(f"Near Critical (1-8 hrs): {len(near_critical)}")
    print(f"Average Float: {sum(floats) / len(floats):.1f} hours")
    print(f"Maximum Float: {max(floats):.1f} hours")
    
    # List critical activities
    if critical:
        print(f"\nCRITICAL ACTIVITIES:")
        for activity in critical[:10]:  # Show first 10
            print(f"  {activity.task_code}: {activity.task_name}")

# Usage
project = xer.projects[0]
float_analysis(project.activities)
```

### Calendar Analysis

```python
def calendar_analysis(xer_file):
    """Analyze calendar usage and working time."""
    
    calendars = xer_file.calendars
    
    print(f"CALENDAR ANALYSIS")
    print(f"{'='*30}")
    
    for calendar in calendars:
        print(f"\nCalendar: {calendar.clndr_name}")
        print(f"  Type: {calendar.clndr_type}")
        print(f"  Default: {'Yes' if calendar.default_flag == 'Y' else 'No'}")
        print(f"  Hours per Day: {calendar.day_hr_cnt}")
        print(f"  Hours per Week: {calendar.week_hr_cnt}")
        
        # Count activities using this calendar
        activities_count = len([a for a in xer_file.activities.get_list() 
                              if a.clndr_id == calendar.clndr_id])
        print(f"  Used by {activities_count} activities")

# Usage
calendar_analysis(xer)
```

## Advanced Examples

### Earned Value Analysis

```python
def earned_value_analysis(project):
    """Perform basic earned value analysis."""
    
    activities = project.activities
    
    # Calculate totals
    total_budget = sum(a.target_cost or 0 for a in activities)
    total_actual = sum(a.act_reg_cost or 0 for a in activities)
    
    # Calculate earned value (simplified)
    earned_value = 0
    for activity in activities:
        if activity.phys_complete_pct and activity.target_cost:
            earned_value += (activity.phys_complete_pct / 100) * activity.target_cost
    
    # Calculate variances
    cost_variance = earned_value - total_actual
    schedule_variance = earned_value - total_budget
    
    print(f"EARNED VALUE ANALYSIS")
    print(f"{'='*30}")
    print(f"Planned Value (PV): ${total_budget:,.2f}")
    print(f"Earned Value (EV): ${earned_value:,.2f}")
    print(f"Actual Cost (AC): ${total_actual:,.2f}")
    print(f"Cost Variance (CV): ${cost_variance:,.2f}")
    print(f"Schedule Variance (SV): ${schedule_variance:,.2f}")
    
    if total_actual > 0:
        cpi = earned_value / total_actual
        print(f"Cost Performance Index (CPI): {cpi:.2f}")
    
    if total_budget > 0:
        spi = earned_value / total_budget
        print(f"Schedule Performance Index (SPI): {spi:.2f}")

# Usage
project = xer.projects[0]
earned_value_analysis(project)
```

### Network Analysis

```python
def network_analysis(xer_file):
    """Analyze the project network structure."""
    
    activities = xer_file.activities.get_list()
    relationships = xer_file.relations.get_list()
    
    # Count relationship types
    relationship_types = {}
    for rel in relationships:
        rel_type = rel.pred_type
        relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
    
    # Find activities with no predecessors (start activities)
    activity_ids = {a.task_id for a in activities}
    successor_ids = {r.task_id for r in relationships}
    start_activities = activity_ids - successor_ids
    
    # Find activities with no successors (end activities)
    predecessor_ids = {r.pred_task_id for r in relationships}
    end_activities = activity_ids - predecessor_ids
    
    print(f"NETWORK ANALYSIS")
    print(f"{'='*30}")
    print(f"Total Activities: {len(activities)}")
    print(f"Total Relationships: {len(relationships)}")
    print(f"Start Activities: {len(start_activities)}")
    print(f"End Activities: {len(end_activities)}")
    
    print(f"\nRelationship Types:")
    for rel_type, count in relationship_types.items():
        print(f"  {rel_type}: {count}")

# Usage
network_analysis(xer)
```

These examples demonstrate the flexibility and power of PyP6Xer for project analysis and data manipulation. You can combine and modify these examples to suit your specific needs.
