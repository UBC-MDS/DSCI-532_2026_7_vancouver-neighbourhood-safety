def resolve_filter(values):
        "Helper function to convert 'All' selections to None for easier filtering logic"
        if not values or "All" in values:
            return None
        if isinstance(values, str):
            return [values]
        return values

def get_filtered_data(df, filter_nb=None, filter_crime=None, filter_month=None, filter_time=None):
        """Helper function to apply selected filters to the vancouver neighbourhood data 
        based on which filters are enabled"""
        if filter_nb is not None:
            df = df[df["NEIGHBOURHOOD"].isin(filter_nb)]
                
        if filter_crime is not None:
            df = df[df["TYPE"].isin(filter_crime)]
                
        if filter_month is not None:
            df = df[df["MONTH_NAME"].isin(filter_month)]
                
        if filter_time is not None:
            df = df[df["TIME_OF_DAY"].isin(filter_time)]
                
        return df