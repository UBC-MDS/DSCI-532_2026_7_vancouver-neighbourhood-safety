import pandas as pd

def load_data(file_path):
    """
    Loads the dataset from the specified file path.
    """
    df = pd.read_csv(file_path)
    return df

def time_of_day(hour):
    """
    Categorizes the hour of the day into:
    Morning, Afternoon, or Evening/Night.
    """
    if  4 <= hour <= 11:
        return "Morning"
    elif 12 <= hour <= 17:
        return "Afternoon"
    else:
        return "Evening/Night"
    
    
def data_preprocess(file_path):
    """
    Preprocesses the input DataFrame by:
    - Filling missing values in 'NEIGHBOURHOOD' with 'Not Specified'
    - Creating a new column 'MONTH_NAME' from the 'MONTH' column
    - Creating a new column 'TIME_OF_DAY' based on the 'HOUR' column
    - Renaming 'Central Business District' to 'Downtown' in the 'NEIGHBOURHOOD' column
    """
    df = load_data(file_path)
    
    # replace missing NaN value with 'Fairview' in the 'neighbourhood'
    df.loc[(df['HUNDRED_BLOCK'] == "15XX GRANVILLE BRDG") & 
        (df['NEIGHBOURHOOD'].isna()) & (df['X'].notna()) & 
        (df['Y'].notna()), 'NEIGHBOURHOOD'] = 'Fairview'
    
    # fill missing values in Neighbourhood with Not Specified
    df['NEIGHBOURHOOD'] = df['NEIGHBOURHOOD'].fillna('Not Specified')

    # create MONTH_NAME column
    df['MONTH_NAME'] = pd.to_datetime(df['MONTH'], format='%m', errors='coerce').dt.month_name()

    # apply time_of_day function to create column 'TIME_OF_DAY'
    df['TIME_OF_DAY'] = df['HOUR'].apply(time_of_day)
    
    # rename Central Business District to Downtown
    df['NEIGHBOURHOOD'] = df['NEIGHBOURHOOD'].replace("Central Business District", "Downtown")

    df.to_csv('data/processed/processed_vancouver_crime_data_2025.csv', index=False)
    
    return df


if __name__ == "__main__":
    df = data_preprocess('data/raw/crimedata_csv_AllNeighbourhoods_2025.csv')
    print('---Data Preprocessing Completed---')