# Python M-Pesa Daraja API
**This is an sdk providing convenient access to the Safaricom MPESA Daraja API for applications written in Python3.**

## Prerequisites
1. Python >= 3.7

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
from mpesa import MpesaBase

mpesa_api = MpesaBase(
    consumer_key='<your consumer key>',
    consumer_secret='<your consumer secret>'
)

mpesa_api.authenticate()
```

# Supported APIs
* Authorization
* Customer to Business (C2B)
* Business to Customer (B2C)
* Transaction Status
* Account Balance

# API Classes
The following are the corresponding API classes
* MpesaBase
* C2B
* B2C
* TransactionStatus
* Balance

# Methods

* Authorization

This API generates the tokens for authenticating your subsequent API calls

````Python
from mpesa import MpesaBase

mpesa_api = MpesaBase(
    consumer_key='<your consumer key>',
    consumer_secret='<your consumer secret>'
)
mpesa_api.authenticate()
````

* Customer To Business (C2B)

This API enables you to register the callback URLs via which you shall receive notifications for payments to your pay bill/till number.

````python
from mpesa import C2B

c2b = C2B(
    consumer_key='<your consumer key>',
    consumer_secret='<your consumer secret>'
)

# Registers confirmation and validation URLs with Mpesa for C2B transactions.
c2b.register(
    short_code=600798,
    response_type='Completed',
    confirmation_url='<your confirmation url>',
    validation_url='<your validation url>'
)

# This initiates a C2B transaction between an end-user and a company (paybill or till number)
c2b.simulate(
    short_code=600987,
    command_id='<your command id>',
    amount=10,
    msisdn='2547XXXXX'
)
````

* Business To Customer (B2C)

This method enables you to make payments from a Business to Customers (Pay Outs), also known as Bulk Disbursements
B2C API is used by businesses that require to either make Salary Payments, Cashback payments and loan disbursements

````python
from mpesa import B2B

b2c = B2C(
    app_key='<your consumer key>'
    app_secret='<your consumer secret>'
)

# This initiates a B2C transaction between a business and customer
b2c.transact(
    originator_conversation_id="conversation_id",
    initiator_name="testapi",
    security_credential="security_credential",
    command_id="BusinessPayment",
    amount=10,
    party_a=600798,
    party_b="2547XXXXXX",
    remarks="test payment",
    queue_timeout_url="https://example.com/queue",
    result_url="https://example.com/result",
    ocassion="Test"
)
````

* TransactionStatus

This method tests the status of a transaction

````python
from mpesa import TransactionStatus

status = TransactionStatus(
    app_key='<your app key>',
    app_secret='<your app secret>'
)

status.check_transaction_status(
    originator_conversation_id="conversation_id",
    party_a=600798,
    initiator="testapi",
    security_credential="security_credential",
    identifier_type=4,
    remarks="Remarks",
    transaction_id="transaction_id",
    queue_timeout_url="https://example.com/queue",
    result_url="https://example.com/results",
    occasion="Test"
)
````
