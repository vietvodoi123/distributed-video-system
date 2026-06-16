from shared.discovery.parsers.list_page_parser import (
    ListPageParser
)

from shared.discovery.parsers.bs4_parser import (
    BS4DiscoveryParser
)


class ParserFactory:

    @staticmethod
    def create(
        website
    ):

        parser_type = (
            website.parser_type
        )

        if parser_type == "list_page":

            return ListPageParser(
                website
            )

        if parser_type == "single_page":

            return BS4DiscoveryParser(
                website
            )

        return BS4DiscoveryParser(
            website
        )