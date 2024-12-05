# localaws

Run local Python scripts with different AWS profiles - perfect for local testing and development.

## Installation

```bash
pip install localaws
```

## Usage

Basic usage:
```bash
localaws script.py -p dev-profile
```

Full options:
```bash
localaws script.py --profile dev-profile --region us-west-2 --verbose
```

Short options:
```bash
localaws script.py -p dev-profile -r us-west-2 -v
```

## Features

- 🚀 Quick switch between AWS profiles for local testing
- ✅ AWS profile validation before execution
- 🌎 AWS region support
- 📦 Proper Python path handling
- 🔍 Verbose logging option
- ❌ Clean error handling with helpful messages
- 🔄 Cross-platform compatibility

## Common Use Cases

1. Testing AWS Lambda functions locally with different profiles:
```bash
localaws lambda_function.py -p test-profile
```

2. Running scripts against different AWS environments:
```bash
localaws deploy_script.py -p staging-profile
localaws deploy_script.py -p production-profile
```

3. Local development with different AWS accounts:
```bash
localaws dev_script.py -p personal-aws -r us-east-1
```

## Requirements

- Python 3.7+
- boto3
- click

## Development

Clone and install in development mode:
```bash
git clone https://github.com/yourusername/localaws.git
cd localaws
pip install -e .
```

Run tests:
```bash
pytest tests/
```

## License

MIT License - See LICENSE file for details