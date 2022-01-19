import pytest
from libgen_api.libgen_search import Libgen

title = "Pride and Prejudice"
author = "Agatha Christie"

class TestBasicSearching:
    def test_title_search(self):
        titles = Libgen.search_title(title)
        first_result = titles[0]

        assert title in first_result.title

    def test_author_search(self):
        titles = Libgen.search_author(author)
        first_result = titles[0]

        assert author in first_result.author

    def test_raise_error_on_invalid_search_type(self):
        with pytest.raises(Exception):
            Libgen.search_title(title, {"invalid": "filter"})

    def test_title_filtering(self):
        title_filters = {"year": "2007", "extension": "epub"}
        titles = Libgen.search_title(title, title_filters, exact_match=True)
        first_result = titles[0]

        assert (title in first_result.title) & fields_match(
            title_filters, first_result
        )

    def test_author_filtering(self):
        author_filters = {"language": "German", "year": "2009"}
        titles = Libgen.search_author(author, author_filters, exact_match=True)
        first_result = titles[0]

        assert (author in first_result.author) & fields_match(
            author_filters, first_result
        )

    # explicit test of exact filtering
    # should return no results as they will all get filtered out
    def test_exact_filtering(self):
        exact_filters = {"extension": "PDF"}
        # if exact_match = True, this will filter out all results as
        # "pdf" is always written lower case on Library Genesis
        titles = Libgen.search_author(author, exact_filters, exact_match=True)

        assert len(titles) == 0

    def test_non_exact_filtering(self):
        non_exact_filters = {"extension": "PDF"}
        titles = Libgen.search_author(author, non_exact_filters, exact_match=False)
        first_result = titles[0]

        assert (author in first_result.author) & fields_match(
            non_exact_filters, first_result, exact=False
        )

    def test_non_exact_partial_filtering(self):
        partial_filters = {"extension": "p", "year": "200"}
        titles = Libgen.search_title(title, partial_filters, exact_match=False)
        first_result = titles[0]

        assert (title in first_result.title) & fields_match(
            partial_filters, first_result, exact=False
        )

    def test_exact_partial_filtering(self):
        exact_partial_filters = {"extension": "p"}
        titles = Libgen.search_title(
            title, exact_partial_filters, exact_match=True
        )

        assert len(titles) == 0

    def test_resolve_download_links(self):
        titles = Libgen.search_author(author)
        title_to_download = titles[0]
        dl_links = title_to_download.get_download_links()

        # ensure each host is in the results and that they each have a url and the cover
        assert (["GET", "Cloudflare", "IPFS.io", "Infura", "cover"] == list(dl_links.keys())) & (
            False not in [len(link) > 0 for key, link in dl_links.items()]
        )

    # should return an error if search query is less than 3 characters long
    def test_raise_error_on_short_search(self):
        with pytest.raises(Exception):
            titles = Libgen.search_title(title[0:2])
    
    def test_download(self):
        titles = Libgen.search_author(author)
        title_to_download = titles[0]
        # download the first link
        book_as_bytes = title_to_download.download()

        assert isinstance(book_as_bytes, bytes)

####################
# Helper Functions #
####################

# Check object fields for equality -
# -> Returns True if they match.
# -> Returns False otherwise.
#
# when exact-True, fields are checked strictly (==).
#
# when exact=False, fields are normalized to lower case,
# and checked whether filter value is a subset of the response.
def fields_match(filter_obj, response_obj, exact=True):

    for key, value in filter_obj.items():

        if exact is False:
            value = value.lower()
            response_obj[key] = response_obj[key].lower()
            if value not in response_obj[key]:
                return False

        elif response_obj[key] != value:
            return False
    return True
