# Advanced Examples

This section provides comprehensive examples for complex project management scenarios using PyP6Xer.

## Schedule Analysis

### Critical Path Analysis

```python
from xerparser.reader import Reader
from datetime import datetime, timedelta

def analyze_critical_path(xer_file):
    """Comprehensive critical path analysis."""
    
    xer = Reader(xer_file)
    
    print("CRITICAL PATH ANALYSIS")
    print("=" * 50)
    
    for project in xer.projects:
        print(f"\nProject: {project.proj_short_name}")
        
        activities = project.activities
        critical_activities = []
        near_critical = []
        
        for activity in activities:
            if activity.total_float_hr_cnt is not None:
                # Convert float to days
                float_days = activity.total_float_hr_cnt / (activity.calendar.day_hr_cnt or 8)
                
                if float_days <= 0:
                    critical_activities.append((activity, float_days))
                elif float_days <= 5:  # Near critical
                    near_critical.append((activity, float_days))
        
        # Sort by float (most negative first)
        critical_activities.sort(key=lambda x: x[1])
        near_critical.sort(key=lambda x: x[1])
        
        print(f"Critical Activities (≤0 days float): {len(critical_activities)}")
        for activity, float_days in critical_activities:
            status = "●" if activity.status_code == "TK_Active" else "○"
            print(f"  {status} {activity.task_code}: {activity.task_name}")
            print(f"    Float: {float_days:.1f} days | Duration: {activity.duration:.1f} days")
        
        print(f"\nNear Critical (1-5 days float): {len(near_critical)}")
        for activity, float_days in near_critical[:10]:  # Show top 10
            status = "●" if activity.status_code == "TK_Active" else "○"
            print(f"  {status} {activity.task_code}: {activity.task_name}")
            print(f"    Float: {float_days:.1f} days")

# Usage
analyze_critical_path("project.xer")
```

### Schedule Performance Analysis

```python
def schedule_performance_analysis(xer_file):
    """Analyze schedule performance and variance."""
    
    xer = Reader(xer_file)
    
    print("SCHEDULE PERFORMANCE ANALYSIS")
    print("=" * 50)
    
    today = datetime.now()
    
    for project in xer.projects:
        print(f"\nProject: {project.proj_short_name}")
        
        activities = project.activities
        performance_metrics = {
            'on_time': 0,
            'ahead': 0,
            'behind': 0,
            'not_started_late': 0,
            'total_variance_days': 0
        }
        
        for activity in activities:
            if activity.target_start_date and activity.target_end_date:
                target_start = activity.target_start_date
                target_end = activity.target_end_date
                
                if activity.status_code == "TK_Complete":
                    # Completed activities - check actual vs planned
                    if activity.act_end_date:
                        variance = (activity.act_end_date - target_end).days
                        performance_metrics['total_variance_days'] += variance
                        
                        if variance <= 0:
                            performance_metrics['ahead'] += 1
                        elif variance <= 3:  # Within 3 days
                            performance_metrics['on_time'] += 1
                        else:
                            performance_metrics['behind'] += 1
                
                elif activity.status_code == "TK_NotStart":
                    # Not started activities - check if start date has passed
                    if target_start < today:
                        performance_metrics['not_started_late'] += 1
        
        # Calculate averages
        total_analyzed = (performance_metrics['on_time'] + 
                         performance_metrics['ahead'] + 
                         performance_metrics['behind'])
        
        if total_analyzed > 0:
            avg_variance = performance_metrics['total_variance_days'] / total_analyzed
            
            print(f"Completed Activities Analysis:")
            print(f"  Ahead of Schedule: {performance_metrics['ahead']} ({performance_metrics['ahead']/total_analyzed*100:.1f}%)")
            print(f"  On Time (±3 days): {performance_metrics['on_time']} ({performance_metrics['on_time']/total_analyzed*100:.1f}%)")
            print(f"  Behind Schedule: {performance_metrics['behind']} ({performance_metrics['behind']/total_analyzed*100:.1f}%)")
            print(f"  Average Variance: {avg_variance:.1f} days")
        
        print(f"Not Started (Past Due): {performance_metrics['not_started_late']}")

# Usage
schedule_performance_analysis("project.xer")
```

