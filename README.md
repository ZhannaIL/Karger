
# Karger Scientific Articles Scraper
## Project Summary

This Python project automates the extraction and analysis of metadata from scientific articles published in the journal Karger, focusing on articles published between 1965 and 1997. The goal is to collect structured information about each article for academic or bibliometric research purposes.

## Key Features

Automates login via OpenAthens to access paywalled content.   
Filters articles by type:  
Research Articles only.  
Extracts metadata for each article:  
Title, DOI, Publication Date  
Number and names of authors  
Inferred gender and gender probability of first and last authors (via Genderize API)  
Author affiliations (first and last authors)   
Number of figures and tables, captions, and downloadable links  
Saves results in an Excel file (output.xlsx)  
Downloads images (figures) and saves them locally by year and article title  

## Technologies Used

Python  
Selenium – browser automation (using Firefox)  
Pandas – data structuring and export  
Requests & BeautifulSoup – HTTP requests and parsing  
Genderize API – for author gender prediction   
OpenAthens – authentication gateway to Karger  

⚠️ Challenges & Notes

Dynamic content and delayed page loads were handled using try-except and WebDriverWait.  
Some article metadata (e.g., author affiliations) may be partially hidden under overlays — the script attempts to close them automatically.  
Manual login is required due to authentication via OpenAthens (no API access).  
