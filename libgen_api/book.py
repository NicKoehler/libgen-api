from requests import get
from bs4 import BeautifulSoup

MIRROR_SOURCES = ["GET", "Cloudflare", "IPFS.io", "Infura"]

class Book():
    """
    This class represents a libgen book.
    """
    
    def __init__(
        self,
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
    ) -> None:
        self.id = id
        self.author = author
        self.title = title
        self.publisher = publisher
        self.year = year
        self.pages = pages
        self.language = language
        self.size = size
        self.extension = extension
        self.mirrors = mirrors

    def get_download_links(self) -> dict[str:str]:
        """
        Get the download links for the book.
        in this mirror also the book's cover url is present.

        Returns:
            A dictionary of download links and cover url.

            Example:
                {
                    'GET':          'http://...',
                    'Cloudflare':   'https://...',
                    'IPFS.io':      'https://...',
                    'Infura':       'https://...',

                    'cover':        'https://...'
                }
        """
        page = get(self.mirrors[0])
        soup = BeautifulSoup(page.text, "lxml")
        links = soup.find_all("a", string=MIRROR_SOURCES)
        download_links = {link.string: link["href"] for link in links}
        download_links["cover"] = self.mirrors[0].split("/main")[0] + soup.find("img", {"alt": "cover"}).get("src")
        return download_links
    
    def download(self) -> bytes:
        """
        Download the book from Cloudflare mirror and returns it as bytes.
        """
        link = self.get_download_links().get("Cloudflare")

        if link is None:
            raise ValueError("No Cloudflare link found for this book.")

        try:
            return get(link).content
        except Exception as e:
            raise e

    @staticmethod
    def from_dict(books_dict: list[dict]):
        """
        Returns a list of books from a list of dictionaries.
        """

        return [
            Book(
                id=item["id"],
                author=item["author"],
                title=item["title"],
                publisher=item["publisher"],
                year=item["year"],
                pages=item["pages"],
                language=item["language"],
                size=item["size"],
                extension=item["extension"],
                mirrors=[
                    item["mirror_1"],
                    item["mirror_2"],
                    item["mirror_3"],
                    item["mirror_4"],
                ],
            ) for item in books_dict
        ]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, {self.author}, {self.title})"

    def __getitem__(self, item):
        return getattr(self, item)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
