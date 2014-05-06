blockchain.py
=============

Blockchain.info python API

Requirements: python3

Example of usage:

```
import blockchain

uid='Your-blockchain.info-uid'
pass1='Main-Password'
pass2='Secondary-Password-if-exists'

wallet = blockchain.Wallet(guid=uid,password1=pass1,password2=pass2)
print(wallet.getBalance())
```
