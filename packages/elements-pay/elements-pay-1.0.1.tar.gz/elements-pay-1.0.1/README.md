# Elements Python SDK

Python bindings for the Elements API.

## Installation

You can install this package from source:

```bash
python setup.py install
```

## Configuration

This library requires you to configure the API key:

```python
import elements
elements.api_key = "my_api_key"
```

You may connect to the sandbox by configuring the base url:

```python
import elements
elements.api_base = elements.API_SANDBOX
```

## Usage

```python
import elements

# To create an authorized charge
authorized_charge = elements.Charge.create(
    amount=300000,
    currency="USD",
    payment_method_id="PM-XXXX",
)

# Access model attributes like object fields
authorized_charge.amount # 30000
authorized_charge.currency # "USD"
authorized_charge.captured # False


# To capture a charge
captured_charge = elements.Charge.capture(
    "CH-pV4rzxf9yRoWaPeJL2C47JoC",
    amount=300000
)

# To create a client token
client_token = elements.ClientToken.create(external_customer_id="foo").client_token

# To retrieve a payment method
payment_method = elements.PaymentMethod.retrieve(
    "PM-XXXX",
    external_customer_id="cus_ext_id"
)
```

Please refer to our REST API docs for detailed API usage.

## Development and Testing

First, set up the virtualenv for development by:

```bash
make
```

Then you may run tests like so:

```bash
make test
```

If you want to test for a specific Python version, supply the version like so (you must have the corresponding version installed first):

```bash
TOX_ARGS="-e py38" make test
```

To run the formatter, do

```bash
make fmt
```

For adhoc testing, you may start a Python REPL and import elements, you may test your changes with a local or a sandbox
environment by setting the `api_base` and `api_key`:

```python
import elements
elements.api_base = "http://localhost:3000"
elements.api_key = "my_api_key"
```
