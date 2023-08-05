"""Cofactr client."""
# Python Modules
import json
from typing import List, Literal, Optional
from urllib import parse

# 3rd Party Modules
import urllib3

Protocol = Literal["http", "https"]


drop_none_values = lambda d: {k: v for k, v in d.items() if v is not None}

parse_query_params = lambda url: {
    k: v[0] for k, v in parse.parse_qs(parse.urlparse(url).query).items()
}

parse_paging_data = lambda paging: {
    "previous": parse_query_params(paging["previous"]),
    "next": parse_query_params(paging["next"]),
}


class GraphAPI:
    """A client-side representation of the Cofactr graph API."""

    PROTOCOL: Protocol = "https"
    HOST = "graph.cofactr.com"

    def __init__(
        self, protocol: Optional[Protocol] = PROTOCOL, host: Optional[str] = HOST
    ):

        self.url = f"{protocol}://{host}"
        self.http = urllib3.PoolManager()

    def check_health(self):
        """Check the operational status of the service."""

        res = self.http.request("GET", self.url)

        return json.loads(res.data.decode("utf-8"))

    def get_products(
        self,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
        external: Optional[bool] = True,
    ):
        """Get products.

        Args:
            query: Search query.
            fields: Used to filter properties that the response should contain. A field can be a
                concrete property like "mpn" or an abstract group of properties like "assembly".
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Maximum number of entities the response should contain.
            external: Whether to query external sources.
        """

        res = self.http.request(
            "GET",
            f"{self.url}/products",
            fields=drop_none_values(
                {
                    "q": query,
                    "fields": fields and ",".join(fields),
                    "before": before,
                    "after": after,
                    "limit": limit,
                    "external": external,
                }
            ),
        )

        data = json.loads(res.data.decode("utf-8"))

        data["paging"] = parse_paging_data(data["paging"])

        return data

    def get_orgs(
        self,
        query: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
    ):
        """Get organizations.

        Args:
            query: Search query.
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Maximum number of entities the response should contain.
        """

        res = self.http.request(
            "GET",
            f"{self.url}/orgs",
            fields=drop_none_values(
                {
                    "q": query,
                    "before": before,
                    "after": after,
                    "limit": limit,
                }
            ),
        )

        data = json.loads(res.data.decode("utf-8"))

        data["paging"] = parse_paging_data(data["paging"])

        return data

    def get_product(self, id: str):
        """Get product."""

        res = self.http.request("GET", f"{self.url}/products/{id}")

        return json.loads(res.data.decode("utf-8"))

    def get_org(self, id: str):
        """Get organization."""

        res = self.http.request("GET", f"{self.url}/orgs/{id}")

        return json.loads(res.data.decode("utf-8"))
