from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_website(website):
    
    chrome_driver_path = "./chromedriver"
    options = webdriver.ChromeOptions()
    # Set headless mode for faster loading (removes the need to render visuals)
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        # Only wait as long as needed to load specific content
        driver.get(website)
        print("Page loading...")

        # Wait for specific element in body to load (like main content div)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        html = driver.page_source
        print("Page loaded.")
        
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return "no body extracted"
    # Target specific div by ID or class if provided
    # target_div = soup.find("div", class_="w3-col", id="main")

    # return str(target_div) if target_div else "no data extracted"

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "lxml")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]