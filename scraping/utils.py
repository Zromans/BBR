import yake
from difflib import SequenceMatcher
import os
import subprocess
import sys
import json
import time
import logging
import requests
from bs4 import BeautifulSoup
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def extract_keywords(text, num_keywords=10):
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, _ in keywords[:num_keywords]]

def calculate_difference(old_data, new_data):
    differences = {}
    if old_data.price != new_data.price:
        price_diff = ((new_data.price - old_data.price) / old_data.price) * 100
        differences['price'] = {
            'old': str(old_data.price),
            'new': str(new_data.price),
            'diff': round(price_diff, 2)
        }
    if old_data.includes != new_data.includes:
        description_similarity = SequenceMatcher(None, old_data.includes, new_data.includes).ratio() * 100
        description_diff = 100 - description_similarity
        differences['description'] = {
            'old': old_data.includes,
            'new': new_data.includes,
            'diff': round(description_diff, 2)
        }
    if old_data.fitments != new_data.fitments:
        differences['fitments'] = {
            'old': old_data.fitments,
            'new': new_data.fitments
        }
    if old_data.brand != new_data.brand:
        differences['brand'] = {
            'old': old_data.brand,
            'new': new_data.brand
        }
    if old_data.manufacturer_part_number != new_data.manufacturer_part_number:
        differences['manufacturer_part_number'] = {
            'old': old_data.manufacturer_part_number,
            'new': new_data.manufacturer_part_number
        }
    return differences

def get_user_input_url():
    return input("Enter the web address of the homepage to be crawled: ")

def run_spider(target_directory, start_url):
    spider_script = os.path.join(target_directory, 'spider.py')
    if os.path.exists(spider_script):
        try:
            subprocess.run([sys.executable, spider_script, start_url], check=True)
            print(f"Spider run successfully in {target_directory}")
        except subprocess.CalledProcessError as e:
            print(f"Error running spider: {e}")
    else:
        print(f"Spider script not found in {target_directory}")

def get_target_directory():
    return os.path.dirname(os.path.abspath(__file__))

def validate_and_clean_data(data):
    cleaned_data = data  # Placeholder for actual cleaning logic
    return cleaned_data

def setup_logging():
    logging.basicConfig(filename='scraper.log', level=logging.INFO)
    return logging.getLogger(__name__)

def save_data_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_data_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def rate_limit(max_per_second):
    min_interval = 1.0 / max_per_second
    def decorate(func):
        last_time_called = [0.0]
        def rate_limited_function(*args, **kwargs):
            elapsed = time.time() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_time_called[0] = time.time()
            return ret
        return rate_limited_function
    return decorate

def update_product_data(existing_data, scraped_data):
    updates = {}
    for product_id, new_data in scraped_data.items():
        if product_id in existing_data:
            differences = calculate_difference(existing_data[product_id], new_data)
            if differences:
                updates[product_id] = differences
        else:
            updates[product_id] = {'new_product': new_data}
    return updates

def apply_updates(existing_data, updates):
    for product_id, update in updates.items():
        if 'new_product' in update:
            existing_data[product_id] = update['new_product']
        else:
            for field, change in update.items():
                existing_data[product_id][field] = change['new']
    return existing_data

def get_last_scrape_info():
    if os.path.exists('last_scrape.json'):
        with open('last_scrape.json', 'r') as f:
            return json.load(f)
    return None

def save_scrape_info(success, timestamp, url):
    info = {
        'success': success,
        'timestamp': timestamp,
        'url': url
    }
    with open('last_scrape.json', 'w') as f:
        json.dump(info, f)

def get_site_directory(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    directory = [link.get('href') for link in links if link.get('href') and link.get('href').startswith('/')]
    return directory

def analyze_and_log_structure(scraped_structure):
    with open('scraped_structures.log', 'a') as f:
        json.dump(scraped_structure, f)
        f.write('\n')
   
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(scraped_structure.values())
   
    num_clusters = min(5, len(scraped_structure))
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)
   
    proposed_structure = {}
    for label, content in zip(kmeans.labels_, scraped_structure.values()):
        if label not in proposed_structure:
            proposed_structure[label] = []
        proposed_structure[label].append(content)
   
    return proposed_structure

def generate_keywords(scraped_content):
    text = ' '.join(scraped_content.values())
    extracted_keywords = extract_keywords(text)
    with open('project_keywords.txt', 'a') as f:
        for keyword in extracted_keywords:
            f.write(keyword + '\n')
   
    return extracted_keywords

