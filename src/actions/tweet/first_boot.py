import logging
import os
from pathlib import Path
import warnings
from dotenv import load_dotenv
from runtime.config import RuntimeConfig

def send_first_boot_tweet(config: RuntimeConfig):
    """
    Send a 'Hello I'm alive' tweet on first omOS boot.
    
    Parameters
    ----------
    config : RuntimeConfig
        Runtime configuration containing agent name
    """
    logging.info("Starting first boot tweet process...")
    
    # Create .omos directory in project root if it doesn't exist
    project_root = Path(__file__).parent.parent.parent.parent
    omos_dir = project_root / '.omos'
    logging.info(f"Creating .omos directory at: {omos_dir}")
    omos_dir.mkdir(exist_ok=True)
    
    # Check if first boot marker exists
    first_boot_file = omos_dir / 'first_boot_tweet'
    logging.info(f"Checking for first boot marker at: {first_boot_file}")
    
    if first_boot_file.exists():
        logging.info("First boot tweet already sent")
        return

    try:
        # Initialize Twitter client
        logging.info("Loading environment variables...")
        load_dotenv()
        
        # Check if environment variables are loaded
        api_key = os.getenv('TWITTER_API_KEY')
        if not api_key:
            logging.error("Twitter API credentials not found in .env file")
            return
        
        logging.info("Initializing Twitter client...")
        # Suppress tweepy warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=SyntaxWarning)
            import tweepy
            
            client = tweepy.Client(
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            )
        
        # Get agent name from config
        agent_name = config.name
        logging.info(f"Agent name from config: {agent_name}")
        
        # Send first boot tweet
        tweet_text = f"🤖 Hi! I'm {agent_name}, an AI agent running on @openmind_agi's omOS platform. Excited to learn and grow with this amazing community! ✨ #AI #omOS"
        logging.info(f"Attempting to send tweet: {tweet_text}")
        
        response = client.create_tweet(text=tweet_text)
        
        # Create marker file
        first_boot_file.touch()
        
        # Log success
        tweet_id = response.data['id']
        tweet_url = f"https://twitter.com/user/status/{tweet_id}"
        logging.info(f"First boot tweet sent! URL: {tweet_url}")
        
    except Exception as e:
        logging.error(f"Failed to send first boot tweet: {str(e)}")
        # Print full exception details
        logging.exception("Full error details:")