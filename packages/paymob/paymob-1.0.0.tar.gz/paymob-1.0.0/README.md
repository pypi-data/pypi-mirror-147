# Paymob Python SDK

## _The Fast Way To Get Payment Duds Ready, Ever_

Paymob Python is a minimal, straightforward and easy way to config payment intention methods, voiding, refunding and more..

Find the [documentation](https://docs.paymob.com/)

## Installation        
<!-- STEPS -->

## Prerequisites
- Python Requests


## Supported languages
- Python 3.6+


## Intention
Paymob Python offers variety of intention methods like create, retrieve and list.

- Create
<!-- SAMPLE -->
```
import paymob
from paymob.logging import log

paympb.secret_key= "secret_key"

def secret():
    intent = paymob.accept.Intention.create(
        amount="300",
        currency="EGP",
        payment_methods=["card","kiosk"],
        items= [
    {
        "name": "ASC1124",
        "amount": "150",
        "description": "Smart Watch",
        "quantity": "1"
    },
    {
        "name": "ERT6565",
        "amount": "150",
        "description": "Power Bank",
        "quantity": "1"
    }
    ],
        billing_data={
            "apartment": "803",
            "email": "claudette09@exa.com",
            "floor": "42",
            "first_name": "Mohamed",
            "street": "Ethan Land",
            "building": "8028",
            "phone_number": "9135210487",
            "shipping_method": "PKG",
            "postal_code": "01898",
            "city": "Jaskolskiburgh",
            "country": "CR",
            "last_name": "Nicolas",
            "state": "Utah",
        },
        customer={"first_name": "misrax", "last_name": "misrax", "email": "misrax@misrax.com"},
        delivery_needed=False,
        extras= {
            "name": "test",
            "age": "30"
        },
        special_reference= "Special reference test 4"
    )
    log(
        "Intention Creation Response - {intent}".format(
            intent=intent
        ),
        "info",
    )
    return intent


```
Example: https://github.com/PaymobAccept/paymob-python/blob/main/paymob-marketplace/app.py


