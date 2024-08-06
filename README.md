# LinkedIn Job Scraper for Microsoft, Google, and Amazon

## Project Overview

This project involves developing a Python script to scrape job postings from LinkedIn for Microsoft, Google, and Amazon. The script extracts key job details and stores the data in JSON and CSV formats.

## Features

- Scrapes job postings from LinkedIn for Microsoft, Google, and Amazon.
- Extracts key details such as:
  - Company Name
  - LinkedIn Job ID
  - Job Title
  - Location
  - Posted On
  - Posted Date
  - Work Mode
  - Employment Type
  - Skills
- Handles missing data by assigning `null` values.
- Stores the collected data in JSON and CSV formats.
- Includes error handling and respects LinkedIn's rate limits and terms of service.

## Requirements

- Python 3.x
- `selenium`
- `beautifulsoup4`
- `pandas`
- WebDriver for your browser (e.g., ChromeDriver)
