Demo Video : https://youtu.be/1BmRKKI2gqM

# CaptchaCoin

Captchacoin ia a web based application that lets you earn coins by solving captchas.
This fictitious crypto currency does not rely on computers proving their work but on **100% human work**. 
All transactions are shown on the "Blockchain" and like in the real world of crypto you can go to the shop and get yourself some NFT's.

The dollar CaptchaCoin exchange rate is based on what real workers get by solving captchas. There are a number of companies that provide the service of captcha solving to bypass restictions on the web. For image captchas the wage is around 0.7$ per 1000 captchas. To create the illusion of a volatile exchange rate by calling a function every time the app is opened that returns random values from a normal (Gaussian) distribution. 

# Web Routes/Pages

These are the main pages

- Work
  - here the user can earn coins by solving captchas. Each time the site loads a new random image captcha is created. To give feedback a sound plays and a little bubble appears. In the stats box you can find your sucessrate and average solving time. Each captcha solving is saved in the work datatable. With javascript the time is stopped that passes while solving captchas. The timestamp is set on entering the first key untill clicking the submit button. 
- Shop
  - Here the user can browse through some "NFT" art to get a sence of the dollar captchacoin exchange rate. Of course the user wont have enough coin to buy the NFT's but is sent to the about page.
- About
  - This page contains an explaination of the main ideas behind captchacoin
- Transaction
  - Users can send each other coin using their public keys.
- Blockchain
  This site only contains a table where each transaction is shown publicly.

# Tech-Stach

- **ripples** to create the beautiful liquify effect on the index page
- **bootstrap** for basic styling
- Libraries:
  - **Captcha** - For generating image captchas
  - **numpy** - For generating random values in a normal distribution
  - **datetime** - To create timestamps

The app is hosted on **heroku** at https://captchacoin.herokuapp.com/.



This project was created as my final project for Harvard introduction to computer science course CS50x
