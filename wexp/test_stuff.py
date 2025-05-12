from wexp.load_data import load_data
import duckdb
import pandas as pd

load_data()

# this returns several rows for the same country and type
# indicating duplicates in the data table
def get_top_types_per_country():
    con = duckdb.connect(":default:")
    results = con.execute("""
        select 
             c.Name as CountryName
            ,wt.Type as WhiskeyType
            ,we.Value as Value 
        from Countries c
        inner join WhiskeyExports we 
            on c.Id = we.CountryId
        inner join WhiskeyTypes wt
            on we.WhiskeyType = wt.Id
        order by c.Name, wt.Type 
    """).fetchall()

    return results

print(
    pd.DataFrame(
        get_top_types_per_country(),
        columns=["country", "type", "export"]
    ).sort_values(["country", "type", "export"])
)