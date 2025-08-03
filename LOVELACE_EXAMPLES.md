# Lovelace Card Examples for Grasplet Integration

## Data Usage Gauge Card

Here's how to create a visual gauge showing data usage percentage:

```yaml
type: gauge
name: Data Usage
entity: sensor.your_sim_name_data_usage_percentage
min: 0
max: 100
severity:
  green: 0
  yellow: 70
  red: 90
```

## Complete SIM Monitoring Dashboard

```yaml
type: vertical-stack
cards:
  - type: gauge
    name: Data Usage
    entity: sensor.your_sim_name_data_usage_percentage
    min: 0
    max: 100
    severity:
      green: 0
      yellow: 70
      red: 90
    
  - type: entities
    title: SIM Details
    entities:
      - entity: sensor.your_sim_name_status
      - entity: sensor.your_sim_name_plan
      - entity: sensor.your_sim_name_data_limit
      - entity: sensor.your_sim_name_data_remaining
      - entity: sensor.your_sim_name_expiry_date
      - entity: sensor.your_sim_name_availability_zone
```

## Progress Bar Card (Alternative to Gauge)

```yaml
type: custom:bar-card
entity: sensor.your_sim_name_data_usage_percentage
title: Data Usage
direction: up
height: 40
color: var(--primary-color)
```

## Mini Graph Card

```yaml
type: custom:mini-graph-card
entity: sensor.your_sim_name_data_usage_percentage
name: Data Usage Trend
hours_to_show: 24
points_per_hour: 1
```

## Multiple SIMs Overview

```yaml
type: grid
columns: 2
square: false
cards:
  - type: gauge
    name: SIM 1 Usage
    entity: sensor.sim1_data_usage_percentage
    min: 0
    max: 100
    
  - type: gauge
    name: SIM 2 Usage
    entity: sensor.sim2_data_usage_percentage
    min: 0
    max: 100
```

## Installation Notes

- Replace `your_sim_name` with your actual SIM device name
- The gauge card is built into Home Assistant
- For progress bars, install the "Bar Card" custom component
- For mini graphs, install the "Mini Graph Card" custom component 