import numpy as np
import pandas as pd
import db.db_functions as db

# display prices of land from state and region in dataframe
def prices():
    price_list = []
    size_list = []

    state = str(input('What state would you like to see prices from? '))
    
    print()
    print("{} regions: {}".format(state, db.region_search(state)))
    print()

    region = str(input('What region in {}? '.format(state)))

    # get land data from parameters
    land_data = db.land_search(state, region)

    # get prices for mean
    for i in land_data:
        # replace $ and , in price field
        price = i['price'].replace('$', '', 1)
        size = float(i['size'].replace(' acres', '', 1))
        try:
            price = int(price.replace(',', '', 3))
        # skip values of 'Auction'
        except ValueError:
            continue
        
        size_list.append(size)
        price_list.append(price)
    
    # get mean price
    mean_price = round(sum(price_list) / len(price_list))
    mean_size = round(sum(size_list) / len(size_list))

    # print data with frame, exclude id column
    df = pd.DataFrame(land_data).drop(columns='_id')
    print()
    print(df)
    print()
    print('Mean Land Price: ${}     Mean Land Size: {} acres'.format(mean_price, mean_size))
    print()

