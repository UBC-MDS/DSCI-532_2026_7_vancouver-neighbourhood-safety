import duckdb

# Load main data source as parquet
PARQUET_FILE = "data/processed/van_crime_data_2025.parquet"

con = duckdb.connect()

def resolve_filter(values):
    "Helper function to convert 'All' selections to None "
    "for easier filtering logic"

    if not values or "All" in values:
        return None
    if isinstance(values, str):
        return [values]
    return values


def get_filtered_data(
    filter_nb=None, 
    filter_crime=None, 
    filter_month=None, 
    filter_time=None
):
    """Helper function to apply selected filters to the vancouver 
    neighbourhood data, based on which filters are enabled.
    Parquet file + DuckDB + SQL approach."""

    filter_nb = resolve_filter(filter_nb)
    filter_crime = resolve_filter(filter_crime)
    filter_month = resolve_filter(filter_month)
    filter_time = resolve_filter(filter_time)

    where_clause = []

    if filter_nb:
        ids = ", ".join(f"'{p}'" for p in filter_nb)
        where_clause.append(f"NEIGHBOURHOOD IN ({ids})")
            
    if filter_crime:
        ids = ", ".join(f"'{p}'" for p in filter_crime)
        where_clause.append(f"TYPE IN ({ids})")
            
    if filter_month:
        ids = ", ".join(f"'{p}'" for p in filter_month)
        where_clause.append(f"MONTH_NAME IN ({ids})")
            
    if filter_time:
        ids = ", ".join(f"'{p}'" for p in filter_time)
        where_clause.append(f"TIME_OF_DAY IN ({ids})")

    sql = f"""
        SELECT * 
        FROM read_parquet('{PARQUET_FILE}')
    """

    if where_clause:
        sql += " WHERE " + " AND ".join(where_clause)

    df = con.execute(sql).df()
            
    return df

def get_neighbourhoods():
    
    sql = f"""
        SELECT DISTINCT NEIGHBOURHOOD 
        FROM read_parquet('{PARQUET_FILE}')
        ORDER BY NEIGHBOURHOOD ASC
    """
    
    results = con.execute(sql).df()["NEIGHBOURHOOD"].tolist()
    #print(results)

    return results

def get_crime_types():
    
    sql = f"""
        SELECT DISTINCT TYPE 
        FROM read_parquet('{PARQUET_FILE}')
        ORDER BY TYPE ASC
    """
    
    results = con.execute(sql).df()["TYPE"].tolist()
    #print(results)

    return results