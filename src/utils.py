import duckdb

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
    params = []  # To bind values to query (for ? notation)

    if filter_nb:
        where_clause.append("NEIGHBOURHOOD IN (?)")
        params.append(filter_nb)
            
    if filter_crime:
        where_clause.append("TYPE IN (?)")
        params.append(filter_crime)
            
    if filter_month:
        where_clause.append("MONTH_NAME IN (?)")
        params.append(filter_month)
            
    if filter_time:
        where_clause.append("TIME_OF_DAY IN (?)")
        params.append(filter_time)

    sql = f"""
        SELECT * 
        FROM read_parquet('{PARQUET_FILE}')
    """

    if where_clause:
        sql += " WHERE " + " AND ".join(where_clause)

    df = con.execute(sql, params).df()
            
    return df