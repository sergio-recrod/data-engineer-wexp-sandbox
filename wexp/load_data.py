import duckdb
import logging

from wexp.logger import setup_logger

logger = setup_logger(
    "ingestion", level=logging.INFO, file_name="logs.txt"
    )

# this could be done differently, so if a single table fails
# the rest can continue
# each duckdb.sql can be wrapped in a try-except statement,
# and failure of a table can return some clear message without
# interrupting the whole data loading
def load_data(logger=logger):
    logger.info("Started ingestion")
    logger.info("Table Countries")
    try:
        duckdb.sql("""
        create table Countries(
            Id     int primary key
            ,Name   varchar
        );

        copy Countries
        from 'wexp/data/Countries.csv'
        (auto_detect true)
        """)
        logger.info("Table Countries ingested successfully")
    except Exception as e:
        logger.error(
            f"Table Countries failed to ingest with error:\n{e}"
        )

    logger.info("Table Years")
    try:
        duckdb.sql("""
        create table Years(
            Id     int primary key
            ,Year   int
        );

        copy Years
        from 'wexp/data/Years.csv'
        (auto_detect true)
        """)
        logger.info("Table Years ingested successfully")
    except Exception as e:
        logger.error(
            f"Table Years failed to ingest with error:\n{e}"
        )
    # is this table needed? GDP growth could be a column in the Countries
    # table, as it seems to be unique for each country
    # a different matter would be if we had a time series, but we would need to add
    # a year column to the table
    # potentially we could then filter to get the max year for each country
    # actually this table doesn't meet 3NF and it can lead to inconsistencies
    # (e.g. there could be more than one value for each country)
    logger.info("Table GdpGrowthRates")
    try:
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
        logger.info("Table GdpGrowthRates ingested successfully")
    except Exception as e:
        logger.error(
            f"Table GdpGrowthRates failed to ingest with error:\n{e}"
        )

    logger.info("Table WhiskeyTypes")
    try:
        duckdb.sql("""
        create table WhiskeyTypes (
            Id         int primary key
            ,Type       varchar(32)
        );

        copy WhiskeyTypes 
        from 'wexp/data/WhiskeyTypes.csv'
        (auto_detect true);
        """)
        logger.info("Table WhiskeyTypes ingested successfully")
    except Exception as e:
        logger.error(
            f"Table WhiskeyTypes failed to ingest with error:\n{e}"
        )

    # this table has some duplicate rows in the data table
    # i.e. australia has several rows with exports for grain
    # is this an error, is there missing data (e.g. year),
    # does it have to be aggregated before reporting
    # or is there a valid reason for this?
    # if error, some data validation could be included before
    # ingesting to flag
    # otherwise they should be aggregated on report
    logger.info("Table WhiskeyExports")
    try:
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
        logger.info("Table WhiskeyExports ingested successfully")
    except Exception as e:
        logger.error(
            f"Table WhiskeyExports failed to ingest with error:\n{e}"
        )


    # e.g. check duplicates in facts table
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
    if len(results) > 0:
        logger.warning(
            f"{len(results)} duplicates found in table WhiskeyExports"
        )

    logger.info("Finished ingestion.")
