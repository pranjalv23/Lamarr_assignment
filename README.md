# Automated Web Scraping for Legal Judgments

This project automates web scraping to extract legal judgments from the SCC Online website, focusing on judgments from Indian courts. The extracted data includes details such as court name, case name, bench name, document ID, and citations. The script navigates through nested lists of years, months, and days to extract data for each judgment.

## Information to scrape:

- Court name (Defaults to Supreme Court)
- Case name
- Bench name (Judge names)
- doc id
- citations (`a` tags that point to other cases or statutes like IPC, CRPC, etc )
  
## Prerequisites

- Python 3.x
- Chrome browser
- ChromeDriver (installed automatically using ChromeDriverManager)
- Selenium
- BeautifulSoup
- Pandas
