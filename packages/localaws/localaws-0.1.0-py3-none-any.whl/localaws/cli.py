import os
import sys
import logging
from pathlib import Path
import click
import boto3
import runpy
from .utils import setup_logging, validate_aws_profile

logger = logging.getLogger(__name__)

@click.command()
@click.argument('script_path', type=click.Path(exists=True))
@click.option('--profile', '-p', help='AWS profile to use')
@click.option('--region', '-r', help='AWS region to use', default='us-east-1')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.version_option()
def main(script_path, profile, region, verbose):
    """
    Run a Python script with a specific AWS profile and region.
    
    Example: runenv script.py -p dev-profile -r us-west-2
    """
    # Setup logging
    setup_logging(verbose)
    
    try:
        script_path = Path(script_path).resolve()
        logger.info(f"Running script: {script_path}")
        
        # Validate and setup AWS profile
        if profile:
            logger.info(f"Using AWS profile: {profile}")
            if not validate_aws_profile(profile):
                click.secho(f"AWS profile '{profile}' not found in credentials", fg='red', err=True)
                sys.exit(1)
            os.environ['AWS_PROFILE'] = profile
            
        if region:
            logger.info(f"Using AWS region: {region}")
            os.environ['AWS_DEFAULT_REGION'] = region
            
        # Initialize boto3 session
        if profile or region:
            try:
                session = boto3.Session(profile_name=profile, region_name=region)
                boto3.setup_default_session(profile_name=profile, region_name=region)
                # Verify credentials
                session.client('sts').get_caller_identity()
            except Exception as e:
                click.secho(f"Failed to initialize AWS session: {str(e)}", fg='red', err=True)
                sys.exit(1)
        
        # Add script's directory to Python path
        script_dir = str(script_path.parent)
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
            logger.debug(f"Added {script_dir} to Python path")
        
        # Run the target script
        logger.info("Starting script execution")
        runpy.run_path(str(script_path), run_name='__main__')
        
    except Exception as e:
        logger.error(f"Error running script: {e}", exc_info=verbose)
        click.secho(f"Error: {str(e)}", fg='red', err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
