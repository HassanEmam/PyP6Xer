# PyP6Xer Documentation

Welcome to **PyP6Xer**, a powerful Python library for parsing and manipulating Primavera P6 XER files.

*Documentation last updated: July 2025*

## Overview

PyP6Xer is an open-source Python library that provides a comprehensive solution for reading, parsing, and writing Primavera P6 XER (eXchange ERport) files. It allows you to extract project data, activities, resources, calendars, and relationships from P6 exports and work with them programmatically.

## Key Features

- **Complete XER File Parsing**: Parse all major XER file components including projects, activities, WBS, resources, calendars, and relationships
- **Object-Oriented Design**: Clean, intuitive API with well-structured classes representing P6 entities
- **Data Export**: Write modified data back to XER format
- **Comprehensive Coverage**: Support for activities, resources, calendars, codes, relationships, and more
- **Easy Integration**: Simple Python API that integrates easily into existing workflows
- **Open Source**: Licensed under GNU LGPL v2.1

## Quick Start

### Installation

```bash
pip install PyP6XER
```

### Basic Usage

```python
from xerparser.reader import Reader

# Load an XER file
xer = Reader("project.xer")

# Access projects
for project in xer.projects:
    print(f"Project: {project.proj_short_name}")
    
    # Access activities in the project
    for activity in project.activities:
        print(f"  Activity: {activity.task_name}")
        print(f"  Duration: {activity.target_drtn_hr_cnt} hours")
        print(f"  Status: {activity.status_code}")

# Access resources
for resource in xer.resources:
    print(f"Resource: {resource.rsrc_name}")

# Access relationships
for relation in xer.relations:
    print(f"Relationship: {relation.pred_task_id} -> {relation.task_id}")
```

## Table of Contents

```{toctree}
:maxdepth: 2
:caption: User Guide

getting_started
quick_reference
examples
advanced_examples
troubleshooting
```

```{toctree}
:maxdepth: 2
:caption: API Reference

api/xerparser/index
```

```{toctree}
:maxdepth: 1
:caption: Development

contributing
changelog
license
```

## Supported XER Elements

PyP6Xer supports parsing and manipulation of the following XER file elements:

### Core Project Elements
- **Projects**: Project information, settings, and metadata
- **Activities (Tasks)**: Project activities with durations, dates, and status
- **WBS**: Work Breakdown Structure hierarchy
- **Relationships**: Activity dependencies and logic links

### Resources and Assignments
- **Resources**: Human and material resources
- **Resource Assignments**: Activity-resource assignments
- **Resource Rates**: Cost and pricing information
- **Resource Categories**: Resource classification

### Scheduling and Time
- **Calendars**: Working time definitions and exceptions
- **Schedule Options**: Project scheduling parameters

### Classification and Codes
- **Activity Codes**: Custom activity classification
- **Activity Types**: Predefined activity classifications
- **UDF Types and Values**: User-defined fields

### Financial
- **Accounts**: Cost account structure
- **Currencies**: Multi-currency support
- **Financial Templates**: Cost templates

### Organizational
- **OBS**: Organizational Breakdown Structure
- **Roles**: Resource roles and responsibilities

## Project Structure

The library is organized into several key modules:

- `xerparser.reader`: Main parsing functionality
- `xerparser.writer`: XER file output functionality
- `xerparser.model`: Core data model classes
- `xerparser.model.classes`: Individual entity classes (Project, Task, Resource, etc.)

## License

PyP6Xer is licensed under the GNU Lesser General Public License v2.1. See the [License](license.md) page for full details.

## Support and Contributing

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/HassanEmam/PyP6Xer/issues)
- **Contributing**: See the [Contributing Guide](contributing.md)
- **Community**: Join discussions on project development

## Indices and Tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
