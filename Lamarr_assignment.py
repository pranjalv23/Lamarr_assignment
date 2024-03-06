import csv
import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def add_entry(court_name, case_name, bench_name, doc_id, citations):
    # Save the information to CSV
    with open("data/judgments.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([court_name, case_name, bench_name, doc_id, citations])


service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()

# Suppress logging messages from WebDriver
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=service, options=options)

main_url = "https://www.scconline.com/"
driver.get(main_url)

wait = WebDriverWait(driver, 50)

try:
    notif_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[6]/div/div/div[2]/button[1]")
        )
    )
    notif_link.click()
    print("Push notification allowing")
except Exception as e:
    print(e)
    print("Push notification not allowing or doesn't appear")

try:
    notif_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/button",
            )
        )
    )
    notif_link.click()
    print("Pop-up closing")
except Exception as e:
    print(e)
    print("Pop-up not closing or doesn't appear")

try:
    notif_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[6]/div/div/div[2]/button[2]")
        )
    )
    notif_link.click()
except Exception as e:
    print(e)

os.makedirs("data/", exist_ok=True)

try:
    wait.until(
        EC.presence_of_element_located(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close"))
        )
    ).click()
    print("Accepted cookies")
except Exception as e:
    print("No cookie button!")

try:
    # Find and click the "LOGIN" link
    login_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a#login-link-navbar.menu__link")
        )
    )
    login_link.click()
except Exception as e:
    print(e)

# Handle the popup (replace with your login logic)
username_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "loginid"))
)
print("Logging")
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "pass"))
)
login_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "big-btn"))
)

username_input.send_keys(os.environ["username"])
password_input.send_keys(os.environ["password"])
login_button.click()
print("Login button clicking")

time.sleep(15)

try:
    continue_ask_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[2]/div/div/div[1]/div[5]/div/div/div/section/div[2]/div[2]/button[1]",
            )
        )
    )
    continue_ask_link.click()
    print("Allowing to continue in that account")
except Exception as e:
    print(e)
    print("Not allowing to log in the same account")

try:
    e = driver.find_element(By.CLASS_NAME, "button.button-red.positive")
    e.click()
    print("Accepted login")
except Exception as e:
    print("No login popup button!")

browse_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "/html/body/form/section/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/div",
        )
    )
)
driver.execute_script(browse_link.get_attribute("onclick"))
print("Clicking on Browse judgments by Court/Tribunals")
# browse_link.click()

india_link = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "/html/body/form/div[13]/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]/ul/li/ul/li[1]/span",
        )
    )
)
india_link.click()
print("Diminishing India groups")

driver.implicitly_wait(50)

india_link = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "/html/body/form/div[13]/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]/ul/li/ul/li[1]/span/a",
        )
    )
)
india_link.click()
print("Expanding India groups")

sc_link = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "/html/body/form/div[13]/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]/ul/li/ul/li[1]/ul/li[1]/span",
        )
    )
)
sc_link.click()
print("Expanding Supreme Court group")

driver.implicitly_wait(50)

base_xpath = "/html/body/form/div[13]/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]/ul/li/ul/li[1]/ul/li[1]"


def navigate_nested_lists(driver, base_xpath):
    # print(0)
    for year_index in range(1, 9):
        current_xpath = f"{base_xpath}/ul/li[{year_index}]"
        print(current_xpath)
        try:
            # print(1)
            current_link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, current_xpath))
            )
            current_link.click()
            print(f"Opening year range {year_index}")
            navigate_year(driver, current_xpath)
            print("Going to navigate this year")
            if "dynatree-lastsib" in current_link.get_attribute("class"):
                print("Last section found")
                break

        except Exception as e:
            print(f"Exception: {e}")
            print("Backtracking section...")
            backtrack_xpath = f"{base_xpath}/ul/li[{year_index+1}]"
            print(backtrack_xpath)
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, backtrack_xpath))
            )


def navigate_year(driver, base_xpath):
    # print(3)
    for depth in range(1, 5):
        print("year")
        current_xpath = f"{base_xpath}/ul/li[{depth}]"
        try:
            # Wait for the element to be clickable
            current_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, current_xpath))
            )
            current_link.click()
            print(f"Opening year {depth} ")
            navigate_month(driver, current_xpath)
            if "dynatree-lastsib" in current_link.get_attribute("class"):
                print("Last year found")
                break

        except Exception as e:
            print("Backtracking year")