def process_scraped_data(scraped_data):
    proposed_structure = analyze_and_log_structure(scraped_data)
    generated_keywords = generate_keywords(scraped_data)
    return proposed_structure, generated_keywords

def analyze_directory_structure(directory):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(directory)
   
    num_clusters = min(5, len(directory))
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)
   
    clusters = {}
    for i, label in enumerate(kmeans.labels_):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(directory[i])
   
    return clusters

def optimize_keyword_strategy(keywords):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(keywords)
   
    feature_names = vectorizer.get_feature_names_out()
    scores = np.sum(tfidf_matrix.toarray(), axis=0)
   
    keyword_scores = list(zip(feature_names, scores))
    keyword_scores.sort(key=lambda x: x[1], reverse=True)
   
    return keyword_scores[:10]

html_templates = {
    'last_scrape_button': '''
    <button onclick="showLastScrape()">Show Last Scrape</button>
    <div id="lastScrapeInfo" style="display:none;">
        <p>Last Scrape: <span id="lastScrapeTimestamp"></span></p>
        <p>Status: <span id="lastScrapeStatus"></span></p>
        <p>URL: <span id="lastScrapeUrl"></span></p>
    </div>
    ''',
    'site_directory': '''
    <h3>Site Directory</h3>
    <ul id="siteDirectory"></ul>
    ''',
    'keywords': '''
    <h3>Keywords</h3>
    <ul id="keywordsList"></ul>
    ''',
    'ml_insights': '''
    <h3>Machine Learning Insights</h3>
    <div id="directoryStructure"></div>
    <div id="keywordStrategy"></div>
    '''
}

def generate_ui_html():
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Scraper Dashboard</title>
        <script>
        function showLastScrape() {{
            fetch('/api/last_scrape')
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('lastScrapeTimestamp').textContent = data.timestamp;
                    document.getElementById('lastScrapeStatus').textContent = data.success ? 'Success' : 'Failed';
                    document.getElementById('lastScrapeUrl').textContent = data.url;
                    document.getElementById('lastScrapeInfo').style.display = 'block';
                }});
        }}
        function loadSiteDirectory() {{
            fetch('/api/site_directory')
                .then(response => response.json())
                .then(data => {{
                    const ul = document.getElementById('siteDirectory');
                    ul.innerHTML = '';
                    data.forEach(link => {{
                        const li = document.createElement('li');
                        li.textContent = link;
                        ul.appendChild(li);
                    }});
                }});
        }}
        function loadKeywords() {{
            fetch('/api/keywords')
                .then(response => response.json())
                .then(data => {{
                    const ul = document.getElementById('keywordsList');
                    ul.innerHTML = '';
                    data.forEach(keyword => {{
                        const li = document.createElement('li');
                        li.textContent = keyword;
                        ul.appendChild(li);
                    }});
                }});
        }}
        function loadMLInsights() {{
            fetch('/api/ml_insights')
                .then(response => response.json())
                .then(data => {{
                    const directoryStructure = document.getElementById('directoryStructure');
                    const keywordStrategy = document.getElementById('keywordStrategy');
                   
                    directoryStructure.innerHTML = '<h4>Directory Structure Clusters</h4>';
                    Object.entries(data.directory_clusters).forEach(([cluster, urls]) => {{
                        directoryStructure.innerHTML += `<p>Cluster ${{cluster}}: ${{urls.join(', ')}}</p>`;
                    }});
                   
                    keywordStrategy.innerHTML = '<h4>Optimized Keyword Strategy</h4>';
                    data.keyword_strategy.forEach(([keyword, score]) => {{
                        keywordStrategy.innerHTML += `<p>${{keyword}}: ${{score.toFixed(2)}}</p>`;
                    }});
                }});
        }}
        </script>
    </head>
    <body>
        <h1>Scraper Dashboard</h1>
        {html_templates['last_scrape_button']}
        {html_templates['site_directory']}
        {html_templates['keywords']}
        {html_templates['ml_insights']}
        <script>
        loadSiteDirectory();
        loadKeywords();
        loadMLInsights();
        </script>
    </body>
    </html>
    '''

def get_ml_insights(directory, keywords):
    directory_clusters = analyze_directory_structure(directory)
    keyword_strategy = optimize_keyword_strategy(keywords)
    return {
        'directory_clusters': directory_clusters,
        'keyword_strategy': keyword_strategy
    }
