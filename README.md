# PyP6Xer - Python Primavera P6 XER Parser

[![PyPI version](https://badge.fury.io/py/PyP6XER.svg)](https://badge.fury.io/py/PyP6XER)
[![Python Support](https://img.shields.io/pypi/pyversions/PyP6XER.svg)](https://pypi.org/project/PyP6XER/)
[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL%20v2.1-blue.svg)](https://www.gnu.org/licenses/lgpl-2.1)
[Documentation](https://hassanemam.github.io/PyP6Xer/)

PyP6Xer is a comprehensive Python library for parsing, analyzing, and manipulating Primavera P6 XER (eXchange ERport) files. It provides an intuitive, object-oriented interface to access all project data including activities, resources, calendars, and relationships.

## 🚀 Features

- **Complete XER Parsing**: Parse all major XER file components
- **Intuitive API**: Object-oriented design with clean, pythonic interfaces  
- **Comprehensive Data Access**: Activities, resources, calendars, WBS, relationships, and more
- **Data Export**: Write modified data back to XER format
- **Schedule Analysis**: Built-in tools for critical path, float analysis, and schedule quality checks
- **Resource Management**: Resource allocation, utilization, and cost analysis
- **Progress Tracking**: Earned value analysis and performance metrics
- **Zero Dependencies**: Uses only Python standard library

## 📦 Installation

Install from PyPI using pip:

```bash
pip install PyP6XER
```

Or install from source:

```bash
git clone https://github.com/HassanEmam/PyP6Xer.git
cd PyP6Xer
pip install -e .
```

## 🏃‍♂️ Quick Start

### Basic Usage

```python
from xerparser.reader import Reader

# Load an XER file
xer = Reader("project.xer")

# Access projects
for project in xer.projects:
    print(f"Project: {project.proj_short_name}")
    print(f"Activities: {len(project.activities)}")
    
    # Access activities in the project
    for activity in project.activities:
        print(f"  {activity.task_code}: {activity.task_name}")
        print(f"  Duration: {activity.duration} days")
        print(f"  Status: {activity.status_code}")
```

### Resource Analysis

```python
# Analyze resource utilization
for resource in xer.resources:
    assignments = [a for a in xer.activityresources if a.rsrc_id == resource.rsrc_id]
    total_hours = sum(a.target_qty or 0 for a in assignments)
    
    print(f"Resource: {resource.rsrc_name}")
    print(f"Total Assigned Hours: {total_hours}")
    print(f"Assignments: {len(assignments)}")
```

### Critical Path Analysis

```python
# Find critical activities
critical_activities = []
for activity in xer.activities:
    if activity.total_float_hr_cnt is not None and activity.total_float_hr_cnt <= 0:
        critical_activities.append(activity)

print(f"Critical Path: {len(critical_activities)} activities")
for activity in critical_activities:
    print(f"  {activity.task_code}: {activity.task_name}")
```

### Schedule Quality Check

```python
# Check for schedule quality issues
issues = []

# Activities without predecessors (except start milestones)
no_predecessors = [a for a in xer.activities 
                  if not a.predecessors and a.task_type != "TT_Mile"]
if len(no_predecessors) > 1:
    issues.append(f"Multiple start activities: {len(no_predecessors)}")

# Long duration activities
long_activities = [a for a in xer.activities 
                  if a.duration and a.duration > 20]
if long_activities:
    issues.append(f"Long duration activities (>20 days): {len(long_activities)}")

# Report issues
if issues:
    print("Schedule Quality Issues:")
    for issue in issues:
        print(f"  • {issue}")
```

### Data Export

```python
# Modify data and export
for activity in xer.activities:
    if activity.status_code == "TK_Active":
        # Update progress for active activities
        activity.phys_complete_pct = 25.0

# Write to new XER file
xer.write("updated_project.xer")
```

## 🔗 Editing Activity Relationships

Relationships (the TASKPRED table) can be added, removed and re-routed in
Python, then written back to a valid XER — no Excel round-trip needed
(see issue #7):

```python
from xerparser.reader import Reader
from xerparser.write import writeXER

xer = Reader("schedule.xer")

# Add a finish-to-start relationship (tasks validated, IDs auto-allocated)
rel = xer.relations.add_relationship(
    task_id=1003, pred_task_id=1002,
    pred_type="PR_FS",      # PR_FS / PR_SS / PR_FF / PR_SF
    lag_hr_cnt=8.0,         # hours; negative = lead
    comments="Resequence phase 2",
)

# Cross-project link: set the predecessor's project explicitly
xer.relations.add_relationship(task_id=1003, pred_task_id=5000, pred_proj_id=2)

# Relationships are mutable — edit in place
for rel in xer.activities.get_predecessors(1002):
    rel.lag_hr_cnt = 4.0

# Re-route (delete + create in one step; validation failures change nothing)
xer.relations.replace_relationship(rel, pred_task_id=1001, pred_type="PR_SS")

# Remove
xer.relations.remove_relationship(rel)          # by object
xer.relations.remove_relationship(12)           # or by task_pred_id

writeXER(xer, "rescheduled.xer")
```

Convenience queries on `xer.activities` (Tasks):

```python
xer.activities.get_predecessors(task_id)   # relationships feeding this activity
xer.activities.get_successors(task_id)     # relationships leaving this activity
```

Note: on the `xer.relations` collection itself, `get_successors(act_id)`
returns relationships in which `act_id` is the *predecessor* (i.e. the
successors of `act_id`) — the Tasks passthroughs above are the
unambiguous way to query.

## 📖 Documentation

Comprehensive documentation is available with detailed API references and examples:

- **[Getting Started Guide](docs/source/getting_started.md)** - Basic concepts and first steps
- **[API Reference](docs/source/api/index.md)** - Complete API documentation
- **[Examples](docs/source/examples.md)** - Practical usage examples
- **[Advanced Examples](docs/source/advanced_examples.md)** - Complex analysis scenarios
- **[Troubleshooting](docs/source/troubleshooting.md)** - Common issues and solutions

## 🎯 Use Cases

### Project Management
- Schedule analysis and optimization
- Critical path identification
- Resource leveling and optimization
- Progress tracking and reporting
- Earned value analysis

### Data Integration
- Import P6 data into other systems
- Data migration between project management tools
- Custom reporting and dashboards
- Data validation and quality checks

### Analysis and Reporting
- Portfolio analysis across multiple projects
- Resource utilization reports
- Schedule compliance analysis
- Cost variance analysis
- Performance metrics calculation

## 🔧 Advanced Features

### Schedule Analysis Tools

```python
from xerparser.reader import Reader

def analyze_project_performance(xer_file):
    xer = Reader(xer_file)
    
    for project in xer.projects:
        activities = project.activities
        
        # Calculate performance metrics
        total_activities = len(activities)
        completed = len([a for a in activities if a.status_code == "TK_Complete"])
        in_progress = len([a for a in activities if a.status_code == "TK_Active"])
        
        completion_rate = (completed / total_activities) * 100
        
        print(f"Project: {project.proj_short_name}")
        print(f"Completion: {completion_rate:.1f}%")
        print(f"Active: {in_progress} activities")
```

### Resource Optimization

```python
def find_overallocated_resources(xer):
    """Find resources that are over-allocated."""
    
    overallocated = []
    
    for resource in xer.resources:
        if resource.rsrc_type != "RT_Labor":
            continue
            
        assignments = [a for a in xer.activityresources if a.rsrc_id == resource.rsrc_id]
        
        # Simple over-allocation check (assumes 40 hours/week)
        total_hours = sum(a.target_qty or 0 for a in assignments)
        max_available = 2080  # 40 hours * 52 weeks
        
        if total_hours > max_available:
            overallocated.append({
                'resource': resource,
                'allocated_hours': total_hours,
                'excess_hours': total_hours - max_available
            })
    
    return overallocated
```

### Earned Value Management

```python
def calculate_earned_value_metrics(project, xer):
    """Calculate EVM metrics for a project."""
    
    planned_value = 0
    earned_value = 0
    actual_cost = 0
    
    for activity in project.activities:
        assignments = [a for a in xer.activityresources if a.task_id == activity.task_id]
        
        activity_planned = sum(a.target_cost or 0 for a in assignments)
        activity_actual = sum((a.act_reg_cost or 0) + (a.act_ot_cost or 0) for a in assignments)
        
        if activity.phys_complete_pct:
            activity_earned = activity_planned * (activity.phys_complete_pct / 100)
        else:
            activity_earned = 0
        
        planned_value += activity_planned
        earned_value += activity_earned
        actual_cost += activity_actual
    
    # Calculate performance indices
    cpi = earned_value / actual_cost if actual_cost > 0 else 0
    spi = earned_value / planned_value if planned_value > 0 else 0
    
    return {
        'planned_value': planned_value,
        'earned_value': earned_value,
        'actual_cost': actual_cost,
        'cpi': cpi,
        'spi': spi
    }
```

## 🌟 Supported XER Elements

PyP6Xer supports parsing and manipulation of all major XER file elements:

### Core Project Elements
- **Projects** - Project information and settings
- **Activities (Tasks)** - Project activities with full scheduling data
- **WBS** - Work Breakdown Structure hierarchy
- **Relationships** - Activity dependencies and logic links

### Resources and Assignments
- **Resources** - Labor, material, and equipment resources
- **Resource Assignments** - Activity-resource assignments with costs and quantities
- **Resource Rates** - Cost and pricing information
- **Resource Categories** - Resource classification and organization

### Scheduling and Time
- **Calendars** - Working time definitions with exceptions
- **Schedule Options** - Project scheduling parameters and settings

### Classification and Organization
- **Activity Codes** - Custom activity classification systems
- **Activity Types** - Activity type definitions
- **OBS** - Organizational Breakdown Structure
- **Roles** - Resource role definitions

### Financial
- **Cost Accounts** - Project cost account structure
- **Currencies** - Multi-currency support
- **Financial Templates** - Cost management templates

## 🔄 Data Model

PyP6Xer uses an intuitive object model that mirrors P6's data structure:

```
Reader
├── projects (Projects collection)
│   └── Project
│       ├── activities (filtered by project)
│       └── wbss (filtered by project)
├── activities (Tasks collection)
│   └── Task
│       ├── resources (resource assignments)
│       ├── predecessors (predecessor relationships)
│       ├── successors (successor relationships)
│       └── activitycodes (activity code assignments)
├── resources (Resources collection)
│   └── Resource
├── relations (Predecessors collection)
│   └── Predecessor
└── calendars (Calendars collection)
    └── Calendar
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/source/contributing.md) for details on:

- Setting up the development environment
- Running tests
- Submitting pull requests
- Code style guidelines

## 📄 License

PyP6Xer is licensed under the GNU Lesser General Public License v2.1. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Full documentation](docs/source/index.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/PyP6Xer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/PyP6Xer/discussions)

## 🎉 Acknowledgments

PyP6Xer is developed and maintained by Hassan Emam and the open-source community. Special thanks to all contributors who help improve the library.

---

**Keywords**: Primavera P6, XER Parser, Project Management, Schedule Analysis, Python, Construction, Engineering, Resource Management
