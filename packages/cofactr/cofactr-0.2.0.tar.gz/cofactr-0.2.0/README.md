# Cofactr

Python client library for accessing Cofactr.

## Example

```python
from urllib import parse
from cofactr.graph import GraphAPI

graph_api = GraphAPI()

resistors = graph_api.get_products(
    query="resistor",
    fields=["mpn", "assembly"],
    limit=3,
    external=False,
)

more_resistors = graph_api.get_products(**resistors["paging"]["next"])
```