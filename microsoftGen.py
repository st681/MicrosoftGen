from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random
import re
import imaplib
import email
import requests
import csv
from licensing.models import*
from licensing.methods import Key, Helpers


print("""\
              __  __ _                           __ _      _____                           _             
             |  \/  (_)                         / _| |    / ____|                         | |            
             | \  / |_  ___ _ __ ___  ___  ___ | |_| |_  | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
             | |\/| | |/ __| '__/ _ \/ __|/ _ \|  _| __| | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
             | |  | | | (__| | | (_) \__ \ (_) | | | |_  | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
             |_|  |_|_|\___|_|  \___/|___/\___/|_|  \__|  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   

""")



def menu():
   choice = input("""
                         A: Generator
                         B: Payment Inserter
   
                         Please enter your choice: """)

   if choice == "A" or choice =="a":
      generate()
   elif choice == "B" or choice =="b":
      payment_insert()
   else:
      print("You must only select either A or B")
      print("Please try again")
      menu()

def generate():
   catchall = input("Input catchall domain:")
   privateemailusername = input("Input catchall username:")
   privateemailpassword = input("Input catchall password:")
   password_accounts = input("Enter password:")
   apikey = input("Enter online sim api key:")
   num_accs = input("Quantity to generate:")

   # set sms api variables
   onlinesimapigetnumlink = "https://onlinesim.ru/api/getNum.php?apikey=" + apikey + "&service=Microsoft&country=1&number"
   onlinesimapigetmsglink = "https://onlinesim.ru/api/getState.php?apikey=" + apikey

   i = 1

   # methods needed
   def check_exists_by_xpath(xpath):
      try:
         driver.find_element_by_xpath(xpath)
      except NoSuchElementException:
         return False
      return True

   def type_out(text_to_type, ELEMENT):
      letters = list(text_to_type)
      for x in letters:
         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ELEMENT)).send_keys(x)
         add_time = random.randint(1, 2)
         add_time_two = random.randint(1, 2)
         time.sleep(0.02 + add_time / 30 + add_time_two / 30)

   while (i <= int(num_accs)):
      lines = open('proxies.txt').read().splitlines()
      full_proxy = random.choice(lines)

      lines = open('firstnames.txt').read().splitlines()
      firstname = random.choice(lines)

      lines = open('lastnames.txt').read().splitlines()
      lastname = random.choice(lines)

      generatedemail = firstname + "." + lastname + "@" + catchall
      print("Creating account: " + generatedemail + "...")

      proxy = re.search(r"(.*):(.*):(.*):(.*)", full_proxy)
      ip = proxy.group(1)
      port = proxy.group(2)
      user = proxy.group(3)
      password_proxy = proxy.group(4)

      options = {
         'proxy': {
            'http': 'http://' + user + ':' + password_proxy + '@' + ip + ':' + port,
            'https': 'https://' + user + ':' + password_proxy + '@' + ip + ':' + port,
         }
      }


      driver = webdriver.Chrome('chromedriver.exe', seleniumwire_options=options)

      driver.get('https://signup.live.com/signup?contextid=DA7D7A6865441E29&bk=1633580513&ru=https://login.live.com/login.srf%3fcontextid%3dDA7D7A6865441E29%26uiflavor%3dweb%26mkt%3dEN-US%26lc%3d1033%26bk%3d1633580513%26uaid%3d849670e383634bd6b5d8c197c5512cf1&uiflavor=web&lic=1&mkt=EN-US&lc=1033&uaid=849670e383634bd6b5d8c197c5512cf1')

      def get_otp():
         otp = []
         # create an IMAP4 class with SSL
         imap = imaplib.IMAP4_SSL("mail.privateemail.com")
         # authenticate
         imap.login(privateemailusername, privateemailpassword)
         status, messages = imap.select("Inbox")
         # number of top emails to fetch
         N = 1
         # total number of emails
         messages = int(messages[0])
         for i in range(messages, messages - N, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
               if isinstance(response, tuple):
                  # parse a bytes email into a message object
                  msg = email.message_from_bytes(response[1])
                  # if the email message is multipart
                  if msg.is_multipart():
                     # iterate over email parts
                     for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                           # get the email body
                           body = part.get_payload(decode=True).decode()
                        except:
                           pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                           body = body.split("To verify your email address use this security code:")[1]
                           body = body.split(
                              "If you didn't request this code, you can safely ignore this email. Someone else might have typed your email address by mistake")[
                              0]
                           otp.append(int(body))
         return otp

      # email page
      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      ENTER_EMAIL = (By.XPATH, '//*[@id="MemberName"]')
      type_out(generatedemail, ENTER_EMAIL)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      NEXT = (By.XPATH, '//*[@id="iSignupAction"]')
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXT)).click()
      # password page
      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      ENTER_PASSWORD = (By.XPATH, '//*[@id="PasswordInput"]')
      type_out(password_accounts, ENTER_PASSWORD)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      NEXT = (By.XPATH, '//*[@id="iSignupAction"]')
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXT)).click()
      # name page
      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      ENTER_FIRST = (By.XPATH, '//*[@id="FirstName"]')
      type_out(firstname, ENTER_FIRST)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      ENTER_LAST = (By.XPATH, '//*[@id="LastName"]')
      type_out(lastname, ENTER_LAST)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      NEXT = (By.XPATH, '//*[@id="iSignupAction"]')
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXT)).click()
      # birthday page
      add_time = random.randint(8, 12)
      add_time_two = random.randint(8, 12)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      random_month = str(random.randint(2, 12))
      month_xpath = "//*[@id='BirthMonth']/option[" + random_month + "]"
      MONTH = (By.XPATH, month_xpath)
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MONTH)).click()

      add_time = random.randint(8, 12)
      add_time_two = random.randint(8, 12)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      random_day = str(random.randint(2, 30))
      day_xpath = "//*[@id='BirthDay']/option[" + random_day + "]"

      add_time = random.randint(8, 12)
      add_time_two = random.randint(8, 12)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      DAY = (By.XPATH, day_xpath)
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(DAY)).click()

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      random_year = random.randint(1980, 2001)
      random_year = str(random_year)
      DAY = (By.XPATH, '//*[@id="BirthYear"]')
      type_out(random_year, DAY)

      add_time = random.randint(8, 12)
      add_time_two = random.randint(8, 12)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      NEXT = (By.XPATH, '//*[@id="iSignupAction"]')
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXT)).click()

      # OPT PAGE
      print("Getting OTP...")
      time.sleep(20)
      otp = get_otp()
      otp_split = [str(i) for i in str(otp[0])]
      if (otp[0] == "0" or otp[0] == 0):
         ENTER_OTP = (By.XPATH, '//*[@id="VerificationCode"]')
         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ENTER_OTP)).send_keys("0")
      ENTER_OTP = (By.XPATH, '//*[@id="VerificationCode"]')
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ENTER_OTP)).send_keys(otp_split)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      NEXT = (By.XPATH, '//*[@id="iSignupAction"]')
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXT)).click()
      # Check for SMS
      time.sleep(5)
      if check_exists_by_xpath('//*[@id="wlspispHipChallengeContainer"]'):
         PHONENUMBER_VERIFY = (By.XPATH,
                               '/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[5]/div[1]/div[2]/input')
         response = requests.get(onlinesimapigetnumlink)
         jsonResponse = (response.json())
         onlinesimnumber = (jsonResponse['number'])
         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(PHONENUMBER_VERIFY)).send_keys(onlinesimnumber)
         # Submit
         SUBMITPHONE = (By.XPATH,
                        '/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[5]/div[2]/a[1]')
         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SUBMITPHONE)).click()
         # Enter SMS Code
         time.sleep(60)
         msg = requests.get(onlinesimapigetmsglink).json()
         msgcode = (msg[0]['msg'])
         INPUTPHONE = (By.XPATH,
                       '/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[5]/div[3]/div/input')
         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(INPUTPHONE)).send_keys(msgcode)
         NEXT = (By.XPATH,
                 '/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[7]/div/div/div[2]/input')
         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXT)).click()
      else:
         # Captcha
         print("Solve manual captcha")

      # Logging process
      FINISHDONE = (By.XPATH, '//*[@id="idSIButton9"]')
      WebDriverWait(driver, 10000).until(EC.element_to_be_clickable(FINISHDONE)).click()
      print("Captcha solved")
      print("Success. Next.")
      with open('generated_accounts.txt', 'a') as the_file:
         the_file.write(generatedemail + ":" + password_accounts + "\n")
      with open('ips.txt', 'a') as the_file:
         the_file.write(full_proxy + ":" + generatedemail + ":" + password_accounts + "\n")
      driver.quit()
      i += 1

