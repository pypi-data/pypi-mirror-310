import pytest
from localaws.utils import validate_aws_profile
import os
import configparser
import tempfile

def test_validate_aws_profile():
    # Create temporary AWS credentials file
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ['HOME'] = tmp_dir
        os.makedirs(os.path.join(tmp_dir, '.aws'))
        
        # Create credentials file with test profile
        credentials_path = os.path.join(tmp_dir, '.aws', 'credentials')
        config = configparser.ConfigParser()
        config['test-profile'] = {
            'aws_access_key_id': 'test',
            'aws_secret_access_key': 'test'
        }
        with open(credentials_path, 'w') as f:
            config.write(f)
        
        assert validate_aws_profile('test-profile') == True
        assert validate_aws_profile('non-existent-profile') == False
