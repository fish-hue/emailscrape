import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import time

def extract_emails(content):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}(?<!\.png)(?<!\.jpg)\b'
    return set(re.findall(email_pattern, content))

# prompt user for website url
url = input("Enter website URL (including https://): ")

# retrieve website content
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    content = response.content.decode()
except requests.RequestException as e:
    print(f"Error fetching {url}: {e}")
    exit()

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(content, 'html.parser')

# Extract emails from the initial page
emails = extract_emails(content)

# Find all links on the page
links = [a.get('href') for a in soup.find_all('a', href=True) if not a['href'].endswith(('.jpg', '.png'))]

# Loop through each link to find more email addresses
for link in links:
    full_link = urljoin(url, link)  # Handle relative URLs
    try:
        response = requests.get(full_link)
        response.raise_for_status()
        link_content = response.content.decode()
        emails.update(extract_emails(link_content))
    except requests.RequestException as e:
        print(f"Error fetching {full_link}: {e}")
    
    time.sleep(1)  # Delay to be polite to the server

# Prompt user to either view or export email addresses
print(f"Found {len(emails)} unique email addresses.")
choice = input("Enter 'view' to see the list of email addresses, or 'export' to save the list to a file: ")

if choice.lower() == "view":
    for email in emails:
        print(email)
elif choice.lower() == "export":
    filename = input("Enter filename (including .txt extension): ")
    with open(filename, "w") as f:
        for email in emails:
            f.write(email + "\n")
    print(f"Email addresses saved to {filename}.")
else:
    print("Invalid choice.")