## Resource Management

### Resource Leveling Analysis

```python
def resource_leveling_analysis(xer_file):
    """Analyze resource conflicts and over-allocation."""
    
    xer = Reader(xer_file)
    
    print("RESOURCE LEVELING ANALYSIS")
    print("=" * 50)
    
    from collections import defaultdict
    from datetime import timedelta
    
    # Group assignments by resource and date
    resource_schedule = defaultdict(lambda: defaultdict(float))
    
    for assignment in xer.activityresources:
        if not assignment.target_qty or not assignment.target_start_date:
            continue
            
        # Find the activity to get duration
        activity = None
        for task in xer.activities:
            if task.task_id == assignment.task_id:
                activity = task
                break
        
        if not activity or not activity.target_start_date or not activity.target_end_date:
            continue
        
        # Simple daily allocation (assumes even distribution)
        duration_days = (activity.target_end_date - activity.target_start_date).days
        if duration_days <= 0:
            duration_days = 1
            
        daily_hours = assignment.target_qty / duration_days
        
        # Add to each day in the duration
        current_date = activity.target_start_date.date()
        end_date = activity.target_end_date.date()
        
        while current_date <= end_date:
            resource_schedule[assignment.rsrc_id][current_date] += daily_hours
            current_date += timedelta(days=1)
    
    # Find over-allocations
    overallocated_resources = {}
    for rsrc_id, schedule in resource_schedule.items():
        # Find resource details
        resource = None
        for r in xer.resources:
            if r.rsrc_id == rsrc_id:
                resource = r
                break
        
        if not resource:
            continue
        
        # Assume 8 hours per day max (could use calendar)
        max_daily_hours = 8
        
        overallocation_days = []
        for date, hours in schedule.items():
            if hours > max_daily_hours:
                overallocation_days.append((date, hours))
        
        if overallocation_days:
            overallocated_resources[resource] = overallocation_days
    
    # Report over-allocations
    print(f"Over-allocated Resources: {len(overallocated_resources)}")
    
    for resource, overallocations in overallocated_resources.items():
        print(f"\nResource: {resource.rsrc_name}")
        print(f"Over-allocation Days: {len(overallocations)}")
        
        # Show worst days
        worst_days = sorted(overallocations, key=lambda x: x[1], reverse=True)[:5]
        for date, hours in worst_days:
            print(f"  {date}: {hours:.1f} hours (excess: {hours-8:.1f})")

# Usage
resource_leveling_analysis("project.xer")
```

### Resource Cost Analysis

