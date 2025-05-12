import duckdb


def load_data():
    duckdb.sql("""
    create table Countries(
        Id     int primary key
        ,Name   varchar
    );

    copy Countries
    from 'wexp/data/Countries.csv'
    (auto_detect true)
    """)

    duckdb.sql("""
    create table Years(
        Id     int primary key
        ,Year   int
    );

    copy Years
    from 'wexp/data/Years.csv'
    (auto_detect true)
    """)

    # is this table needed? GDP growth could be a column in the Countries
    # table, as it seems to be unique for each country
    # a different matter would be if we had a time series, but we would need to add
    # a year column to the table
    # potentially we could then filter to get the max year for each country
    # actually this table doesn't meet 3NF and it can lead to inconsistencies
    # (e.g. there could be more than one value for each country)
    duckdb.sql("""
    create table GdpGrowthRates (
        Id         int primary key
        ,CountryId  int
        ,YearId     int
        ,Value      int
        ,foreign key (YearId) references Years(Id)
        ,foreign key (CountryId) references Countries(Id)
    );

    copy GdpGrowthRates
    from 'wexp/data/GdpGrowthRates.csv'
    (auto_detect true);
    """)

    duckdb.sql("""
    create table WhiskeyTypes (
        Id         int primary key
        ,Type       varchar(32)
    );

    copy WhiskeyTypes 
    from 'wexp/data/WhiskeyTypes.csv'
    (auto_detect true);
    """)

    duckdb.sql("""
    create table WhiskeyExports (
        Id             int primary key
        ,CountryId      int
        ,WhiskeyType    int
        ,Value          int
        ,foreign key (CountryId) references Countries(Id)
        ,foreign key (WhiskeyType) references WhiskeyTypes(Id)
    );

    copy WhiskeyExports 
    from 'wexp/data/WhiskeyExports.csv'
    (auto_detect true);
    """)
