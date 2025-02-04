<div align="center">

![logo](logo.png)

A fork of the original [libgen-api](https://github.com/nickoehler/libgen-api)

![GitHub](https://img.shields.io/github/license/nickoehler/libgen-api?style=plastic)

![GitHub Repo stars](https://img.shields.io/github/stars/nickoehler/libgen-api?style=plastic)

</div>

Search Library Genesis programmatically using a simple Python library.

Allows you to search Library Genesis by title or author, filter results, and resolve download links.

## Contents

- [Getting Started](#getting-started)
- [Basic Searching](#basic-searching)
- [Filtered Searching](#filtered-searching)
  - [Filtered Title Searching](#filtered-title-searching)
  - [Filtered Author Searching](#filtered-author-searching)
  - [Non-exact Filtered Searching](#non-exact-filtered-searching)
  - [Filter Fields](#filter-fields)
- [Resolving mirror links](#resolving-mirror-links)
- [Download books](#Download-books)
- [More Examples](#more-examples)
- [Further Information](#further-information)
- [Testing](#testing)
- [Contributors](#contributors)

---

Please ⭐ if you find this useful!

---

## Getting Started

Install the package -

```
pip install git+https://github.com/nickoehler/libgen-api
```

Perform a basic search -

```python
# search_title()

from libgen_api import Libgen

results = Libgen.search_title("Pride and Prejudice")
print(results)
```

Check out the [results layout](#results-layout) to see how the results data is formatted.

## Basic Searching:

**_NOTE_**: All queries must be at least 3 characters long. This is to avoid any errors on the LibGen end (different mirrors have different requirements, but a minimum of 3 characters is the official limit).

Search by title or author:

### Title:

```python
from libgen_api import Libgen

results = Libgen.search_title("Pride and Prejudice")
print(results)
```

### Author:

```python
from libgen_api import Libgen

results = Libgen.search_author("Jane Austen")
print(results)
```

## Filtered Searching

Skip to the [Examples](#filtered-title-searching)

- You can define a set of filters, and then use them to filter the search results that get returned.
- By default, filtering will remove results that do not match the filters exactly (case-sensitive) -
  - This can be adjusted by setting `exact_match=False` when calling one of the filter methods, which allows for case-insensitive and substring filtering.

### Filtered Title Searching

```python
from libgen_api import Libgen

title_filters = {"year": "2007", "extension": "epub"}
titles = Libgen.search_title("Pride and Prejudice", title_filters, exact_match=True)
print(titles)
```

### Filtered Author Searching

```python
from libgen_api import Libgen

author_filters = {"language": "German", "year": "2009"}
titles = Libgen.search_author("Agatha Christie", author_filters, exact_match=True)
print(titles)
```

### Non-exact Filtered Searching

```python
from libgen_api import Libgen

partial_filters = {"year": "200"}
titles = Libgen.search_author("Agatha Christie", partial_filters, exact_match=False)
print(titles)
```

### Filter Fields

You can filter against this list of fields:

```
id
author
titl
publisher
year
pages
language
size
extension
```

## Resolving mirror links

The mirror links returned in the results (ie. by running search_author() or search_title()) are not direct download links and do not resolve to a downloadable URL without further parsing.

You can call `get_download_links()` on a book object to get direct download links.

The first element of `mirrors` field is used by `get_download_links()` as the results generally contain the most useful URLs.

returns a dictionary of all the download links of the first mirror (each mirror link has up to 4 download links):

```python
from libgen_api import Libgen

results = Libgen.search_author("Jane Austen")
item_to_download = results[0]
download_links = item_to_download.get_download_links()
print(download_links)
```

Example output:

```json
{
  "GET": "http://example.com/file.epub",
  "Cloudflare": "http://example.com/file.epub",
  "IPFS.io": "http://example.com/file.epub",
  "Infura": "http://example.com/file.epub"
}
```

## Download books

If you just want the book file (ie. epub, mobi, pdf, etc.), you can call `download()` and then download the file directly.

This method will return the file as bytes from Cloudflare link.

```python
from libgen_api import Libgen

results = Libgen.search_author("Jane Austen")
book = results[0]
with open(f"{book.title}.{book.extension}", "wb") as f:
    f.write(book.download())
```

## More Examples

See the [testing file](test/manualtesting.py) for more examples.

## Results Layout

Results are returned as a list of Book objects with the following attributes:

```
id: str,
author: str,
title: str,
publisher: str,
year: str,
pages: str,
language: str,
size: str,
extension: str,
mirrors: list[str],
```

## Further information

- If there are no results, the library will return an empty array.
- All fields are strings.
- If a value is not present, the field will contain an empty string.
- Some listings will have page count listed in the form of "count[secondary-count]" as this is how they appear on Library Genesis.
- Only the first page of results (max. 100) will be returned.

## Testing

libgen-api uses Pytest to run unit tests.

To run the tests -

- ## Clone this repo -
  ```
  git clone https://github.com/nickoehler/libgen-api.git && cd libgen-api
  ```
- ## Install dependencies with -
  ```
  pip install .
  ```
- ## Run tests with -
  ```
  pytest
  ```

## Contributors

A massive thank you to those that have contributed to this project!

Please don't hesitate to raise an issue, or fork this project and improve on it.

Thanks to the following contributors -

- [harrison broadbent](https://github.com/harrison-broadbent)
- [calmoo](https://github.com/calmoo)
