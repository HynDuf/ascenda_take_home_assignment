# Ascenda Take Home Assignment

Ascenda Take-home assignment script written in Python.

-   [About](#about)
-   [How to run](#how-to-run)
-   [Edge cases](#edge-cases)

<a name="about"/>

## About

The script `filter_nearby_offers.py` includes:

-   Function `validate_json_input(input_data)`: Validate the JSON input.
-   Function `filter_nearby_offers(INPUT_FILE, OUTPUT_FILE, checkin_date)`: Read
    the JSON input and output the filtered offer given corresponding parameters.
-   The main program is at the bottom of the script file.

Complexity: O(N) (Scaled linearly with the input data)

<a name="how-to-run"/>

## How to run

Tested on Python 3.11.6, Arch Linux. Should work with other Python 3 versions and OS though.

- Clone the repo (or copy the Python script).
- Prepare input file `input.json` in the same directory with `filter_nearby_offers.py`.
- Run Python command:

    ```bash
    python filter_nearby_offers.py YYYY-MM-DD
    ```
- The filtered offer is outputted to `output.json`.

<a name="edge-cases"/>

## Edge cases

The edge cases are included in directory `edge-cases` and is run with check-in date `2019-12-25`:

- `empty_offers.json`: JSON include an empty offers list.
- `error_offer_empty_merchants.json`: `merchants` is an empty list in any offer.
- `error_wrong_json.json`: not a valid JSON file.
- `error_wrong_type.json`: The `valid_to` is in wrong date format. Additionally, the script also checks:
    - Input file is a valid JSON file.
    - All dates are in correct YYYY-MM-DD format.
    - Offer's `category` exists in the mapping (from `1` to `4`).
    - Offer's `merchants` is a list and have at least one element.
    - Merchants' `distance` is valid integer or float (so can be used to compare).
- `output_0.json`: the filtered offers contains no offer (with `valid_to` only 4 days away from check-in date).
- `output_1.json`: the filtered offers contains only 1 offer (with `valid_to` is exactly 5 days away from check-in date).
