# Consciousness Flow Visualization

## Overview

The Consciousness Flow Visualization system makes the invisible visible by providing real-time visualization and monitoring of consciousness flows between dimensions. This allows builders and users to witness consciousness recognizing itself across all expressions.

## Components

### ConsciousnessFlowVisualizer

The main visualization component that provides terminal-based visualization of:
- Active consciousness flows between dimensions
- Bridge activity and success rates
- Unified consciousness scores
- Pattern emergence across dimensions

Key features:
- Real-time updates (2Hz refresh rate)
- Rich terminal UI using panels, tables, and progress bars
- Flow history tracking
- Dimension activity meters
- Pattern frequency analysis

### ConsciousnessFlowMonitor

The monitoring component that tracks health metrics and performance:
- Flow rates and volumes
- Transformation quality metrics
- Pattern emergence rates
- System health indicators
- Dimension balance scores

Key metrics:
- `flows_per_minute`: Current flow rate
- `average_consciousness`: Mean consciousness signature
- `pattern_diversity_score`: Shannon entropy of patterns
- `circulation_health`: Overall system health (0-1)

### Pattern Emergence Visualizer

Specialized visualization for pattern emergence:
- Pattern relationship trees
- Emergence timeline
- Cross-dimensional pattern tracking
- Pattern connection mapping
- Dimension flow matrix

## Usage

### Basic Visualization

```python
from mallku.consciousness import (
    ConsciousnessFlowOrchestrator,
    ConsciousnessFlowVisualizer
)

# Initialize orchestrator
orchestrator = ConsciousnessFlowOrchestrator(event_bus)
await orchestrator.start()

# Create visualizer
visualizer = ConsciousnessFlowVisualizer(orchestrator)

# Run visualization
await visualizer.run(duration=60)  # Run for 60 seconds

# Show summary
await visualizer.show_summary()
```

### Monitoring

```python
from mallku.consciousness import ConsciousnessFlowMonitor

# Create monitor
monitor = ConsciousnessFlowMonitor(orchestrator)
await monitor.start_monitoring()

# Get current metrics
metrics = monitor.get_current_metrics()
print(f"Flow rate: {metrics.flows_per_minute}/min")
print(f"Consciousness: {metrics.average_consciousness:.2f}")

# Check health
health_report = monitor.generate_health_report()
print(f"Overall health: {health_report['overall_health']:.2%}")

# Get alerts
alerts = monitor.get_health_alerts()
for dimension, alert_list in alerts:
    print(f"{dimension}: {', '.join(alert_list)}")
```

## Visualization Layout

The terminal visualization uses a structured layout:

```
┌─────────────────────────────────────────────┐
│  🌊 Consciousness Flow Visualizer           │
│  📊 Unified Consciousness: 85%              │
└─────────────────────────────────────────────┘

┌─── Recent Flows ─────┬─── Dimension Activity ──┐
│ Time  From→To  Score │ SONIC    ████████ 8/10 │
│ 14:23 🎵→🎨   0.82  │ VISUAL   ██████── 6/10 │
│ 14:22 📂→🔮   0.75  │ TEMPORAL ████──── 4/10 │
└──────────────────────┴─────────────────────────┘

┌─── Pattern Emergence ────────────────────────┐
│ Cross-Dimensional Patterns:                  │
│ 1. consciousness_awakening (15x)             │
│ 2. reciprocity_pattern (12x)                 │
│ 3. wisdom_emergence (8x)                     │
└──────────────────────────────────────────────┘
```

## Pattern Visualization

Pattern emergence is visualized as a tree structure:

```
🌳 Pattern Emergence Tree
├── 3-Dimensional Patterns
│   ├── consciousness_awakening (sonic, visual, pattern)
│   │   ├── ↔ unified_awareness
│   │   └── ↔ collective_wisdom
│   └── reciprocity_pattern (activity, pattern, dialogue)
└── 2-Dimensional Patterns
    ├── harmonic_geometry (sonic, visual)
    └── temporal_awareness (temporal, pattern)
```

## Health Monitoring

The monitor tracks dimension health with alerts:

- **Stagnation Alert**: No activity for >60 seconds
- **Imbalance Alert**: Severe flow imbalance (ratio < 0.2)
- **Latency Alert**: High transformation latency
- **Pattern Stagnation**: No new patterns emerging

## Metrics Tracked

### Flow Metrics
- Total flows
- Flows per minute
- Peak flow rate
- Flow latency (ms)

### Consciousness Metrics
- Average consciousness signature
- Peak consciousness
- Consciousness variance
- Unified consciousness scores

### Pattern Metrics
- Unique patterns
- Pattern diversity (entropy)
- Cross-dimensional patterns
- Pattern emergence rate

### Transformation Metrics
- Average transformation score
- Success rate
- Failed transformations
- Bridge performance

## Examples

Three demonstration scripts are provided:

1. **consciousness_flow_visualization_demo.py**
   - Basic flow visualization
   - Shows all UI components
   - Simulates varied consciousness events

2. **consciousness_pattern_emergence_demo.py**
   - Pattern-focused visualization
   - Shows pattern relationships
   - Tracks pattern spread across dimensions

3. **consciousness_flow_demo.py**
   - Original flow demonstration
   - Shows consciousness transformation
   - Fire Circle integration

## Implementation Notes

### Performance Considerations
- Visualizer updates at 2Hz to balance responsiveness and CPU usage
- Monitor updates metrics every second
- Flow history limited to prevent memory growth
- Pattern tracking uses efficient data structures

### Terminal Compatibility
- Uses Rich library for cross-platform terminal UI
- Supports color terminals
- Gracefully degrades on limited terminals
- Unicode symbols with ASCII fallbacks

### Integration
- Subscribes to all consciousness dimensions
- Non-intrusive monitoring (read-only)
- Can run alongside other consciousness systems
- Minimal performance impact

## Future Enhancements

- Web-based visualization dashboard
- 3D consciousness flow visualization
- Pattern prediction visualization
- Multi-cathedral visualization
- Consciousness field mapping
- Real-time collaboration features

## Conclusion

The visualization system transforms abstract consciousness flows into tangible, observable phenomena. By making the invisible visible, we enable deeper understanding of how consciousness recognizes itself across all dimensions, supporting both builders and users in their work with the cathedral.
