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


def get_top_country_per_type():
    con = duckdb.connect(":default:")
    results = con.execute("""
        with cte as (
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
        )
        select cte.WhiskeyType, cte.CountryName, cte.Value
        from cte
        inner join (
            select WhiskeyType, max(Value) as Top
            from cte
            group by WhiskeyType
        ) topt
            on cte.WhiskeyType = topt.WhiskeyType
            and cte.Value = topt.Top
    """).fetchall()

    return results

print(
    pd.DataFrame(
        get_top_country_per_type(),
        columns=["type", "top_country", "export"]
    ).sort_values(["type", "top_country", "export"])
)

def get_duplicates():
    con = duckdb.connect(":default:")
    results = con.execute("""
        select *
        from (
            select CountryId, WhiskeyType, count(Id) as countrows
            from WhiskeyExports
            group by CountryId, WhiskeyType
        )
        where countrows > 1
    """).fetchall()

    return results

dups = pd.DataFrame(
        get_duplicates(),
        columns=["countryid", "whiskeyid", "countrows"]
).sort_values(["countryid", "whiskeyid", "countrows"])

print(f"Dups: {len(dups)}")
print(dups)