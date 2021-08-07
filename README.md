# CaptchaCoin

Captchacoin ia a web based application that lets you earn coins by solving captchas.
This fictitious crypto currency does not rely on computers proving their work but on **100% human work**. 
All transactions are shown on the "Blockchain" and like in the real world of crypto you can go to the shop and get yourself some NFT's.

The dollar CaptchaCoin exchange rate is based on what real workers get by solving captchas. There are a number of companies that provide the service of captcha solving to bypass restictions on the web. For image captchas the wage is around 0.7$ per 1000 captchas.

# Project design
The flask app is hosted on heroku at https://captchacoin.herokuapp.com/.
The app.py file contains the site's structure and all the main functions for generating captchas, validating, transactions and loggging in. The helpers.py file contains functions for the exchange rate, generating random keys and translating timestamps.In my three SQL tables I store user data, log each earned captcha and all the transactions.
To keep everything organized and seperate I decided to wirte the javascript directly onto the individual html pages. 
