import requests
from bs4 import BeautifulSoup, ResultSet

class Scrapper:
    """
    Class for scraping data from a website, specifically designed for WooCommerce-based stores.

    Args:
        url (str): The base URL of the website to scrape.
    """
    def __init__(self, url):
        self.url = url

    def get_content(self, htype, hclass, url, href = False)-> ResultSet[any]:
        """
        Fetches the content of a given URL and parses it using BeautifulSoup.

        Args:
            htype (str): The HTML tag to search for.
            hclass (str): The class attribute of the HTML tag.
            url (str): The URL to fetch.
            href (bool, optional): Whether to include links in the results. Defaults to False.

        Returns:
            ResultSet[Any]: A list of BeautifulSoup elements matching the criteria.
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        content = soup.find_all(htype, class_=hclass, href=href)
        return content

    def get_text_input(self, htype, hclass, url)->list:
        """
        Extracts text from elements matching the given criteria.

        Args:
            htype (str): The HTML tag to search for.
            hclass (str): The class attribute of the HTML tag.
            url (str): The URL to fetch.

        Returns:
            list: A list of extracted text.
        """
        target = self.get_content(htype, hclass, url=url)
        target = [x.text for x in target]
        return target

    def get_link_input(self, htype, hclass)->list:
        """
        Extracts links from elements matching the given criteria.

        Args:
            htype (str): The HTML tag to search for.
            hclass (str): The class attribute of the HTML tag.

        Returns:
            list: A list of extracted links.
        """
        links = self.get_content(htype, hclass, href=True, url=self.url)
        links = [x["href"] for x in links]
        return links

    def scrap_links(self, link_list)->list|list:
        """
        Scrapes product descriptions and stock information from a list of product links.

        Args:
            link_list (list): A list of product URLs.

        Returns:
            contents (list): Returns product descriptions.
            stocks (list): Returns stock information.
        """
        contents = []
        stocks = []
        for link in link_list:
            content = self.get_content(
                "div",
                "woocommerce-product-details__short-description",
                url=link,
                href=False,
            )
            content = content[0].text.strip()
            contents.append(content)
            stock = self.get_text_input(htype="p", hclass="stock in-stock", url=link)
            stocks += stock
        return contents, stocks

    def create_json(self, names, prices, descriptions, stocks)->list:
        """
        Creates a list of dictionaries representing products.

        Args:
            names (list): A list of product names.
            prices (list): A list of product prices.
            descriptions (list): A list of product descriptions.
            stocks (list): A list of product stock information.

        Returns:
            list: A list of dictionaries, each representing a product.
        """
        json_data = []
        for n, p, d, s in zip(names, prices, descriptions, stocks):
            jdict = {"names": n, "prices": p, "description": d, "stock": s}
            json_data.append(jdict)
        return json_data

    def call(self) ->list :
        """
        Main scraping function to extract product information.

        Returns:
            list: A list of dictionaries representing scraped products.
        """
        names = self.get_text_input(
            "h2", hclass="woocommerce-loop-product__title", url=self.url
        )
        prices = self.get_text_input(
            "span", hclass="woocommerce-Price-amount amount", url=self.url
        )[1:]
        links = self.get_link_input(
            "a", "woocommerce-LoopProduct-link woocommerce-loop-product__link"
        )
        descriptions, stocks = self.scrap_links(links)
        json_data = self.create_json(names, prices, descriptions, stocks)
        return json_data

