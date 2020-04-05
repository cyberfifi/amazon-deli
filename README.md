# COVID-19 Grocery Assistant
This is a selenium BOT that will access your Amazon Fresh delivery page through browser. 
Once a delivery window is detected, you will get an SMS.

# Note
- Only tested on MAC. If you want to run on linux, you need a different web driver other
than the chromedriver-mac.
- The Amazon 2FA is the biggest blocker. This app will only support if Amazon sends a 2FA
request to you Amazon Mobile App. You need to click and confirm it with in 1 min. 
Otherwise, login will fail.
- After running for a while, the app may get stuck and not responding
- Whole Foods is not support since the checkout process is too complicated

# Prerequisites
## Twillio
You will need Twillio to send SMS
### Get your Twillio account 
https://www.twilio.com/try-twilio

After creating the account, follow the instructions to get `sid` and `auth_token`
### Add your number as verified number
Twillio trial account only allows you to send SMS to verified numbers

https://www.twilio.com/console/phone-numbers/verified

## Amazon
### Mobile App
Install the Amazon Mobile App on your phone. You will need this for the potential Two 
Factor Authentication step. You will also need this to place the order once your receive
the SMS notification.
### Cart
Make sure you always put some items in both of your Fresh cart. 
The bot will not be able to access delivery page without items in your carts.

## Python 3
This app requires Python 3

# Installation
## Generate Credentials
Run `./init.sh` 

Update the generated `credentials.yaml` file with your real information
## Install dependencies
Always recommended to activate a virtual environment before you do this.

Run `pip install -r requirements.txt`

# Run
Again, highly recommended to run this in a virtual environment

In the project root, run `PYTHONPATH=. python src/main.py`

# TODO
Wrap this as a Docker App. 但我不会为了金钟乔一个人去做这个功能。
