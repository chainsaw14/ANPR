import pandas as pd
from difflib import get_close_matches

def store():
    data = pd.read_csv('.\\data\\test.csv')

    # Find the row with the highest license_number_score for each car_id
    max_score_rows = data.loc[data.groupby('car_id')['license_number_score'].idxmax()]
    print(max_score_rows)
    existing_data = pd.read_csv('.\\data\\data.csv')
    print(existing_data)
    updated_data = pd.concat([existing_data, max_score_rows], ignore_index=True)
    # Now, let's save this data to a new CSV file named final.csv
    #updated_data.to_csv('.\\data\\final.csv', index=False)
    print(updated_data)
    # Fix state codes in the final.csv file
    updated_data = fix_state_code(max_score_rows)
    updated_data.to_csv('.\\data\\final.csv', mode="a", index=False, header= False)


def fix_state_code(data):
    # Define a dictionary to map fumbled state codes to correct ones
    state_code_correction = {
        'TM': 'TN',
        'HH': 'MH',
        'NH': 'MH',  # Example correction: 'NH' should be mapped to 'MH'
        'DJ': 'DL',  # Delhi
        'BR': 'HR',  # Haryana
        'RJ': 'RJ',  # Rajasthan (no change)
        # Add more corrections as needed
    }

    # Iterate through each row of the DataFrame
    for index, row in data.iterrows():
        license_number = str(row['license_number'])
        state_code = license_number[:2]

        # Check if the state code needs correction
        if state_code in state_code_correction:
            corrected_state_code = state_code_correction[state_code]
            corrected_license_number = corrected_state_code + license_number[2:]

            # Update the DataFrame with the corrected license number
            data.at[index, 'license_number'] = corrected_license_number

    return data

