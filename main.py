import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

# Set up WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome for efficiency
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service('ChromeDriver/chromedriver.exe')  # Update path to your chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# List of URLs to scrape
urls = [
    "https://www.linkedin.com/jobs/search?location=India&geoId=102713980&f_C=1035&position=1&pageNum=0",
    "https://www.linkedin.com/jobs/search?keywords=&location=India&geoId=102713980&f_C=1441",
    "https://www.linkedin.com/jobs/search?keywords=&location=India&geoId=102713980&f_TPR=r86400&f_C=1586&position=1&pageNum=0"
]

job_data = []

def get_job_details(job_url):
    driver.get(job_url)
    time.sleep(3)  # Allow time for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        company_name = soup.find('a', {'class': 'topcard__org-name-link topcard__flavor--black-link'}).text.strip()
    except AttributeError:
        company_name = 'null'

    try:
        job_title = soup.find('h1', {'class': 'topcard__title'}).text.strip()
    except AttributeError:
        job_title = 'null'

    try:
        location = soup.find('span', {'class': 'topcard__flavor topcard__flavor--bullet'}).text.strip()
    except AttributeError:
        location = 'null'

    try:
        posted_on = soup.find('span', {'class': 'posted-time-ago__text topcard__flavor--metadata'}).text.strip()
    except AttributeError:
        posted_on = 'null'

    try:
        employment_type = soup.find('span', {'class': 'topcard__flavor--metadata'}).text.strip()
    except AttributeError:
        employment_type = 'null'

    try:
        work_mode = soup.find('span', {'class': 'topcard__flavor--metadata'}).text.strip()
    except AttributeError:
        work_mode = 'null'

    try:
        skills_section = soup.find('div', {'class': 'description__skills-section'})
        skills = [skill.text.strip() for skill in skills_section.find_all('span')] if skills_section else 'null'
    except AttributeError:
        skills = 'null'

    job_id = re.findall(r'/(\d+)', job_url)[0] if re.findall(r'/(\d+)', job_url) else 'null'
    posted_date = calculate_posted_date(posted_on)

    return {
        "company": company_name,
        "job_title": job_title,
        "linkedin_job_id": job_id,
        "location": location,
        "posted_on": posted_on,
        "posted_date": posted_date,
        "work_mode": work_mode,
        "employment_type": employment_type,
        "skills": skills
    }

def calculate_posted_date(posted_on):
    if 'today' in posted_on.lower():
        return time.strftime("%d-%m-%Y")
    elif 'yesterday' in posted_on.lower():
        return (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime("%d-%m-%Y")
    else:
        try:
            days_ago = int(re.search(r'\d+', posted_on).group())
            return (pd.Timestamp.now() - pd.Timedelta(days=days_ago)).strftime("%d-%m-%Y")
        except:
            return 'null'

for url in urls:
    driver.get(url)
    time.sleep(3)  # Allow time for the page to load

    # Scroll to the bottom to load more jobs
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for additional jobs to load

    job_links = driver.find_elements(By.CSS_SELECTOR, 'a.base-card__full-link')
    job_urls = [link.get_attribute('href') for link in job_links[:50]]  # Get the first 50 job links

    for job_url in job_urls:
        job_details = get_job_details(job_url)
        job_data.append(job_details)
        time.sleep(1)  # Respect LinkedIn's rate limits

driver.quit()

# Save the data to JSON and CSV
with open('jobs_data.json', 'w') as json_file:
    json.dump(job_data, json_file, indent=4)

df = pd.DataFrame(job_data)
df.to_csv('jobs_data.csv', index=False)

print("Data scraping and saving completed successfully.")
