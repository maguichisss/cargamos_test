# cargamos.py

```python
import cargamos

package = cargamos.Package()

address = cargamos.Address(
  "Evergreen terrace", "48007", "Springfield", "Springfield",
  "Nevada", "USA", address_line_2="742", notes="Simpson's house",
)

args = ["Evergreen terrace","48007","Springfield","Springfield","Nevada","USA",]
kwargs = dict(address_line_2="742", notes="Simpson's house", sku="order_1")

order = cargamos.Order(*args, **kwargs)
```

# locations.py

```python
import locations

locations = locations.Locations(3,4,7)
locations.element(2,2,2) # output 17
locations.add("something", 2,2,2)
locations.list_all()
```

# api.py

Es un script que se puede ejecutar de la siguiente manera
```
python3 api.py ./orders.csv --skus sku,1231231123,emptyX
```
# unittests
Dentro del proyecto ejecutar:
```
python3 -m unittest test_cargamos.py
python3 -m unittest test_locations.py
python3 -m unittest test_api.py
```

