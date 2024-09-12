# BBR Django Project

# BBR E-commerce Project

## Overview
A robust Django-based e-commerce platform with advanced web scraping capabilities, designed for efficient product management and seamless user experience.

## Key Features
- Product management with categories, years, makes, and models
- Web scraping using Scrapy and Selenium for automated data collection
- FTP data import for bulk product updates
- Elasticsearch-powered product search and filtering
- Shopping cart with session management
- Order processing and checkout system
- User authentication and profile management
- Flash sales functionality
- Admin interface for comprehensive site management

## Detailed Component Breakdown

### Products App
- Models: Product, Category, Year, Make, Model, Review, FlashSale
- Views: product listing, detail, search, and filtering
- Admin: Custom admin actions for product management
- Management Commands: populate_makes, populate_years, scrape_product

### Scraping App
- Spiders: EccppSpider for scraping product data
- Models: ScrapedData for storing raw scraped information
- Utils: Data processing and comparison functions
- Views: Review and approve scraped data changes

### Orders App
- Models: Order, OrderItem, ShippingOption
- Views: Checkout process, order confirmation, order history
- Admin: Order management interface

### Users App
- Views: User registration, login, profile management
- Models: UserProfile for extended user information

### Cart App
- Cart: Session-based shopping cart implementation
- Views: Add to cart, remove from cart, view cart

### Core App
- Base templates and static files
- Home page view

## Setup and Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix or MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure the database in `ecommerce_project/settings.py`
6. Run migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Start the development server: `python manage.py runserver`

## Usage
- Admin interface: Navigate to `/admin/` and log in with superuser credentials
- Product list: Browse products at `/products/`
- User registration: Create an account at `/users/register/`
- Shopping: Add products to cart and proceed to checkout

## Management Commands
- Populate car makes: `python manage.py populate_makes`
- Populate years: `python manage.py populate_years`
- Run product scraper: `python manage.py scrape_product`

## Web Scraping
The project uses Scrapy and Selenium for web scraping. The `EccppSpider` in `eccpp_crawler/spiders/eccpp_spider.py` is responsible for crawling product data. Scraped data is then processed and can be reviewed before being added to the product catalog.

## FTP Import
The `ftp_import.py` module provides functionality to import product data from FTP servers, supporting various file formats including CSV, XML, and JSON.

## Search Functionality
Elasticsearch is integrated for advanced product search capabilities. The `search.py` module in the products app handles search queries and filtering.

## Contributing
1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

## Testing
Run the test suite with: `python manage.py test`

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Documentation:

1. Django models:
   - `Product`: Represents a product with fields like name, price, and SKU.
   - `ProductDetail`: Stores additional details for a product, such as description and image URL.
   - `Make`: Represents a car, truck, or SUV make (e.g., Toyota, Ford).
   - `Model`: Represents a specific model of a make (e.g., Camry, F-150).
   - `Year`: Represents a year associated with a product.

2. Django management commands:
   - `scrape_product.py`: Scrapes product information from eccppautoparts.com using Scrapy and Selenium. It handles user login, starts the Scrapy spider, and imports the scraped data into the database.
   - `populate_makes.py`: Populates the database with a predefined list of car, truck, and SUV makes in the USA.

3. Scrapy spider:
   - `ProductSpider`: Defines the spider logic for scraping product information from eccppautoparts.com. It extracts details like name, price, description, and image URL.

The codebase aims to automate the process of scraping and importing product information from eccppautoparts.com into a Django database. It leverages Scrapy for web scraping, Selenium for handling user login, and Django's management commands for executing the scraping and data population tasks.

Enhancements and updates have been made to improve error handling, logging, and code organization. The codebase follows best practices and coding conventions to ensure readability and maintainability.

Please review the codebase and provide any further enhancements, optimizations, or suggestions to improve its functionality and performance. Let me know if you have any specific questions or areas you'd like me to focus on.

Project Structure and File Dependencies

1. eccpp_crawler/eccpp_crawler/spiders/eccpp_spider.py
Uses: Web scraping for product data from eccppautoparts.com
Dependencies: scrapy
Depended on by: products/management/commands/scrape_product.py for running the spider

2. products/ftp_import.py
Uses: Importing product data from FTP servers
Dependencies: ftplib, csv, xml.etree.ElementTree, json
Depended on by: Likely used by a management command or view for data import

3. products/views.py
Uses: Handling product-related HTTP requests
Dependencies: products/models.py, products/forms.py
Depended on by: products/urls.py for URL routing

4. products/search.py
Uses: Product search functionality
Dependencies: elasticsearch_dsl
Depended on by: products/views.py for search operations

5. products/admin.py
Uses: Customizing the admin interface for product management
Dependencies: products/models.py
Depended on by: Django admin site

6. products/models.py
Uses: Defining database schema for products
Dependencies: django.db.models
Depended on by: products/views.py, products/admin.py, orders/models.py

7. cart/cart.py
Uses: Shopping cart functionality
Dependencies: products/models.py
Depended on by: cart/views.py, orders/views.py

8. cart/views.py
Uses: Handling cart-related HTTP requests
Dependencies: cart/cart.py, products/models.py
Depended on by: cart/urls.py for URL routing

9. orders/views.py
Uses: Handling order-related HTTP requests
Dependencies: orders/models.py, cart/cart.py
Depended on by: orders/urls.py for URL routing

10. orders/models.py
Uses: Defining database schema for orders
Dependencies: django.db.models, products/models.py
Depended on by: orders/views.py, orders/admin.py

