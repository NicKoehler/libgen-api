"""

Basic testing script for libgen-api.
Runs through a number of searches using different parameters, outputs results to terminal.

Run -
python3 test.py

"""


from libgen_api.libgen_search import Libgen

title = "Pride and Prejudice"
author = "Agatha Christie"


# helper function to print first title if it exists.
def print_results(titles_array):
    print(titles_array[0] if len(titles_array) else "No results.")
    print("\n\n--- END OF OUTPUT ---\n\n")


# test title search
# should print a result for the book specified at the top of the file.
print("\n>>>\tSearching for title: " + title)

titles = Libgen.search_title(title)
print_results(titles)


# test author search
# should print a result for the author specified at the top of the file.
print("\n>>>\tSearching for author: " + author)

titles = Libgen.search_author(author)
print_results(titles)


# test title filtering
# should print a result for the book specified at the top of the file,
# conforming to the title_filters below.
title_filters = {"year": "2007", "extension": "epub"}
print(
    "\n>>>\tSearching for title: "
    + title
    + " with filters --- "
    + ", ".join([":".join(i) for i in title_filters.items()])
)

titles = Libgen.search_title(title, title_filters, exact_match=True)
print_results(titles)


# test author filtering
# should print a result for the author specified at the top of the file,
# conforming to the title_filters below.
author_filters = {"language": "German", "year": "2009"}
print(
    "\n>>>\tSearching for author: "
    + author
    + " with filters --- "
    + ", ".join([":".join(i) for i in author_filters.items()])
)

titles = Libgen.search_author(author, author_filters, exact_match=True)
print_results(titles)


# test exact filtering explicitly (using an Author search)
# should print no results as the filter exclude all results.
exact_filters = {
    "extension": "PDF"
}  # if exact_match = True, all results get filtered as "pdf" is always written lower case
print(
    "\n>>>\tSearching for author: "
    + author
    + " with filters --- "
    + ", ".join([":".join(i) for i in exact_filters.items()])
    + " & exact_match == True"
)

titles = Libgen.search_author(author, exact_filters, exact_match=True)
print_results(titles)


# test non-exact filtering (using an Author search)
# should print a result for the author specified at the top of the file,
# conforming to the title_filters below.
non_exact_filters = {
    "extension": "PDF"
}  # if exact_match = True, all results get filtered as "pdf" is always written lower case
print(
    "\n>>>\tSearching for author: "
    + author
    + " with filters --- "
    + ", ".join([":".join(i) for i in non_exact_filters.items()])
    + " & exact_match == FALSE"
)

titles = Libgen.search_author(author, non_exact_filters, exact_match=False)
print_results(titles)


# test partial filtering (using a Title)
# should print a result for the title specified at the top of the file,
# conforming to the non_exact_filter below, with non-exact matching.
partial_filters = {"extension": "p", "year": "200"}
print(
    "\n>>>\tSearching for title: "
    + title
    + " with filters --- "
    + ", ".join([":".join(i) for i in partial_filters.items()])
    + " & exact_match == False"
)

titles = Libgen.search_title(title, partial_filters, exact_match=False)
print_results(titles)


# test partial filtering (using a Title)
# should return nothing as the extension is not an exact match to an existing one (ie. "pdf")
exact_partial_filters = {"extension": "p"}
print(
    "\n>>>\tSearching for title: "
    + title
    + " with filters --- "
    + ", ".join([":".join(i) for i in exact_partial_filters.items()])
    + " & exact_match == True"
)

titles = Libgen.search_title(title, exact_partial_filters, exact_match=True)
print_results(titles)


# test resolving of mirror links
# should print a populated hash of source:download_link pairs
print("\n>>>\tSearching for title: " + title + " and resolving download links")

# Author hard-coded so that it pairs with title (currently pride and prejudice)
titles = Libgen.search_author("Jane Austen")
item_to_download = titles[0]
download_links = item_to_download.get_download_links()
for source, link in download_links.items():
    print(f"{source}:\t{link[:30]}...\n")
