#import the libraries 
from bs4 import BeautifulSoup  #used for web scraping purposes to pull the data out of HTML and XML files. 
import requests #will allow you to send HTTP/1.1 requests using Python.
import time  #provides various time-related functions
import smtplib #client session object that can be used to send mail to any Internet machine
import ssl #to create secure connection between client and server
from email.mime.text import MIMEText as MT #used to create MIME objects of major type text
from email.mime.multipart import MIMEMultipart as MM #can be used to specify the subtype of the message
import PySimpleGUI as sg # for GUI

#create a function to get the price of a bitcoin
def get_crypto_price(coin):
  #Get the URL
  url = "http://www.google.com/search?q="+coin+"+price"

  #Make a request to the website 
  HTML =  requests.get(url)

  #Parse the HTML
  soup = BeautifulSoup(HTML.text, 'html.parser')

  #Find the current price 
  text = soup.find("div", attrs={'class':'BNeawe iBp4i AP7Wnd'}).text

  #Return the text
  return text

#store the email addresses for the receiver, and the sender and stort the sender password
receiver = 'ganorkarniranjan@gmail.com'
sender ='gpcharde@gmail.com'
sender_password= 'enter your pass'

#Create a function to send emails
def send_email(sender, receiver, sender_password, text_price):
  #create a MIMEMultipart Object 
  msg = MM()
  msg['Subject']= "New Crypto Price Alert !"
  msg['From'] = sender
  msg['To'] = receiver

  #create the HTML for the message
  HTML = """
    <html>
      <body>
        <h1>New Crypto Price Alert !</h1>
        <h2>"""+text_price+"""
        </h2>
      </body>
    </html>
    """

  #create a html MIMEText Object 
  MTObj = MT(HTML, "html")
  #Attach the MIMEText Object 
  msg.attach(MTObj)


  #create the secure socket layer (SSL) context object 
  SSL_context = ssl.create_default_context()
  #create the secure simple mail transfer Protocol (SMTP) connection
  server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=SSL_context)
  #login to the email 
  server.login(sender, sender_password)
  #send the email
  server.sendmail(sender, receiver, msg.as_string())

#Create a function to display price alert on GUI
def gui_alert(coin, price):
    layout = [[sg.Text(coin.capitalize()+' price: '+ str(price))],
              [sg.Button("OK")]]

    # Create the window
    window = sg.Window("Crypto Currency Alert!!", layout, size=(300,75))

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()

#create a function to send the alert 
def send_alert():
  last_price = -1
  #create an infinite loop to continously send/show the price 
  while True:
    # choose the cryptocurrency/coin 
    coin = 'bitcoin'
    #get the price of the cryptocurrency 
    price = get_crypto_price(coin)
    #check if the price has changed 
    if price != last_price:
      print(coin.capitalize()+' price: ', price)
      gui_alert(coin, price)
      price_text = coin.capitalize()+' is '+price
      send_email(sender, receiver, sender_password, price_text)
    
      last_price = price #update the last price
      time.sleep(3)

#send alert
send_alert()