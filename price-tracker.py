import requests
from bs4 import BeautifulSoup
import shelve
import os
import urllib
from datetime import datetime
import sys
import glob




def reset():
    for file in glob.glob('price_record' + '*'):
        try:
            os.remove(file)
            print(f"\nRecord is deleted.\n")
        except Exception as e:
            print(f"\nCould not delete: {e}\n")



def notify(api_url,notify_text):
    
   
    requests.get(api_url)

def setup():
    shelve_file = shelve.open("price_record")
    product_link = input('\nProduct url: ').strip()
    shelve_file['product_link'] = product_link


    choice = input("Do you want Telegram notifications when the Flipkart product hits its lowest price since tracking started? Type 'yes' to enable: ")

    if choice == 'yes':
        api_url = input('\nCallMeBot api URL: ')
        notify_text = input('\nNotification text: ')

        shelve_file = shelve.open("price_record")


        parsed_url = urllib.parse.urlparse(api_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        query_params['text'] = [notify_text]
        new_query_string = urllib.parse.urlencode(query_params, doseq=True)
        new_parsed_url = parsed_url._replace(query=new_query_string)

        shelve_file['api_url'] = new_parsed_url.geturl()
        



    if 'product_link' in shelve_file:
        print('\nSetup is done.\n')
    else:
        print('\nSetup failed\n')
        
    shelve_file.close()


def get_current_price(product_link):
    
    try:
        r = requests.get(product_link)
        soup = BeautifulSoup(r.text,'html.parser')

        tag = soup.find('div',class_="Nx9bqj CxhGGd")

        current_price = tag.string.replace("₹", "").replace(",", "").strip()
        return current_price


    except AttributeError:
        print('Could not get the current price.')
        exit(0)

    except requests.exceptions.ConnectionError:
        print('Failed to resolve product link')
        exit(0)

    except requests.exceptions.MissingSchema:
        print('Record not set properly')
        exit(0)

def start():
    shelve_file = shelve.open("price_record")

    try:

        product_link = shelve_file['product_link']
        current_price = get_current_price(product_link)

    except KeyError:
        print("Record is not set.")
        exit(0)




    now = datetime.now()

    if 'lowest' not in shelve_file:
        shelve_file['lowest'] = int(current_price)

    else:
        
        if int(current_price) < shelve_file['lowest']:
            shelve_file['lowest'] = int(current_price)
            notify('new deal')


    date_time = f'{now.strftime("%-I:%M %p").lower()} -- {now.strftime("%d %B %Y")}'

    shelve_file[date_time] = f'₹{current_price}'

    shelve_file.close()


def list_prices():

    shelve_file = shelve.open("price_record")

    print()

    if not shelve_file:
        print('\nRecord is empty\n')
        exit(0)

    for key in shelve_file:

        if key == 'lowest':
            continue
        elif key == 'product_link':
            print('\n')
            print(f"Product URL: {shelve_file[key]}\n")
            continue
        elif key == 'api_url':
            continue    

        print(f"{key}: {shelve_file[key]}")


    shelve_file.close()

def print_options():
    print("""
        Usage: python script.py [option]

        Available options:
      --reset     Resets the price records
      --set       Runs the setup configuration
      --list      Displays the records
      --start     Starts collecting price records
    """)


def check_args():

    if len(sys.argv) < 2:
       print_options() 
       exit(0)


    elif len(sys.argv) > 2:
        print('Progaram will only take 1 argument.')
        exit(0)


    if sys.argv[1] == '--reset':
        reset()
    elif sys.argv[1] == '--set':
        setup()
    elif sys.argv[1] == '--list':
        list_prices()
    elif sys.argv[1] == '--start':
        start()
    else:
        print_options()
        exit(0)


def main():
    check_args()


if __name__ == "__main__":
    main()


