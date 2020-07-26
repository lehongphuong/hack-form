import threading

from bs4 import BeautifulSoup as soup
import requests
import time
import json
import urllib3
import codecs
import random
# import database

''' ------------------------------ SETTINGS ------------------------------ '''
# Global settings
base_url = "https://mct.tokyo"  # Don't add a / at the end
# Search settings
# keywords = ["BE@RBRICK BAPE(R) MICKEY MOUSE"]  # Seperate keywords with a comma
# size = "11"
# If a size is sold out, a random size will be chosen instead, as a backup plan
random_size = True
# To avoid a Shopify soft-ban, a delay of 7.5 seconds is recommended if
# starting a task much earlier than release time (minutes before release)
# Otherwise, a 1 second or less delay will be ideal
search_delay = 1
# Checkout settings
email = "khong.minhcong@gmail.com"
fname = "DUCCONG"
lname = "KHONG"
addy1 = "福岡県 太宰府市宰府 １−８−５メリーメイト１−１０９号"
addy2 = ""  # Can be left blank
city = "太宰府"
province = "福岡"
country = "日本"
postal_code = "8180117"
phone = "09082494931"
# card_number = "4297690111419380"  # No spaces
# cardholder = "KHONG DUCCONG"
# exp_m = "09"  # 2 digits
# exp_y = "2023"  # 4 digits
# cvv = "781"  # 3 digits
''' ------------------------------- MODULES ------------------------------- '''

def get_products(session):
    '''
    Gets all the products from a Shopify site.
    '''
    # Download the products
    link = base_url + "/products.json"
    r = session.get(link, verify=False)
    # Load the product data
    products_json = json.loads(r.text)
    products = products_json["products"]
    # Return the products
    return products

def keyword_search(session, products, keywords):
    '''
    Searches through given products from a Shopify site to find the a product
    containing all the defined keywords.
    '''
    # Go through each product
    for product in products:
        # Set a counter to check if all the keywords are found
        keys = 0
        # Go through each keyword
        for keyword in keywords:
            # If the keyword exists in the title
            if(keyword.upper() in product["title"].upper()):
                # Increment the counter
                keys += 1
            # If all the keywords were found
            if(keys == len(keywords)):
                print(keys, len(keywords))
                # Return the product
                return product

def generate_cart_link(session, variant):
    '''
    Generate the add to cart link for a Shopify site given a variant ID.
    '''
    # Create the link to add the product to cart
    link = base_url + "/cart/" + str(variant) + ":1"
    # Return the link
    return link

def get_payment_token(card_number, cardholder, expiry_month, expiry_year, cvv):
    '''
    Given credit card details, the payment token for a Shopify checkout is
    returned.
    '''
    # POST information to get the payment token
    link = "https://elb.deposit.shopifycs.com/sessions"
    payload = {
        "credit_card": {
            "number": card_number,
            "name": cardholder,
            "month": expiry_month,
            "year": expiry_year,
            "verification_value": cvv
        }
    }
    r = requests.post(link, json=payload, verify=False)
    # Extract the payment token
    payment_token = json.loads(r.text)["id"]
    # Return the payment token
    return payment_token

def get_shipping(postal_code, country, province, cookie_jar):
    '''
    Given address details and the cookies of a Shopify checkout session, a shipping option is returned
    '''
    # Get the shipping rate info from the Shopify site
    link = base_url + "//cart/shipping_rates.json?shipping_address[zip]=" + postal_code + "&shipping_address[country]=" + country + "&shipping_address[province]=" + province
    r = session.get(link, cookies=cookie_jar, verify=False)
    # Load the shipping options
    shipping_options = json.loads(r.text)
    # Select the first shipping option
    ship_opt = shipping_options["shipping_rates"][0]["name"].replace(' ', "%20")
    ship_prc = shipping_options["shipping_rates"][0]["price"]
    # Generate the shipping token to submit with checkout
    shipping_option = "shopify-" + ship_opt + "-" + ship_prc
    # Return the shipping option
    return shipping_option

def add_to_cart(session, variant):
    '''
    Given a session and variant ID, the product is added to cart and the
    response is returned.
    '''
    # Add the product to cart
    link = base_url + "/cart/add.js?quantity=1&id=" + variant
    response = session.get(link, verify=False)
    # Return the response
    return response