def payment_insert():
   def type_out(text_to_type, ELEMENT):
      letters = list(text_to_type)
      for x in letters:
         WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ELEMENT)).send_keys(x)
         add_time = random.randint(1, 2)
         add_time_two = random.randint(1, 2)
         time.sleep(0.02 + add_time / 30 + add_time_two / 30)

   # loop for all csv documents
   with open('tasks.csv', 'r') as f:
      reader = csv.reader(f)
      next(reader)
      lines = len(list(reader))

   with open('tasks.csv', 'r') as f:
      reader = csv.reader(f, delimiter=',')
      next(reader)
      data = []
      for row in reader:
         data.append(row)

   i = 0
   print(data[i][3])
   while i < lines:
      # set proxy for task i
      proxy_extraction = data[i][0]
      print("                                                                                                   ")
      print("                                                                                                   ")
      print("---------------------------------------------------------------------------------------------------")
      print("Task: " + str(i + 1))
      print("PROXY:" + proxy_extraction)
      proxy = re.search(r"(.*):(.*):(.*):(.*)", proxy_extraction)
      ip = proxy.group(1)
      port = proxy.group(2)
      user = proxy.group(3)
      password = proxy.group(4)
      # print(ip)
      # print(port)
      # print(user)
      # print(password)
      options = {
         'proxy': {
            'http': 'http://' + user + ':' + password + '@' + ip + ':' + port,
            'https': 'https://' + user + ':' + password + '@' + ip + ':' + port,
         }
      }

      # browser launch operations
      driver = webdriver.Chrome('chromedriver.exe', seleniumwire_options=options)

      # Microsoft Login

      # launch login site
      driver.get('https://login.live.com')
      # variables for input IDs for live login
      EMAILFIELD = (By.ID, "i0116")
      PASSWORDFIELD = (By.ID, "i0118")
      NEXTBUTTON = (By.ID, "idSIButton9")
      STAYSIGNEDIN = (By.ID, "idSIButton9")

      # reads email and pass, sets as variables
      email = data[i][1]
      emailpass = data[i][2]
      print("ACCOUNT: " + email)
      # wait for email field and enter email
      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      type_out(email, EMAILFIELD)
      # Click Next
      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
      # wait for password field and enter password
      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      type_out(emailpass, PASSWORDFIELD)
      # Click Login - same id?
      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
      # Stay signed in page
      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(STAYSIGNEDIN)).click()
      time.sleep(3)

      # Add Payment
      driver.get('https://account.microsoft.com/billing/payments/?ref=storeuhf')
      time.sleep(5)

      ADDPAYMENT = (
         By.XPATH, '//*[@id="payment-north-star-sdk-app-host"]/div[1]/div[4]/div/div[2]/div/div/div/div/div')
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ADDPAYMENT)).click()

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      CARDNAME = (By.XPATH, '//*[@id="accountHolderName"]')
      card_name = data[i][12]
      type_out(card_name, CARDNAME)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      CARDNUMBER = (By.XPATH, '//*[@id="accountToken"]')
      card_number = data[i][3]
      type_out(card_number, CARDNUMBER)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      MONTH = (By.XPATH, '//*[@id="expiryMonth"]')
      ex_month = data[i][4]
      type_out(ex_month, MONTH)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      YEAR = (By.XPATH, '//*[@id="expiryYear"]')
      ex_year = data[i][5]
      type_out(ex_year, YEAR)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      CVV = (By.XPATH, '//*[@id="cvvToken"]')
      pay_cvv = data[i][6]
      type_out(pay_cvv, CVV)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      LINEONE = (By.XPATH, '//*[@id="address_line1"]')
      line_one = data[i][7]
      type_out(line_one, LINEONE)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      LINETWO = (By.XPATH, '//*[@id="address_line2"]')
      line_two = data[i][8]
      type_out(line_two, LINETWO)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      CITY = (By.XPATH, '//*[@id="city"]')
      pay_city = data[i][9]
      type_out(pay_city, CITY)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      STATE = (By.XPATH, '//*[@id="input_region-option"]')
      pay_city = data[i][10]

      d = {
         'Alabama': '1',
         'Alaska': '2',
         'Arizona': '3',
         'Arkansas': '4',
         'Armed Forces Africa': '5',
         'Armed Forces America': '6',
         'Armed Forces Pacific': '7',
         'California': '8',
         'Colorado': '9',
         'Connecticut': '10',
         'Delaware': '11',
         'Florida': '12',
         'Georgia': '13',
         'Hawaii': '14',
         'Idaho': '15',
         'Illinois': '16',
         'Indiana': '17',
         'Iowa': '18',
         'Kansas': '19',
         'Kentucky': '20',
         'Louisiana': '21',
         'Maine': '22',
         'Maryland': '23',
         'Massachusetts': '24',
         'Michigan': '25',
         'Minnesota': '26',
         'Mississippi': '27',
         'Missouri': '28',
         'Montana': '29',
         'Nebraska': '30',
         'Nevada': '31',
         'New Hampshire': '32',
         'New Jersey': '33',
         'New Mexico': '34',
         'New York': '35',
         'North Carolina': '36',
         'North Dakota': '37',
         'Ohio': '38',
         'Oklahoma': '39',
         'Oregon': '40',
         'Pennsylvania': '41',
         'Puerto Rico': '42',
         'Rhode Island': '43',
         'South Carolina': '44',
         'South Dakota': '45',
         'Tennessee': '46',
         'Texas': '47',
         'Utah': '48',
         'Vermont': '49',
         'Virgina': '50',
         'Washington': '51',
         'Washington D.C.': '52',
         'West Virginia': '53',
         'Wisconsin': '54',
         'Wyoming': '55',

      }
      key_return = d[pay_city]
      # print(key_return)
      xpath = '//*[@id="input_region-list' + key_return + '"]'
      STATE_DICTIONARY = (By.XPATH, xpath)
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(STATE)).click()
      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(STATE_DICTIONARY)).click()

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      ZIP = (By.XPATH, '//*[@id="postal_code"]')
      pay_zip = data[i][11]
      type_out(pay_zip, ZIP)

      add_time = random.randint(4, 8)
      add_time_two = random.randint(4, 6)
      time.sleep(0.02 + add_time / 30 + add_time_two / 30)
      SAVE = (By.XPATH, '//*[@id="pidlddc-button-saveButton"]')
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SAVE)).click()

      time.sleep(10)

      driver.get('https://account.microsoft.com/billing/addresses?ref=storeuhf#/')
      time.sleep(4)

      SETADDY = (By.XPATH,
                 '//*[@id="billing-app-host"]/div/ui-view/div[1]/div[1]/div[2]/div[1]/div[2]/section/div/div/div/section/div[2]/div/div/div/a')
      WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SETADDY)).click()
      time.sleep(3)
      driver.quit()
      print("Finished inserting billing to " + email + "...")
      print(
         "                                                                                                         ")
      print(
         "---------------------------------------------------------------------------------------------------------")
      i += 1

menu()


