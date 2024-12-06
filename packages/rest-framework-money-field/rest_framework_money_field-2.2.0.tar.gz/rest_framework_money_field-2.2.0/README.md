# Money field for Django REST framework

[![pipeline status][pipeline-image]][pipeline-url]
[![coverage report][coverage-image]][coverage-url]
[![pypi][pypi-image]][pypi-url]

An serializer field implementation for [Django REST framework] that serializes
monetary types provided by [py-moneyed] library. Serialized data is compatible
with [Dinero.js] JavaScript library.

## Usage example

For example, if you would have an serializer like this:

```python
from rest_framework.serializers import Serializer
from rest_framework_money_field import MoneyField


class ProductSerializer(Serializer):
    price = MoneyField()
```

And you would use the serializer with data like this:

```python
from moneyed import Money
from rest_framework.renderers import JSONRenderer

serializer = ProductSerializer({"price": Money(50, "EUR")})
json = JSONRenderer().render(serializer.data)
```

You would end up with JSON like this:

```json
{
    "price": {
        "amount": 5000,
        "currency": "EUR"
    }
}
```

[django rest framework]: https://www.django-rest-framework.org/
[py-moneyed]: https://github.com/py-moneyed/py-moneyed
[dinero.js]: https://dinerojs.com/
[pipeline-url]: https://gitlab.com/treet/rest-framework-money-field/commits/master
[pipeline-image]: https://gitlab.com/treet/rest-framework-money-field/badges/master/pipeline.svg
[coverage-url]: https://gitlab.com/treet/rest-framework-money-field/commits/master
[coverage-image]: https://gitlab.com/treet/rest-framework-money-field/badges/master/coverage.svg
[pypi-url]: https://pypi.org/project/rest-framework-money-field
[pypi-image]: https://badge.fury.io/py/rest-framework-money-field.svg