def submit_customer_info(session, cookie_jar):
    '''
    Given a session and cookies for a Shopify checkout, the customer's info
    is submitted.
    '''
    # Submit the customer info
    payload = {
        "utf8": u"\u2713",
        "_method": "patch",
        "authenticity_token": "",
        "previous_step": "contact_information",
        "step": "shipping_method",
        "checkout[email]": email,
        "checkout[buyer_accepts_marketing]": "0",
        "checkout[shipping_address][first_name]": fname,
        "checkout[shipping_address][last_name]": lname,
        "checkout[shipping_address][company]": "",
        "checkout[shipping_address][address1]": addy1,
        "checkout[shipping_address][address2]": addy2,
        "checkout[shipping_address][city]": city,
        "checkout[shipping_address][country]": country,
        "checkout[shipping_address][province]": province,
        "checkout[shipping_address][zip]": postal_code,
        "checkout[shipping_address][phone]": phone,
        "checkout[remember_me]": "0",
        "checkout[client_details][browser_width]": "1710",
        "checkout[client_details][browser_height]": "1289",
        "checkout[client_details][javascript_enabled]": "1",
        "button": ""
    }
    link = base_url + "//checkout.json"
    response = session.get(link, cookies=cookie_jar, verify=False)
    # Get the checkout URL
    link = response.url
    checkout_link = link
    # POST the data to the checkout URL
    response = session.post(link, cookies=cookie_jar, data=payload, verify=False)
    print("submit_customer_info", response, checkout_link)

    # Return the response and the checkout link
    return (response, checkout_link)
''' ------------------------------- CODE ------------------------------- '''
# Initialize
session = requests.session()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



# card_number = "3574010086639035"  # No spaces ba năm bảy bốn  0100 tám sáu sáu 3 chín không 35
# cardholder = "khong minhcong"
# exp_m = "04"  # 2 digits
# exp_y = "2023"  # 4 digits
# cvv = "491"  # 3 digits

keywords = ["BE@RBRICK 招き猫 銀メッキ 発光"]
keywords = ["BE@RBRICK ANDY WARHOL"]

def booking_tokyo(product, card_number, cardholder, exp_m, exp_y, cvv, id):
    print("phuong start 0 ")
    # Loop until a product containing all the keywords is found
    print('keywords', keywords)
    while (product == None):
        # Grab all the products on the site
        products = get_products(session)
        # Grab the product defined by keywords
        product = keyword_search(session, products, keywords)
        if (product == None):
            time.sleep(search_delay)

    print("phuong 1")
    # Get the variant ID for the size
    variant = str(product["variants"][0]["id"])
    print(variant)

    start = time.time()
    # Get the cart link
    cart_link = generate_cart_link(session, variant)
    print("phuong 2")
    # Add the product to cart
    r = add_to_cart(session, variant)
    # Store the cookies
    cj = r.cookies

    # Get the payment token
    p = get_payment_token(card_number, cardholder, exp_m, exp_y, cvv)
    print("phuong 3")
    # Submit customer info and get the checkout url
    (r, checkout_link) = submit_customer_info(session, cj)
    # Get the shipping info
    ship = get_shipping(postal_code, country, province, cj)
    print("phuong 4")
    # Get the payment gateway ID
    link = checkout_link + "?step=payment_method"
    r = session.get(link, cookies=cj, verify=False)
    bs = soup(r.text, "html.parser")
    div = bs.find("div", {"class": "radio__input"})
    # print(div)
    gateway = ""
    values = str(div.input).split('"')
    for value in values:
        if value.isnumeric():
            gateway = value
            break
    # Submit the payment
    link = checkout_link
    payload = {
        "utf8": u"\u2713",
        "_method": "patch",
        "authenticity_token": "",
        "previous_step": "payment_method",
        "step": "",
        "s": p,
        "checkout[payment_gateway]": gateway,
        "checkout[credit_card][vault]": "false",
        "checkout[different_billing_address]": "true",
        "checkout[billing_address][first_name]": fname,
        "checkout[billing_address][last_name]": lname,
        "checkout[billing_address][address1]": addy1,
        "checkout[billing_address][address2]": addy2,
        "checkout[billing_address][city]": city,
        "checkout[billing_address][country]": country,
        "checkout[billing_address][province]": province,
        "checkout[billing_address][zip]": postal_code,
        "checkout[billing_address][phone]": phone,
        "checkout[shipping_rate][id]": ship,
        "complete": "1",
        "checkout[client_details][browser_width]": str(random.randint(1000, 2000)),
        "checkout[client_details][browser_height]": str(random.randint(1000, 2000)),
        "checkout[client_details][javascript_enabled]": "1",
        "g-recaptcha-repsonse": "",
        "button": ""
        }
    print("phuong 5")
    r = session.post(link, cookies=cj, data=payload, verify=False)
    print("finish", r)
    end = time.time()
    print(end -start)
    print("phuong 6")
    # database.update_status(id)


def booking(card_number, cardholder, exp_m, exp_y, cvv, id):
    product = None
    xxx = threading.Thread(target=booking_tokyo, args=(product, card_number, cardholder, exp_m, exp_y, cvv, id))
    xxx.start()
    xxx.join()





