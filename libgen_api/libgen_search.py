from .book import Book
from .search_request import SearchRequest

class Libgen:
    """
    Class Libgen with the following static methods:

    Methods:
        search_title: Search for books by title.
        search_author: Search for books by author.
    """

    @staticmethod
    def search_title(query: str, filters: dict = None, exact_match: bool = True) -> list[Book]:
        """
        Search for books by title.

        Args:
            query: The title to search for.
            filters: A dictionary of filters to apply to the search.
                e.g. {"year": "2007", "extension": "pdf"}
            Possible filters are:
                id - author - title - publisher - year - pages - language - size - extension

            exact_match: If True, the search will be performed with an exact match.

        Returns:
            A list of books matching the search.

        """

        search_request = SearchRequest(query, search_type="title")
        results = search_request.aggregate_request_data()

        if filters is not None:
            check_filter(filters)
            results = filter_results(
                results=results, filters=filters, exact_match=exact_match
            )
        
        return Book.from_dict(results)

    @staticmethod
    def search_author(query: str, filters: dict = None, exact_match: bool = True) -> list[Book]:
        """
        Search for books by author.

        Args:
            query: The author to search for.
            filters: A dictionary of filters to apply to the search.
                e.g. {"year": "2007", "extension": "pdf"}
            Possible filters are:
                id - author - title - publisher - year - pages - language - size - extension

            exact_match: If True, the search will be performed with an exact match.

        Returns:
            A list of books matching the search.

        """

        search_request = SearchRequest(query, search_type="author")
        results = search_request.aggregate_request_data()

        if filters is not None:
            check_filter(filters)
            results = filter_results(
                results=results, filters=filters, exact_match=exact_match
            )
        
        return Book.from_dict(results)


def check_filter(filter: dict):
    """
    reise error if filter is not a dict or if any of the keys are not in SearchRequest.col_names
    """
    valid_filters = SearchRequest.col_names[:-6]

    if not isinstance(filter, dict):
        raise ValueError("Filter must be a dict.")
    if any(i not in valid_filters for i in filter.keys()):
        raise ValueError(
            "Invalid filter keys. Valid keys are: " + ", ".join(valid_filters)
        )


def filter_results(results, filters, exact_match) -> list[dict]:
    """
    Returns a list of results that match the given filter criteria.
    When exact_match = true, we only include results that exactly match
    the filters (ie. the filters are an exact subset of the result).

    When exact-match = false,
    we run a case-insensitive check between each filter field and each result.

    exact_match defaults to TRUE -
    this is to maintain consistency with older versions of this library.
    """

    filtered_list = []
    if exact_match:
        for result in results:
            # check whether a candidate result matches the given filters
            if filters.items() <= result.items():
                filtered_list.append(result)

    else:
        filter_matches_result = False
        for result in results:
            for field, query in filters.items():
                if query.casefold() in result[field].casefold():
                    filter_matches_result = True
                else:
                    filter_matches_result = False
                    break
            if filter_matches_result:
                filtered_list.append(result)
    return filtered_list
