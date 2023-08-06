
Library that allows you to connect to the LVA valuation API 

To use it, you need credentials provided by the LVA valuation team.

<br>



<br>

##  Example Usage

```
from  Valuation_API import ConnectionAPILVA
import pprint

pp = pprint.PrettyPrinter(indent=4)

api_v = ConnectionAPILVA()

api_v.api_connection(user, password)

response = api_v.request_data(query)

pp.pprint(response)
```