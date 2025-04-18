
# 🧠 Karger Scientific Articles Scraper

## 📚 Project Summary

This Python project automates the extraction and analysis of metadata from scientific articles published in the journal *Karger*, focusing on articles published between **1965 and 1997**.
The goal is to collect structured information about each article for academic and bibliometric research.

## 🔧 Key Features

- Automated login via **OpenAthens** to access paywalled content
- Filters articles by type: **Research Articles only**
- Extracts detailed metadata from each article:
  - Title, DOI, Publication Date
  - Number and names of authors
  - Inferred gender and gender probability of first and last authors (via [Genderize API](https://genderize.io))
  - Author affiliations (first and last)
  - Number of figures and tables, including captions
  - Downloadable figure links (PPT format)
- Saves structured data into an Excel file (`output.xlsx`)
- Downloads images into local folders sorted by year and article title

## 🛠️ Technologies Used

- Python 3.8+
- Selenium (browser automation)
- Pandas (data processing)
- Requests & BeautifulSoup (web scraping)
- Genderize API (gender inference)
- Firefox + Geckodriver


> ⚠️ Note: The script uses [OpenAthens](https://my.openathens.net/) authentication.
> You will need to log in manually when the browser window appears.

## 📂 Repository Contents

| File | Description |
|------|-------------|
| `karger_code.py` | Main scraping script |
| `output.xlsx` | Excel file with structured article metadata |
| `README.md` | Project documentation |


## ⚠️ Challenges & Solutions

- **Dynamic Content**: Solved using `try-except` and `WebDriverWait` to handle asynchronous loads.
- **Element Overlap**: Script detects and closes obstructing UI overlays.
- **Partial/Missing Data**: Graceful handling for absent authors or affiliations.
- **Navigation Errors**: Retry logic implemented for broken or slow links.


---

This project demonstrates practical skills in data scraping, automation, and metadata analysis — suitable for research or data engineering portfolios.
