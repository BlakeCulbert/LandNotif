from selenium import webdriver
import db.db_functions as db
import pandas as pd

# Get parameters on land
def get_query():
    state = str(input("What state are you looking for land in? "))

    # print regions from state
    print()
    print("{} regions: {}".format(state, db.region_search(state)))
    print()

    region = str(input("What region in " + state + "? "))
    min_acres = int(input("What is the minimum amount of acres? "))
    max_price = int(input("What is the maximum price? "))
    email = str(input("What is your email address? "))

    land_query = {
        'state' : state,
        'region' : region,
        'min_acres' : min_acres,
        'max_price' : max_price,
        'email': email
    }

    db.insert_query(land_query)

# Check queries for matches
def check_query():
    # get states and corresponding regions from db
    land_query = db.query_search()

    size_list = []
    price_list = []

    # loop through queries, check against scraped landData
    for i in land_query:
        # get scraped data that fits parameters
        land_data = list(db.land_search(i['state'], i['region']))
        df2 = pd.DataFrame(land_data)
        print(df2)

        for x in land_data:
            # replace $ and , in price field
            price = x['price'].replace('$', '', 1)
            size = float(x['size'].replace(' acres', '', 1))
            try:
                price = int(price.replace(',', '', 3))
            # skip values of 'Auction'
            except ValueError:
                continue
            
            size_list.append(size)
            price_list.append(price)

            check = True
            while check:
                if i['price'] >= x['price'] and i['size'] >= x['size']:
                    print('MATCH: {} {}'.format(x['price'], x['size']))
                    check = False

check_query()

# Scrape landwatch newest listings
def get_land_data():
    # sample size of states
    states = ['alabama', 'arizona', 'alaska', 'arkansas', 'california', 'colorado']
    LISTING = "d99b8"
    TEXT = "_78864"
    DRIVER_PATH = 'C:/Users/User/Desktop/LandScrape/driver/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    for state in states:
        regions = db.region_search(state)
        for region in regions:
            driver.get('https://landwatch.com/{}-land-for-sale/{}-region/sort-newest'.format(state, region))
            listings = driver.find_elements_by_class_name(LISTING)
            for listing in listings:
                if driver.title == "Landwatch / 404":
                    print("Incorrect Parameters")

                page_text = listing.find_element_by_class_name(TEXT).find_elements_by_tag_name('div')[:2]

                land_data = {
                    'state': state,
                    'region': region,
                    'price': page_text[0].text,
                    'size': page_text[-1].text.split(' - ')[0]
                }
            
                db.insert_land_data(land_data)

            


    