11. users/views.py
Uses: Handling user-related HTTP requests
Dependencies: django.contrib.auth.models
Depended on by: users/urls.py for URL routing

12. ecommerce_project/settings.py
Uses: Project-wide Django settings
Dependencies: Various Django and third-party packages
Depended on by: All Django apps in the project

13. ecommerce_project/urls.py
Uses: Project-wide URL routing
Dependencies: Various app-level urls.py files
Depended on by: Django's URL dispatcher

14. scraping/models.py
Uses: Defining database schema for scraped data
Dependencies: django.db.models
Depended on by: scraping/views.py, scraping/admin.py

15. scraping/views.py
Uses: Handling scraping-related HTTP requests
Dependencies: scraping/models.py, scraping/utils.py
Depended on by: scraping/urls.py for URL routing

16. scraping/utils.py
Uses: Utility functions for scraping operations
Dependencies: Various Python libraries
Depended on by: scraping/views.py, possibly management commands

17. products/management/commands/populate_makes.py
Uses: Populating the database with car makes
Dependencies: products/models.py
Depended on by: Used as a Django management command

18. products/management/commands/populate_years.py
Uses: Populating the database with years
Dependencies: products/models.py
Depended on by: Used as a Django management command

19. products/management/commands/scrape_product.py
Uses: Running the product scraper
Dependencies: eccpp_crawler/eccpp_crawler/spiders/eccpp_spider.py
Depended on by: Used as a Django management command

20. core/views.py
Uses: Handling core app HTTP requests
Dependencies: None visible in the provided code
Depended on by: core/urls.py for URL routing

21. core/apps.py
Uses: Configuring the core Django app
Dependencies: django.apps
Depended on by: INSTALLED_APPS in ecommerce_project/settings.py

eccpp_crawler/eccpp_crawler/spiders/eccpp_spider.py:

parse: Extracts links and product information
parse_product: Extracts specific product details
products/ftp_import.py:

connect: Establishes FTP connection
disconnect: Closes FTP connection
list_files: Retrieves file list from FTP server
download_file: Transfers file from FTP server
validate_file: Checks file integrity
process_file: Handles imported file data
import_from_ftp: Orchestrates FTP import process
products/views.py:

update_stock: Modifies product inventory
upload_csv: Imports product data from CSV
products/search.py:

search_products: Performs product search operations
products/admin.py:

mark_as_featured: Highlights selected products
bulk_update_price: Changes prices for multiple products
export_as_csv: Generates CSV export of products
import_csv: Imports product data from CSV
cart/cart.py:

add: Inserts product into cart
save: Persists cart data
remove: Deletes product from cart
clear: Empties the entire cart
orders/views.py:

checkout: Processes order completion
generate_order_number: Creates unique order identifier
process_payment: Handles payment transactions
finalize_order: Completes order processing
apply_coupon: Applies discount to order
users/views.py:

profile_view: Displays user profile information
order_history: Shows user's past orders
scraping/views.py:

review_changes: Presents scraped data changes for approval
scraping/utils.py:

calculate_difference: Compares old and new scraped data
products/management/commands/populate_makes.py:

handle: Executes make population process
products/management/commands/populate_years.py:

handle: Executes year population process
products/management/commands/scrape_product.py:

handle: Initiates product scraping process
This list provides an overview of key actions performed within each file of the e-commerce system.

eccpp_crawler/eccpp_crawler/spiders/eccpp_spider.py:

scrapy: Web scraping framework
urllib.parse: URL parsing and manipulation
products/ftp_import.py:

ftplib: FTP protocol client
concurrent.futures: Asynchronous execution
csv: CSV file reading and writing
xml.etree.ElementTree: XML parsing
json: JSON data handling
logging: Logging functionality
products/views.py:

django.shortcuts: Simplified HTTP responses
django.contrib.auth.decorators: Authentication checks
django.core.files.storage: File storage operations
django.http: HTTP-specific functions
django.views.decorators.csrf: CSRF protection
pandas: Data manipulation and analysis
cv2: Image processing
products/search.py:

elasticsearch_dsl: Elasticsearch query DSL
products/admin.py:

django.contrib.admin: Admin interface customization
django.urls: URL handling
django.db.models: Database operations
django.shortcuts: Simplified HTTP responses
django.http: HTTP-specific functions
csv: CSV file handling
products/models.py:

django.db.models: Database modeling
django.core.exceptions: Django-specific exceptions
django.utils: Django utility functions
cart/cart.py:

decimal: Precise decimal arithmetic
django.conf: Django settings access
orders/views.py:

django.shortcuts: Simplified HTTP responses
django.contrib.auth.decorators: Authentication checks
uuid: Unique identifier generation
users/views.py:

django.shortcuts: Simplified HTTP responses
django.contrib.auth.decorators: Authentication checks
django.contrib: Django's built-in features
scraping/views.py:

django.shortcuts: Simplified HTTP responses
django.http: HTTP-specific functions
scraping/utils.py:

difflib: Sequence comparison
products/management/commands/populate_makes.py:

django.core.management.base: Custom management commands
products/management/commands/populate_years.py:

django.core.management.base: Custom management commands
django.utils: Django utility functions
products/management/commands/scrape_product.py:

django.core.management.base: Custom management commands
scrapy.crawler: Scrapy crawler process
scrapy.utils.project: Scrapy project utilities
selenium: Web browser automation
time: Time-related functions