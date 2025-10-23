#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
from bs4 import BeautifulSoup
from collections import defaultdict
import re

def format_authors(raw_authors):
    author_list = re.split(r'\s+(?:and|,|;)\s+', raw_authors.strip())

    formatted = []
    for author in author_list:
        if not author.strip():
            continue
        parts = author.strip().split()
        if len(parts) == 0:
            continue
        last = parts[-1].rstrip(",.")
        initials = "".join(p[0].upper() + "." for p in parts[:-1] if p)
        formatted.append(f"{last}, {initials}")
    return "; ".join(formatted)

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

soup = BeautifulSoup("<html><head><title>Publications</title></head><body></body></html>", "html.parser")

# === 🎨 Add CSS ===
style_tag = soup.new_tag("style")
style_tag.string = """
body {
    font-family: Arial, sans-serif;
}
.year-group {
    margin-bottom: 40px;
}
.publication {
    background-color: #add8e6;
    border: 1px solid #000080;
    padding: 10px;
    margin: 10px 0;
}
.publication-title {
    font-weight: bold;
    color: blue;
    font-size: 1.1em;
}
.back-to-top {
    margin-bottom: 10px;
}
"""
soup.head.append(style_tag)

pub_head = soup.new_tag("div", id="pubHead")
page_top_anchor = soup.new_tag("a", attrs={"name": "page-top"})
pub_head.append(page_top_anchor)

font_outer = soup.new_tag("font", size="2")
bold_title = soup.new_tag("b")
bold_title.string = "Shea Group Publications"
font_outer.append(bold_title)
font_outer.append(" [ ")

font_inner = soup.new_tag("font", size="2")
group_home = soup.new_tag("a", href="index.html")
group_home.string = "Group Home"
font_inner.append(group_home)
font_inner.append(" / ")

years_sorted = sorted(
    [y for y in grouped.keys() if isinstance(y, int)], reverse=True
) + [y for y in grouped.keys() if not isinstance(y, int)]

for i, year in enumerate(years_sorted):
    year_link = soup.new_tag("a", href=f"#pub{year}")
    year_link.string = str(year)
    font_inner.append(year_link)
    if i < len(years_sorted) - 1:
        font_inner.append(" / ")

font_outer.append(font_inner)
font_outer.append(" ]")
pub_head.append(font_outer)
soup.body.append(pub_head)

container = soup.new_tag("div", id="publications-container")
soup.body.append(container)


for year in years_sorted:
    year_div = soup.new_tag("div", **{"class": "year-group"})

    year_anchor = soup.new_tag("a", attrs={"name": f"pub{year}"})
    year_div.append(year_anchor)

    h2 = soup.new_tag("h2")
    h2.string = str(year)
    year_div.append(h2)

    form = soup.new_tag("form", **{"class": "back-to-top"})
    input_button = soup.new_tag("input", type="BUTTON", value="Back to top of page")
    input_button["onclick"] = "window.location.href='#page-top'"
    form.append(input_button)
    year_div.append(form)

    for pub in grouped[year]:
        pub_div = soup.new_tag("div", **{"class": "publication"})

        
        title = soup.new_tag("div", **{"class": "publication-title"})
        title.string = pub.get("title", "No Title")
        pub_div.append(title)

        
        authors = soup.new_tag("p")
        raw_authors = pub.get("authors", "Unknown")
        formatted_authors = format_authors(raw_authors)
        authors.string = formatted_authors
        pub_div.append(authors)

        
        journal = soup.new_tag("p")
        journal_em = soup.new_tag("em")
        journal_em.string = pub.get("source") or pub.get("journal", "Unknown")
        journal.append(journal_em)
        pub_div.append(journal)

        
        year_p = soup.new_tag("p")
        year_p.string = f"Year: {pub.get('year', 'Unknown')}"
        pub_div.append(year_p)

        
        if pub.get("doi"):
            doi_p = soup.new_tag("p")
            doi_p.string = "DOI: "
            doi_link = soup.new_tag("a", href=f"https://doi.org/{pub['doi']}", target="_blank")
            doi_link.string = f"https://doi.org/{pub['doi']}"
            doi_p.append(doi_link)
            pub_div.append(doi_p)

        year_div.append(pub_div)

    container.append(year_div)


with open("updated_publications.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("✅ Styled HTML with formatted authors generated!")

