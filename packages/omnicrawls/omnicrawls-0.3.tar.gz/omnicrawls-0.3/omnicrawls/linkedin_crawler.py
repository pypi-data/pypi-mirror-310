import os
import time
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager

class LinkedInCrawler:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.cookies_file = "linkedin_cookies.pkl"

        # Set up WebDriver
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless=new")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-accelerated-2d-canvas")
        options.add_argument("--disable-gpu-compositing")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=1")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--ignore-certificate-errors")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def extract(self, base_url, data_types=["all"]):
        # Initialize data containers
        profile_data = {}
        experience_data = []
        education_data = []
        posts_content = []

        # Step 1: Login to LinkedIn
        self.driver.get("https://www.linkedin.com/login")
        if os.path.exists(self.cookies_file):
            with open(self.cookies_file, "rb") as file:
                cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            print("Logged in using saved cookies.")
        else:
            email = os.getenv("EMAIL")
            password = os.getenv("PASSWORD")
            self.driver.find_element(By.ID, "username").send_keys(email)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(3)
            cookies = self.driver.get_cookies()
            with open(self.cookies_file, "wb") as file:
                pickle.dump(cookies, file)
            print("Logged in using email and password, cookies saved.")

        # Extract data based on user-selected data types
        extracted_data = {}

        # Step 2: Extract Profile Data
        if "Basic Profile" in data_types or "all" in data_types:
            self.driver.get(base_url)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            name = soup.find('div', {'class': 'keOsAaSEeURweqOUOfzyPONzRjMYxnQjpo'})
            if name:
                name = name.get_text().strip().split("\n")[0].strip()
                profile_data['name'] = name
            profile_data['url'] = base_url

            headline = soup.find('div', {'class': 'text-body-medium break-words'})
            if headline:
                profile_data['headline'] = headline.get_text().strip()
            extracted_data["Profile_data"] = profile_data

        # Step 3: Extract Experience Data
        if "Experience" in data_types or "all" in data_types:
            self.driver.get(f"{base_url}/details/experience/")
            time.sleep(2)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            target_li = soup.find_all('li', class_='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
            for company in target_li:
                spans = company.find_all('span', class_='visually-hidden')
                text_list = [span.get_text(strip=True) for span in spans if span.get_text(strip=True)]
                experience_data.append(text_list)

            extracted_data={"Experience" :experience_data}

        # Step 4: Extract Education Data
        if "Education" in data_types or "all" in data_types:
            self.driver.get(f"{base_url}/details/education/")
            time.sleep(2)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            all_edu = soup.find_all('li', class_='pvs-list__paged-list-item')
            for edu in all_edu:
                spans = edu.find_all('span', class_='visually-hidden')
                text_list = [span.get_text(strip=True) for span in spans if span.get_text(strip=True)]
                education_data.append(text_list)

            extracted_data={"Education":education_data}

        # Step 5: Extract Posts Content
        if "Posts" in data_types or "all" in data_types:
            self.driver.get(f"{base_url}/recent-activity/all/")
            self.driver.title
            time.sleep(4)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            posts = soup.find_all("div", class_="update-components-text relative update-components-update-v2__commentary")

            for post in posts:
                posts_content.append(post.get_text(strip=True))
            extracted_data={"Posts" : posts_content}

        return extracted_data



