import logging
import os
import configparser
from pathlib import Path

def setup_logging(verbose):
    """Configure logging based on verbosity level."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def validate_aws_profile(profile_name):
    """Validate that AWS profile exists in credentials or config file."""
    config = configparser.ConfigParser()
    
    # Check credentials file
    credentials_path = os.path.expanduser("~/.aws/credentials")
    if os.path.exists(credentials_path):
        config.read(credentials_path)
        if profile_name in config.sections():
            return True
    
    # Check config file
    config_path = os.path.expanduser("~/.aws/config")
    if os.path.exists(config_path):
        config.read(config_path)
        if f"profile {profile_name}" in config.sections():
            return True
    
    return False
