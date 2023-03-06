import requests
import re

# prompt user for website url
url = input("Enter website URL (including https://): ")

# retrieve website content
response = requests.get(url)
content = response.content.decode()

# use regular expression to extract email addresses from website content
email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
emails = set(re.findall(email_pattern, content))

# loop through all links on website to find more email addresses
link_pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"'
links = re.findall(link_pattern, content)

for link in links:
    if link.startswith("/"):
        link = url + link
    elif not link.startswith("http"):
        continue

    response = requests.get(link)
    content = response.content.decode()
    emails.update(set(re.findall(email_pattern, content)))

# prompt user to either view or export email addresses
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