def navigate_month(driver, base_xpath):
    # print(5)
    for depth in range(0, 12):
        print("month")
        try:
            if depth == 0:
                current_xpath = f"{base_xpath}/ul/li"
            else:
                current_xpath = f"{base_xpath}/ul/li[{depth}]"
            # Wait for the element to be clickable
            current_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, current_xpath))
            )
            current_link.click()
            print("Navigating day")
            navigate_day(driver, current_xpath)
            if "dynatree-lastsib" in current_link.get_attribute("class"):
                print("Last month found")
                break

        except Exception as e:
            print("Backtracking month")


def read_data(driver):
    # Extract the date, month, and year dynamically
    try:
        date_element = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//a[@class='BredCrumbNode breadcrumblist']/span[@class='fortootipBreadCrumb']",
                )
            )
        )
        year_text = date_element[3].text.strip()
        print("Year", year_text)

        month_text = date_element[4].text.strip()
        print("Month:", month_text)

        index_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[@class='BredCrumbNode breadcrumblist']/span[@class='fortootipBreadCrumbSmall']",
                )
            )
        )
        index_text = index_element.text.strip()
        print("Day", index_text)

        title_text = date_element[5].text.strip()
        print("Title", title_text)

    except Exception as e:
        print(f"Error extracting date, month, and year: {e}")

    div_xpath = "/html/body/form/div[13]/div[1]/div[2]/div[2]/div[2]/div[3]"
    print("Extracting inner text ")

    try:
        # Find the div element and extract inner text
        target_div = WebDriverWait(driver, 5000).until(
            EC.presence_of_element_located((By.XPATH, div_xpath))
        )
        soup = BeautifulSoup(target_div.get_attribute("outerHTML"), "html.parser")

        inner_text = soup.get_text()

        os.makedirs(
            "data/{}-{}-{}/".format(year_text, month_text, index_text), exist_ok=True
        )
        if inner_text != "":
            with open(
                "data/{}-{}-{}/{}.csv".format(
                    year_text, month_text, index_text, title_text
                ),
                "w+",
                encoding="utf-8",
            ) as file:
                writer = csv.writer(file)

                judge_name = driver.find_element(By.ID, "FJUD01").text
                print(judge_name)

                scc_id = driver.find_element(By.CLASS_NAME, "SectionheadText").text
                print(scc_id)

                case_name = [
                    e.text for e in driver.find_elements(By.CLASS_NAME, "app")
                ]
                print(case_name)

                case_name = " vs ".join(case_name)
                print(case_name)

                case_no = driver.find_element(By.CLASS_NAME, "caseno").text
                print(case_no)

                date = driver.find_element(By.CLASS_NAME, "date").text
                print(date)

                advocates = [
                    e.text for e in driver.find_elements(By.CLASS_NAME, "advo")
                ]
                print(advocates)

                citations = [
                    a.get_attribute("onclick")
                    for a in driver.find_elements(By.CLASS_NAME, "citalink")
                ]
                print(citations)

                # inserts data
                add_entry(judge_name, case_name, advocates, scc_id, citations)

                writer.writerow([case_name, case_no, date, advocates, citations, inner_text])
            print("Inner text written to csv")

    except Exception as e:
        print(f"Error extracting inner text: {e}")


def wait_for_preloader_to_disappear(driver):
    try:
        # Wait for the preloader element to become invisible
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.ID, "thirdPanelPreloader"))
        )
        print("Preloader disappeared.")
    except TimeoutException:
        print("Timed out waiting for preloader to disappear.")


def navigate_day(driver, base_xpath):
    for depth in range(1, 32):
        current_xpath = f"{base_xpath}/ul/li[{depth}]"
        try:
            # Wait for the element to be clickable
            current_link = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.XPATH, current_xpath))
            )
            current_link.click()

            ul_element = WebDriverWait(driver, 200).until(
                EC.presence_of_element_located((By.XPATH, f"{current_xpath}/ul"))
            )
            li_elements = ul_element.find_elements(By.XPATH, "./li")
            for li_element in li_elements:
                li_element.click()
                print("In")
                wait_for_preloader_to_disappear(driver)
                print("Out")
                read_data(driver)

            if "dynatree-lastsib" in current_link.get_attribute("class"):
                print("Last element found")
                break

        except Exception as e:
            print("Backtracking day")
            pass


# Call the function to navigate through nested lists starting from 'sc_link'
navigate_nested_lists(driver, base_xpath)  # Adjust max_depth as needed

# Close the browser window
driver.quit()
