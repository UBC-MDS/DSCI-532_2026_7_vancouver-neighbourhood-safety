import pandas as pd


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
    
    
def data_preprocess(df):
    """
    Preprocesses the input DataFrame by:
    - Filling missing values in 'NEIGHBOURHOOD' with 'Not Specified'
    - Creating a new column 'MONTH_NAME' from the 'MONTH' column
    - Creating a new column 'TIME_OF_DAY' based on the 'HOUR' column
    - Renaming 'Central Business District' to 'Downtown' in the 'NEIGHBOURHOOD' column
    """
    
    # fill missing values in Neighbourhood with Not Specified
    df['NEIGHBOURHOOD'] = df['NEIGHBOURHOOD'].fillna('Not Specified')

    # create MONTH_NAME column
    df['MONTH_NAME'] = pd.to_datetime(pd.to_numeric(df['MONTH'], errors='coerce'), format='%m', errors='coerce').dt.month_name()

    # apply time_of_day function to create column 'TIME_OF_DAY'
    df['TIME_OF_DAY'] = df['HOUR'].apply(time_of_day)
    
    # rename Central Business District to Downtown
    df['NEIGHBOURHOOD'] = df['NEIGHBOURHOOD'].replace("Central Business District", "Downtown")

    
    return df