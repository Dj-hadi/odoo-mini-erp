# ISIL Manufacturing Planning Module

## Overview
This Odoo module extends the manufacturing functionality with advanced planning features and mandatory quality control checks.

## Features

### 1. Quality Control Integration
- Mandatory quality checks before marking manufacturing orders as done
- Quality check creation directly from manufacturing orders
- Pass/Fail functionality with quality scoring
- Defect tracking and notes

### 2. Bill of Materials Enhancements
- Complex product identification
- Automatic technical validation requirements for complex products
- Extended BOM views with complexity indicators

### 3. Production Planning
- Gantt chart view for production scheduling
- Workcenter capacity visualization
- Production timeline management

## Installation

1. Place this module in your Odoo addons path
2. Install the module through Odoo Apps
3. The module depends on:
   - mrp (Manufacturing)
   - quality (Quality Control)

## Usage

### Quality Control Workflow
1. Create a manufacturing order
2. Click "Create Quality Check" button
3. Perform quality inspection
4. Click "Pass" or "Fail" based on results
5. Mark manufacturing order as done (only if quality check passed)

### Production Planning
- Navigate to Manufacturing > Production Planning to view the Gantt chart
- Visualize production schedules by workcenter
- Monitor production timelines and capacities

## Technical Details

### Models Extended
- `mrp.production` - Added quality check fields and validation
- `mrp.bom` - Added complexity and technical validation fields

### New Models
- `quality.check` - Quality control records with scoring

### Views Added
- Extended manufacturing order form and tree views
- Extended BOM form and tree views
- Quality check form, tree, and search views
- Production planning Gantt view

## Testing
Run tests with: `./odoo-bin --test-enable -d test_db -i isil_manufacturing_planning`

## Dependencies
- mrp
- quality
