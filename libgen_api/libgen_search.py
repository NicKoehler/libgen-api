from .book import Book
from .search_request import SearchRequest

class Libgen:

    @staticmethod
    def search_title(query: str, filters: dict = None, exact_match: bool = True) -> list[Book]:

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
    if not isinstance(filter, dict):
        raise ValueError("Filter must be a dict.")
    if any(i not in SearchRequest.col_names for i in filter.keys()):
        raise ValueError(
            "Invalid filter keys. Valid keys are: " + ", ".join(SearchRequest.col_names)
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
