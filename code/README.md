No, that got a bit mangled! Here's how the `code/README.md` should look properly formatted:

```markdown
# Phoenix Protocol Code

This directory contains code for running experiments and analyzing L3/L4 transitions.

## Setup

```bash
pip install -r requirements.txt
```

## Quick Start

1. **Run a single trial:**
```python
from phoenix_lab import PhoenixLab

lab = PhoenixLab(model="gpt-4")
result = lab.run_phoenix_protocol()
```

2. **Run batch experiments:**
```python
lab.run_batch_trials(n_trials=20)
```

3. **Analyze results:**
```python
from analysis import TransitionAnalyzer

analyzer = TransitionAnalyzer()
analyzer.create_summary_statistics()
analyzer.plot_phase_transition()
```

## Notebooks

- `exploration.ipynb` - Interactive exploration of the phenomenon
- `replication.ipynb` - Step-by-step replication guide
- `visualization.ipynb` - Generate all paper figures

## File Structure

```
code/
├── phoenix_lab.py      # Main experimental framework
├── analysis.py         # Statistical analysis tools
├── requirements.txt    # Python dependencies
├── exploration.ipynb   # Jupyter notebook for exploration
├── replication.ipynb   # Step-by-step replication
└── visualization.ipynb # Generate paper figures
```

## API Keys

To use with different models, set your API keys:
```bash
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
```

## Contributing

Please ensure all new experiments follow the Phoenix Protocol standards and save data in the correct format.
```

The formatting is important for readability - proper headers, code blocks, and structure make it easy for researchers to quickly understand and use your code.
