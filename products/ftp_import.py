import ftplib
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
import logging
import csv
from decimal import Decimal
from .scraper import scrape_competitor_prices
import xml.etree.ElementTree as ET
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FTPConnection:
    def __init__(self, host: str, user: str, password: str):
        self.host = host
        self.user = user
        self.password = password
        self.ftp = None

    def connect(self):
        try:
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.user, self.password)
            logger.info(f"Connected to FTP server: {self.host}")
        except ftplib.all_errors as e:
            logger.error(f"Failed to connect to FTP server {self.host}: {str(e)}")
            raise

    def disconnect(self):
        if self.ftp:
            self.ftp.quit()
            logger.info(f"Disconnected from FTP server: {self.host}")

    def list_files(self, directory: str) -> List[str]:
        files = []
        if self.ftp:
            self.ftp.cwd(directory)
            self.ftp.retrlines('LIST', lambda x: files.append(x.split()[-1]))
        return files

    def download_file(self, remote_path: str, local_path: str):
        if self.ftp:
            with open(local_path, 'wb') as local_file:
                self.ftp.retrbinary(f'RETR {remote_path}', local_file.write)
            logger.info(f"Downloaded {remote_path} to {local_path}")

def validate_file(file_path, file_type):
    if file_type == 'csv':
        # Implement CSV validation
        pass
    elif file_type == 'xml':
        try:
            ET.parse(file_path)
        except ET.ParseError:
            raise ValueError("Invalid XML file")
    elif file_type == 'json':
        try:
            with open(file_path) as f:
                json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file")

def process_file(file_path, file_type):
    validate_file(file_path, file_type)
    if file_type == 'csv':
        return process_csv(file_path, Decimal('0.2'))  # Default profit margin of 20%
    elif file_type == 'xml':
        # Process XML file
        pass
    elif file_type == 'json':
        # Process JSON file
        pass

def process_csv(file_path: str, profit_margin: Decimal) -> List[Dict[str, Any]]:
    processed_data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cost_price = Decimal(row['price'])
            selling_price = cost_price * (1 + profit_margin)
            
            processed_item = {
                'part_number': row['part_number'],
                'name': row['name'],
                'description': row['description'],
                'cost_price': cost_price,
                'selling_price': selling_price,
                'make': row['make'],
                'model': row['model'],
                'year': int(row['year']),
            }
            processed_data.append(processed_item)
    
    return processed_data

def adjust_prices_based_on_competitors(processed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    competitor_prices = scrape_competitor_prices()
    
    for item in processed_data:
        part_number = item['part_number']
        if part_number in competitor_prices:
            competitor_price = competitor_prices[part_number]
            if item['selling_price'] > competitor_price:
                # Adjust price to be slightly lower than competitor
                item['selling_price'] = competitor_price * Decimal('0.99')
                logger.info(f"Adjusted price for {part_number} to beat competitor")
            elif item['selling_price'] < item['cost_price']:
                # Ensure we don't sell at a loss
                item['selling_price'] = item['cost_price'] * Decimal('1.05')
                logger.warning(f"Price for {part_number} adjusted to avoid loss")
    
    return processed_data

def import_from_ftp(host: str, user: str, password: str, remote_path: str, profit_margin: Decimal) -> List[Dict[str, Any]]:
    ftp_conn = FTPConnection(host, user, password)
    try:
        ftp_conn.connect()
        files = ftp_conn.list_files(remote_path)
        
        results = []
        for file in files:
            local_path = os.path.join('temp', file)
            ftp_conn.download_file(os.path.join(remote_path, file), local_path)
            processed_data = process_file(local_path, 'csv')  # Assuming CSV files for now
            if processed_data is not None:
                adjusted_data = adjust_prices_based_on_competitors(processed_data)
                results.extend(adjusted_data)
            else:
                logger.warning(f"No data processed for file: {file}")
            os.remove(local_path)
        
        logger.info(f"Successfully imported {len(results)} products from FTP")
        return results
    except Exception as e:
        logger.error(f"Error during FTP import: {str(e)}")
        raise
    finally:
        ftp_conn.disconnect()

def import_from_multiple_ftps(ftp_configs: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    results = {}
    
    def import_worker(config):
        host = config['host']
        user = config['user']
        password = config['password']
        remote_path = config['remote_path']
        profit_margin = config.get('profit_margin', Decimal('0.2'))  # Default 20% profit margin
        
        try:
            data = import_from_ftp(host, user, password, remote_path, profit_margin)
            return host, data
        except Exception as e:
            logger.error(f"Error importing from {host}: {str(e)}")
            return host, []

    with ThreadPoolExecutor() as executor:
        for host, data in executor.map(import_worker, ftp_configs):
            results[host] = data

    return results

# Usage example:
if __name__ == "__main__":
    ftp_configs = [
        {"host": "ftp1.example.com", "user": "user1", "password": "pass1", "remote_path": "/data", "profit_margin": Decimal('0.25')},
        {"host": "ftp2.example.com", "user": "user2", "password": "pass2", "remote_path": "/files", "profit_margin": Decimal('0.3')},
    ]
    
    all_results = import_from_multiple_ftps(ftp_configs)
    for host, data in all_results.items():
        print(f"Imported {len(data)} items from {host}")
