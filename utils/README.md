### 📘 How to Use in Any Script

Add this at the top of your scripts:

```python
from utils.config_loader import load_config
```

And use it after parsing arguments:

including in the scripts

```python
parser.add_argument('--config', help='Path to YAML config file (optional)')
```


```python
config = load_config(args)
regex = config.get('filter', {}).get('regex', args.regex)
```

This now enables centralized and elegant YAML config support across all toolkit modules.
