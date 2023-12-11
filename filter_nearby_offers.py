import json
import sys
from datetime import datetime, timedelta

# Define category ID mapping
category_mapping = {
    1: "Restaurant",
    2: "Retail",
    3: "Hotel",
    4: "Activity"
}

def validate_json_input(input_data):
    """
    Validate the input data read from INPUT_FILE, so that function `filter_nearby_offers` can run normally:
        1. Offer's category is valid (i.e. exists in `category_mapping`)
        2. Offer's valid_to is in valid format (YYYY-MM-DD)
        3. Offer's merchants is indeed a list and isn't empty
        4. Every merchant in offer's merchants have valid `distance` (int or float)
    """
    # Iterate through each offer in the input data
    for offer in input_data['offers']:
        # 1. Attempt to get the category from the category mapping
        if offer['category'] not in category_mapping:
            print(f"Error processing offer {offer['id']}: Invalid category {offer['category']} (doesn't exist in category_mapping)")
            sys.exit(1)

        # 2. Attempt to parse the 'valid_to' date to format YYYY-MM-DD
        try:
            valid_to = datetime.strptime(offer['valid_to'], '%Y-%m-%d')
        except (ValueError, KeyError) as e:
            print(f"Error parsing offer {offer['id']}'s `valid_to`: {e}")
            sys.exit(1)

        # 3. Check if 'merchants' is not a list or is an empty list
        if (
            not isinstance(offer.get('merchants'), list) or 
            len(offer['merchants']) == 0
        ):
            print(f"Error processing offer {offer['id']}. `merchants` isn't a list or is an empty list.")
            sys.exit(1)

        # 4. Iterate through each merchant in the 'merchants' list
        for merchant in offer['merchants']:
            # Check if 'distance' is not present or is not a valid float or integer
            if 'distance' not in merchant or not isinstance(merchant['distance'], (int, float)):
                print(f"Error processing offer {offer['id']}. Invalid 'distance' for merchant {merchant.get('id', 'Unknown')}.")
                sys.exit(1)

def filter_nearby_offers(INPUT_FILE, OUTPUT_FILE, checkin_date):
    """
    The filter algorithm structure:
        1. Iterate through valid offer:
            - `category` is in ["Restaurant", "Retail", "Activity"]
            - `valid_to` >= checkin_date + 5 days
        2. For each valid offer, sort the merchants by `distance` and take the closest one
        3. For each category, take only one offer that have the closest merchant
        4. Take maximum 2 offers that have closest merchants among all the categories
    """
    # Load JSON file INPUT_FILE
    try:
        with open(INPUT_FILE) as json_file:
            input_data = json.load(json_file)
        validate_json_input(input_data)
    except (FileNotFoundError, IOError) as e:
        print(f"Error: Unable to read '{INPUT_FILE}'. {e}")
        sys.exit(1)
    except (json.JSONDecodeError) as e:
        print(f"Error: Invalid JSON file '{INPUT_FILE}'.\n{e}")
        sys.exit(1)

    # List of accepted categories
    accepted_categories = ["Restaurant", "Retail", "Activity"]

    # Save maximum one offer in each category
    filtered_offers_of_category = {
        "Restaurant": {},
        "Retail": {},
        "Activity": {}
    }

    for offer in input_data['offers']:
        category = category_mapping.get(offer['category'])
        valid_to = datetime.strptime(offer['valid_to'], '%Y-%m-%d')

        if (
             category in accepted_categories and
             valid_to >= checkin_date + timedelta(days=5)
        ):
            # Iterate through all merchants and select the closest one
            closest_merchant = offer['merchants'][0]
            for merchant in offer['merchants']:
                if closest_merchant['distance'] > merchant['distance']:
                    closest_merchant = merchant

            # Check and update the closest offer of the corresponding category
            # If there is no offer in the category yet
            # Or the current offer is closer than the saved offer
            if (
                len(filtered_offers_of_category[category]) == 0 or 
                filtered_offers_of_category[category]['merchants'][0]['distance'] > closest_merchant['distance']
            ):
                filtered_offers_of_category[category] = {
                    'id': offer['id'],
                    'title': offer['title'],
                    'description': offer['description'],
                    'category': offer['category'],
                    'merchants': [closest_merchant],
                    'valid_to': offer['valid_to']
                }

    # Get the filtered offers to a list
    final_offers = []

    for category, offer_info in filtered_offers_of_category.items():
        if offer_info:
            final_offers.append(offer_info)

    # Sort final offers by distance
    final_offers = sorted(final_offers, key=lambda x: x['merchants'][0]['distance'])

    # Choose maximum 2 offers with closest merchants
    selected_offers = final_offers[:2]

    # Save the selected offers to output.json
    output_data = {'offers': selected_offers}
    with open(OUTPUT_FILE, 'w') as output_file:
        json.dump(output_data, output_file, indent=2)

if __name__ == "__main__":
    # Accept customer check-in date as a command line argument
    if len(sys.argv) != 2:
        print("Incorrect usage! There must be exactly one command line argument!\n")
        print("Usage:\n\tpython filter_nearby_offers.py YYYY-MM-DD")
        print("where YYYY-MM-DD is a valid customer check-in date")
        sys.exit(1)

    # Check if the given check-in date is in the correct format YYYY-MM-DD
    try:
        checkin_date_str = sys.argv[1]
        checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d')
    except ValueError:
        print("Error: Incorrect date format. Please use the format 'YYYY-MM-DD'")
        sys.exit(1)

    # Filter nearby offers with data from INPUT_FILE and output to OUTPUT_FILE
    INPUT_FILE = "input.json"
    OUTPUT_FILE = "output.json"
    filter_nearby_offers(INPUT_FILE, OUTPUT_FILE, checkin_date)