```python
def resource_cost_analysis(xer_file):
    """Comprehensive resource cost breakdown."""
    
    xer = Reader(xer_file)
    
    print("RESOURCE COST ANALYSIS")
    print("=" * 50)
    
    from collections import defaultdict
    
    cost_breakdown = defaultdict(lambda: {
        'planned_cost': 0,
        'actual_cost': 0,
        'remaining_cost': 0,
        'assignments': 0
    })
    
    total_costs = {
        'planned': 0,
        'actual': 0,
        'remaining': 0
    }
    
    # Analyze each assignment
    for assignment in xer.activityresources:
        rsrc_id = assignment.rsrc_id
        
        # Get costs
        planned = assignment.target_cost or 0
        actual = (assignment.act_reg_cost or 0) + (assignment.act_ot_cost or 0)
        remaining = assignment.remain_cost or 0
        
        cost_breakdown[rsrc_id]['planned_cost'] += planned
        cost_breakdown[rsrc_id]['actual_cost'] += actual
        cost_breakdown[rsrc_id]['remaining_cost'] += remaining
        cost_breakdown[rsrc_id]['assignments'] += 1
        
        total_costs['planned'] += planned
        total_costs['actual'] += actual
        total_costs['remaining'] += remaining
    
    # Create resource lookup
    resource_lookup = {r.rsrc_id: r for r in xer.resources}
    
    # Sort by planned cost
    sorted_resources = sorted(
        cost_breakdown.items(),
        key=lambda x: x[1]['planned_cost'],
        reverse=True
    )
    
    print(f"Total Project Costs:")
    print(f"  Planned: ${total_costs['planned']:,.2f}")
    print(f"  Actual: ${total_costs['actual']:,.2f}")
    print(f"  Remaining: ${total_costs['remaining']:,.2f}")
    print(f"  Total (Actual + Remaining): ${total_costs['actual'] + total_costs['remaining']:,.2f}")
    
    if total_costs['planned'] > 0:
        variance = (total_costs['actual'] + total_costs['remaining']) - total_costs['planned']
        variance_pct = (variance / total_costs['planned']) * 100
        print(f"  Variance: ${variance:,.2f} ({variance_pct:+.1f}%)")
    
    print(f"\nTop 10 Resources by Planned Cost:")
    print("-" * 80)
    print(f"{'Resource':<30} {'Planned':>12} {'Actual':>12} {'Remaining':>12} {'Variance':>12}")
    print("-" * 80)
    
    for rsrc_id, costs in sorted_resources[:10]:
        resource = resource_lookup.get(rsrc_id)
        name = resource.rsrc_name if resource else f"Resource {rsrc_id}"
        
        planned = costs['planned_cost']
        actual = costs['actual_cost']
        remaining = costs['remaining_cost']
        variance = (actual + remaining) - planned
        
        print(f"{name:<30} ${planned:>11,.0f} ${actual:>11,.0f} ${remaining:>11,.0f} ${variance:>+11,.0f}")

# Usage
resource_cost_analysis("project.xer")
```

## Progress Tracking

### Earned Value Analysis

```python
def earned_value_analysis(xer_file):
    """Calculate Earned Value Management metrics."""
    
    xer = Reader(xer_file)
    
    print("EARNED VALUE ANALYSIS")
    print("=" * 50)
    
    for project in xer.projects:
        print(f"\nProject: {project.proj_short_name}")
        
        activities = project.activities
        
        # Calculate EVM metrics
        planned_value = 0      # PV - Budgeted cost of work scheduled
        earned_value = 0       # EV - Budgeted cost of work performed  
        actual_cost = 0        # AC - Actual cost of work performed
        
        for activity in activities:
            # Get resource assignments for this activity
            assignments = [a for a in xer.activityresources if a.task_id == activity.task_id]
            
            activity_planned = sum(a.target_cost or 0 for a in assignments)
            activity_actual = sum((a.act_reg_cost or 0) + (a.act_ot_cost or 0) for a in assignments)
            
            # Earned value based on physical percent complete
            if activity.phys_complete_pct:
                activity_earned = activity_planned * (activity.phys_complete_pct / 100)
            else:
                activity_earned = 0
            
            planned_value += activity_planned
            earned_value += activity_earned
            actual_cost += activity_actual
        
        # Calculate EVM metrics
        if planned_value > 0 and earned_value > 0:
            # Schedule Performance Index
            spi = earned_value / planned_value if planned_value > 0 else 0
            
            # Cost Performance Index  
            cpi = earned_value / actual_cost if actual_cost > 0 else 0
            
            # Schedule Variance
            sv = earned_value - planned_value
            
            # Cost Variance
            cv = earned_value - actual_cost
            
            # Estimate at Completion
            eac = planned_value / cpi if cpi > 0 else planned_value
            
            # Estimate to Complete
            etc = eac - actual_cost
            
            print(f"Budget at Completion (BAC): ${planned_value:,.2f}")
            print(f"Planned Value (PV): ${planned_value:,.2f}")
            print(f"Earned Value (EV): ${earned_value:,.2f}")
            print(f"Actual Cost (AC): ${actual_cost:,.2f}")
            print()
            print(f"Cost Performance Index (CPI): {cpi:.3f}")
            print(f"Schedule Performance Index (SPI): {spi:.3f}")
            print()
            print(f"Cost Variance (CV): ${cv:,.2f}")
            print(f"Schedule Variance (SV): ${sv:,.2f}")
            print()
            print(f"Estimate at Completion (EAC): ${eac:,.2f}")
            print(f"Estimate to Complete (ETC): ${etc:,.2f}")
            print()
            
            # Interpretations
            if cpi < 0.9:
                print("⚠️  COST PERFORMANCE: Significantly over budget")
            elif cpi < 1.0:
                print("🔶 COST PERFORMANCE: Over budget")
            elif cpi > 1.1:
                print("✅ COST PERFORMANCE: Significantly under budget")
            else:
                print("🟢 COST PERFORMANCE: On budget")
            
            if spi < 0.9:
                print("⚠️  SCHEDULE PERFORMANCE: Significantly behind schedule")
            elif spi < 1.0:
                print("🔶 SCHEDULE PERFORMANCE: Behind schedule")
            elif spi > 1.1:
                print("✅ SCHEDULE PERFORMANCE: Ahead of schedule")
            else:
                print("🟢 SCHEDULE PERFORMANCE: On schedule")

# Usage
earned_value_analysis("project.xer")
```

