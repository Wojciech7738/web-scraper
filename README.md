# Web Scraper

## Description

This script is used to search for company names on dedicated websites and save the collected data in the format: "Company Name, NIP, CEO".

## Requirements

- Python 3.12
- Additional libraries listed in the `requirements.txt` file
- Google Chrome

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Wojciech7738/web-scraper.git
   cd web-scraper

2. **Install dependencies**:

    Ensure you have Python 3.12 installed. Then, install the required libraries:
    
    ```bash
    pip install -r requirements.txt

## Usage

The script can be run using the following commands:

- **Default processing from the article and from dedicated websites**:
    ```bash
    python main.py Default Article
- **Processing using dane.biznes.gov.pl API and text file:**:
    ```bash
    python main.py API File
## Configuration
Paths to input and output files, as well as other configuration settings, are defined in the `Config` class. You can customize these settings by editing the corresponding values in the code.
