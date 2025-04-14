import json
from scholarly import scholarly

# Replace with your advisor's Google Scholar ID
advisor_id = "VFHPSMEAAAAJ"

# Retrieve the author object from Google Scholar
author = scholarly.search_author_id(advisor_id)
author = scholarly.fill(author)

# Retrieve the list of publications
publications = author.get('publications', [])

pub_list = []
cnt = 0
for pub in publications:
    cnt += 1
    if cnt == 214:
        pass
    else:
        print(f"Processing Pub {cnt}")
        # Ensure publication details are filled in (if needed, call scholarly.fill(pub))
        pub_filled = scholarly.fill(pub)
        bib = pub_filled.get('bib', {})
        pub_entry = {
            "title": bib.get("title", "No title"),
            "authors": bib.get("author", "Unknown authors"),
            "journal": bib.get("venue", "Unknown journal"),
            "year": bib.get("pub_year", "Unknown"),
            "doi": pub_filled.get("pub_url", "#")
        }
        # Optionally include volume, pages, etc. if available:
        if 'volume' in bib:
            pub_entry["volume"] = bib["volume"]
        if 'pages' in bib:
            pub_entry["pages"] = bib["pages"]
            
        pub_list.append(pub_entry)

# Write the publications data to a JSON file
with open("publications.json", "w") as outfile:
    json.dump({"publications": pub_list}, outfile, indent=2)

print("publications.json has been updated.")