## Quality Assurance

### Schedule Quality Check

```python
def schedule_quality_check(xer_file):
    """Comprehensive schedule quality assessment following best practices."""
    
    xer = Reader(xer_file)
    
    print("SCHEDULE QUALITY CHECK")
    print("=" * 50)
    
    issues = []
    recommendations = []
    
    for project in xer.projects:
        print(f"\nProject: {project.proj_short_name}")
        
        activities = project.activities
        total_activities = len(activities)
        
        # Check 1: Activities without predecessors (except start milestones)
        no_predecessors = [a for a in activities 
                          if not a.predecessors and a.task_type != "TT_Mile" 
                          and a.status_code != "TK_Complete"]
        
        if len(no_predecessors) > 1:
            issues.append(f"Multiple activities without predecessors: {len(no_predecessors)}")
        
        # Check 2: Activities without successors (except finish milestones)
        no_successors = [a for a in activities 
                        if not a.successors and a.task_type != "TT_FinMile"
                        and a.status_code != "TK_Complete"]
        
        if len(no_successors) > 1:
            issues.append(f"Multiple activities without successors: {len(no_successors)}")
        
        # Check 3: Long duration activities (>20 days)
        long_activities = [a for a in activities 
                          if a.duration and a.duration > 20 
                          and a.task_type not in ["TT_Mile", "TT_FinMile", "TT_LOE"]]
        
        if long_activities:
            issues.append(f"Activities with duration >20 days: {len(long_activities)}")
        
        # Check 4: Activities with excessive float (>30 days)
        high_float = []
        for activity in activities:
            if activity.total_float_hr_cnt:
                float_days = activity.total_float_hr_cnt / (activity.calendar.day_hr_cnt or 8)
                if float_days > 30 and activity.status_code != "TK_Complete":
                    high_float.append(activity)
        
        if high_float:
            issues.append(f"Activities with excessive float (>30 days): {len(high_float)}")
        
        # Check 5: Missing resource assignments
        no_resources = [a for a in activities 
                       if not a.resources and a.task_type not in ["TT_Mile", "TT_FinMile"]
                       and a.status_code != "TK_Complete"]
        
        if no_resources:
            issues.append(f"Activities without resource assignments: {len(no_resources)}")
        
        # Check 6: Hard constraints
        hard_constraints = [a for a in activities 
                           if a.cstr_type in ["CS_MSO", "CS_MEO"]
                           and a.status_code != "TK_Complete"]
        
        constraint_pct = (len(hard_constraints) / total_activities) * 100
        if constraint_pct > 5:  # More than 5% hard constrained
            issues.append(f"High percentage of hard constraints: {constraint_pct:.1f}%")
        
        # Check 7: Missing calendars
        no_calendar = [a for a in activities if not a.clndr_id]
        if no_calendar:
            issues.append(f"Activities without calendar assignment: {len(no_calendar)}")
        
        # Check 8: Negative float
        negative_float = []
        for activity in activities:
            if activity.total_float_hr_cnt and activity.total_float_hr_cnt < 0:
                negative_float.append(activity)
        
        if negative_float:
            issues.append(f"Activities with negative float: {len(negative_float)}")
        
        # Report results
        print(f"Total Activities: {total_activities}")
        print()
        
        if issues:
            print("⚠️  ISSUES FOUND:")
            for issue in issues:
                print(f"  • {issue}")
        else:
            print("✅ No major issues found")
        
        # Calculate quality score
        total_checks = 8
        issues_found = len(issues)
        quality_score = ((total_checks - issues_found) / total_checks) * 100
        
        print(f"\nSchedule Quality Score: {quality_score:.0f}%")
        
        if quality_score >= 90:
            print("🟢 Excellent schedule quality")
        elif quality_score >= 75:
            print("🔶 Good schedule quality")
        elif quality_score >= 60:
            print("🔶 Fair schedule quality - improvements recommended")
        else:
            print("⚠️  Poor schedule quality - significant improvements needed")

# Usage
schedule_quality_check("project.xer")
```

