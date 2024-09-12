#!/usr/bin/env python
import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BBR.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.error(f"Couldn't import Django: {str(exc)}")
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Additional functionality and models from the scraping app
    try:
        from scraping.models import ScrapedData
        from scraping.utils import run_spider
        
        logger.info("Running the scraping spider...")
        try:
            run_spider()
            logger.info("Scraping spider completed successfully.")
        except Exception as e:
            logger.error(f"Error occurred while running the scraping spider: {str(e)}")
            raise
        
        logger.info("Processing scraped data...")
        try:
            scraped_data = ScrapedData.objects.filter(approved=False)
            for data in scraped_data:
                # Perform any necessary data processing or validation
                data.approved = True
                data.save()
            logger.info("Scraped data processed successfully.")
        except Exception as e:
            logger.error(f"Error occurred while processing scraped data: {str(e)}")
            raise
        
    except ImportError as exc:
        logger.error(f"Couldn't import the necessary modules: {str(exc)}")
        raise ImportError(
            "Couldn't import the necessary models or perform the required setup. "
            "Please check your project structure and dependencies."
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

