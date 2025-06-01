#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
from bs4 import BeautifulSoup
from collections import defaultdict

with open("publications.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

publications = raw_data.get("publications", [])

grouped = defaultdict(list)
for pub in publications:
    try:
        year = int(pub.get("year", 0))
    except (ValueError, TypeError):
        year = "Unknown"
    grouped[year].append(pub)

with open("publication.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

container = soup.find(id="publications-container")
if not container:
    container = soup.new_tag("div", id="publications-container")
    soup.body.append(container)

container.clear()

years_sorted = sorted(
    [y for y in grouped.keys() if isinstance(y, int)], reverse=True
) + [y for y in grouped.keys() if not isinstance(y, int)]

for year in years_sorted:
    year_div = soup.new_tag("div", **{"class": "year-group"})

    h2 = soup.new_tag("h2")
    h2.string = str(year)
    year_div.append(h2)

    for pub in grouped[year]:
        pub_div = soup.new_tag("div", **{"class": "publication"})

        title = soup.new_tag("h3")
        title.string = pub.get("title", "No Title")
        pub_div.append(title)

        authors = soup.new_tag("p")
        authors.string = f"Authors: {pub.get('authors', 'Unknown')}"
        pub_div.append(authors)

        journal = soup.new_tag("p")
        journal.string = f"Journal: {pub.get('journal', 'Unknown')}"
        pub_div.append(journal)

        year_p = soup.new_tag("p")
        year_p.string = f"Year: {pub.get('year', 'Unknown')}"
        pub_div.append(year_p)

        if pub.get("doi"):
            doi = soup.new_tag("a", href=f"{pub['doi']}", **{"class": "doi", "target": "_blank"})
            doi.string = f"{pub['doi']}"
            pub_div.append(doi)

        year_div.append(pub_div)

    container.append(year_div)

with open("updated_publications.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("✅ HTML updated and grouped by year.")


# In[ ]:




