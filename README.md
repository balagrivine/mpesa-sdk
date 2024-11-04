# Python M-Pesa Daraja API
**This is an sdk providing convenient access to the Safaricom MPESA Daraja API for applications written in Python3.**

## Prerequisites
1. Python3 >= 3.7
2. 

## Installation
Use pip

```shell
pip install mpesa-sdk
```

### Pre-usage
**Please make sure you have read the documentation on [Daraja](https://developer.safaricom.co.ke/home) before continuing.**

You need the following before getting to use this library:
1. Consumer Key and Consumer secret
2. Test credentials *(Optional only for sandbox)*

## Getting started
This is the first API you will call to authenticate subsequent api calls.
```python
from mpesa-sdk.api.auth import MpesaBase

mpesa_api = MpesaBase(
    consumer_key='<your consumer key>',
    consumer_secret='<your consumer secret>'
)

mpesa_api.authenticate()
```

# Supported APIs
* Authorization
* Customer to Business (B2C)
* Business to Customer (C2B)
* Transaction Status
* Account Balance

# API Classes
The following are the corresponding API classes
* MpesaBase
* C2B
* B2C
* TransactionStatus
* Balance

All calls are done by httpx, so for the response structure check httpx documentation.

# Methods
* [Authorization](https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials)
This API generates the tokens for authenticating your subsequent API calls

````Python
mpesa_api.authenticate()
````

* [Customer To Business (C2B)](https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl)
This API enables you to register the callback URLs via which you shall receive notifications for payments to your pay bill/till number.

````python
from mpesa-sdk.api.c2b import C2B

c2b = C2B(
    consumer_key='<your consumer key>',
    consumer_secret='<your consumer secret>'
)

# Registers confirmation and validation URLs with Mpesa for C2B transactions.
c2b.register(
    short_code='XXXXXX',
    response_type='Completed',
    confirmation_url='<your confirmation url>',
    validation_url='<your validation url>'
)

# This initiates a C2B transaction between an end-user and a company (paybill or till number)
c2b.simulate(
    short_code='XXXXXX',
    command_id='<your command id>',
    amount=10,
    msisdn='2547XXXXX'
)
````