## Data Export and Reporting

### Comprehensive Project Report

```python
def generate_project_report(xer_file, output_file="project_report.txt"):
    """Generate a comprehensive project report."""
    
    xer = Reader(xer_file)
    
    with open(output_file, 'w') as f:
        def write_line(text=""):
            f.write(text + "\n")
            print(text)
        
        write_line("PROJECT ANALYSIS REPORT")
        write_line("=" * 50)
        write_line(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        write_line()
        
        for project in xer.projects:
            write_line(f"PROJECT: {project.proj_short_name}")
            write_line(f"Full Name: {project.proj_name}")
            write_line(f"Start Date: {project.plan_start_date}")
            write_line(f"End Date: {project.plan_end_date}")
            write_line()
            
            activities = project.activities
            
            # Activity summary
            write_line("ACTIVITY SUMMARY")
            write_line("-" * 30)
            
            status_counts = {}
            for activity in activities:
                status = activity.status_code
                status_counts[status] = status_counts.get(status, 0) + 1
            
            write_line(f"Total Activities: {len(activities)}")
            for status, count in status_counts.items():
                status_name = {
                    "TK_NotStart": "Not Started",
                    "TK_Active": "In Progress",
                    "TK_Complete": "Complete"
                }.get(status, status)
                pct = (count / len(activities)) * 100
                write_line(f"  {status_name}: {count} ({pct:.1f}%)")
            
            write_line()
            
            # Critical path
            write_line("CRITICAL PATH")
            write_line("-" * 30)
            
            critical = [a for a in activities 
                       if a.total_float_hr_cnt is not None and a.total_float_hr_cnt <= 0]
            
            write_line(f"Critical Activities: {len(critical)}")
            for activity in critical[:10]:  # Top 10
                write_line(f"  {activity.task_code}: {activity.task_name}")
            
            write_line()
            
            # Resource summary
            write_line("RESOURCE SUMMARY")
            write_line("-" * 30)
            
            resource_types = {}
            for resource in xer.resources:
                rtype = resource.rsrc_type
                resource_types[rtype] = resource_types.get(rtype, 0) + 1
            
            for rtype, count in resource_types.items():
                type_name = {
                    "RT_Labor": "Labor",
                    "RT_Mat": "Material", 
                    "RT_Equip": "Equipment"
                }.get(rtype, rtype)
                write_line(f"  {type_name}: {count}")
            
            write_line()
    
    print(f"\nReport saved to: {output_file}")

# Usage
generate_project_report("project.xer")
```

These examples demonstrate advanced PyP6Xer capabilities for professional project management analysis. Each function can be customized and extended based on specific project requirements.
