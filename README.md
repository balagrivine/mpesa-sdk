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
* Mpesa Express
* Reversals

# API Classes
The following are the corresponding API classes
* MpesaBase
* C2B
* B2C
* TransactionStatus
* Balance
* MpesaExpress
* Reversal

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
    consumer_key='<your_consumer_key>',
    consumer_secret='<your_consumer_secret>'
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
    command_id='<command_id',
    amount=10,
    msisdn='2547XXXXX'
)
````

* Business To Customer (B2C)

This method enables you to make payments from a Business to Customers (Pay Outs), also known as Bulk Disbursements
B2C API is used by businesses that require to either make Salary Payments, Cashback payments and loan disbursements

````python
from mpesa import B2C

b2c = B2C(
    app_key='<your_consumer_key>'
    app_secret='<your_consumer_secret>'
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

This class checks the status of a transaction

````python
from mpesa import TransactionStatus

status = TransactionStatus(
    app_key='<your_consumer_key>',
    app_secret='<your_consumer_secret>'
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

* Balance

This class enquire the balance on an M-Pesa BuyGoods (Till Number)

````python
from mpesa import Balance

balance = Balance(
    app_key='<your_consumer_key>',
    app_secret='<your_consumer_secret>'
)

balance.get_balance(
    initiator='test_api_user',
    security_credential='<your_security_credential>',
    party_a=123456,
    identifier_type=4,
    remarks='Test balance enquiry',
    queue_timeout_url='https://example.com/timeout',
    result_url='https://exmple.com/result'
)
````

* MpesaExpress

This class initiates online payment through STK push on behalf of a customer
and checks the status of the transaction

````python
from mpesa import MpesaExpress

mpesa_express = MpesaExpress(
    app_key='<your_consumer_key>',
    app_secret='<your_consumer_secret>'
)

# Initiate an stk push to a customer
mpesa_express.stk_push(
    short_code=123456,
    pass_key='<your_pass_key>',
    transaction_type='transaction_type',
    amount=10,
    sender_msisdn='2547XXXXXX',
    receiver_msisdn='2547XXXXXX',
    callback_url='https://example.com/callback',
    transaction_desc='Test stk push',
    account_ref='AccountReference'
)

# Check the status of the stk push
mpesa_express.status(
    short_code=123456,
    checkout_request_id='<checkout_request_id>',
    pass_key='<your pass key>'
)
````

* Reversal

This class interacts with M-pesa's reversal api to
revesrse a C2B transactions

````python
from mpesa import Reversal

reversal = Reversal(
    app_key='<your_consumer_key>',
    app_secret='<your_consumer_secret>'
)

reversal.reverse(
    receiver=123456,
    initiator='test_api_user',
    amount=10,
    security_credential='<your_security_credential>',
    transaction_id='transaction_id',
    timeout_url='https://example.com/timeout',
    remarks='Test reversal',
    receiver_identifier='11'
)
````
