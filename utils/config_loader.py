import os
import yaml

def load_config(args):
    \"\"\"Load YAML config and return as a dictionary.\"\"\"
    if getattr(args, 'config', None) and os.path.exists(args.config):
        with open(args.config, 'r') as f:
            return yaml.safe_load(f)
    return {}
