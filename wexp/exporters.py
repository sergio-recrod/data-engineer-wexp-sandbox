import duckdb


class Export:
    def __init__(self, whiskey_type, value):
        self.whiskey_type = whiskey_type
        self.value = value

    def __str__(self):
        return f"{self.whiskey_type} worth £{self.value}m"


class Country:
    def __init__(self, record):
        self.Id = record[0]
        self.Name = record[1]
        self.GdpGrowthRate = record[2]
        self.Year = record[3]
        self.exports = {}

    def __str__(self):
        return f"{self.Name} (GDP Growth Rate: {self.GdpGrowthRate}%, year: {self.Year})"  # added year to print

    def add(self, export):
        if export.whiskey_type not in self.exports.keys():
            self.exports[export.whiskey_type] = Export(export.whiskey_type, 0)
        self.exports[export.whiskey_type].value += export.value


def get_country_by_id(id):
    con = duckdb.connect(":default:")
    return Country(
        con.execute("""
        select c.Id, c.Name, gdp.Value, gdp.Year
        from Countries c
        inner join (
            select a.Id, a.CountryId, b.YearId, a.Value, y.Year
            from GdpGrowthRates as a
            inner join Years y
                on a.YearId = y.Id
            inner join (
                select CountryId, max(YearId) YearId
                from GdpGrowthRates
                group by CountryId
            ) b
                on a.YearId = b.YearId
        ) gdp
            on c.Id = gpd.CountryId
        where c.Id = ?
    """,
            [id]
        ).fetchone()
    )


def get_country_by_name(name):
    con = duckdb.connect(":default:")
    return Country(
        con.execute("""
        select c.Id, c.Name, gdp.Value, gdp.Year
        from Countries c
        inner join (
            select a.Id, a.CountryId, b.YearId, a.Value, y.Year
            from GdpGrowthRates as a
            inner join Years y
                on a.YearId = y.Id
            inner join (
                select CountryId, max(YearId) YearId
                from GdpGrowthRates
                group by CountryId
            ) b
                on a.YearId = b.YearId
        ) gdp
            on c.Id = gdp.CountryId
        where c.Name = ?
    """,
            [name],
        ).fetchone()
    )


def get_countries():
    con = duckdb.connect(":default:")
    results = con.execute("""
        select distinct c.Id, c.Name, gdp.Value, gdp.Year
        from Countries c
        inner join (
            select a.Id, a.CountryId, b.YearId, a.Value, y.Year
            from GdpGrowthRates as a
            inner join Years y
                on a.YearId = y.Id
            inner join (
                select CountryId, max(YearId) YearId
                from GdpGrowthRates
                group by CountryId
            ) b
                on a.YearId = b.YearId
        ) gdp
            on c.Id = gdp.CountryId
        inner join WhiskeyExports we 
            on c.Id = we.CountryId
    """).fetchall()

    return (Country(r) for r in results)


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

    countries = {}

    for record in results.fetchall():
        if record[0] not in countries.keys():
            countries[record[0]] = get_country_by_name(record[0])

        countries[record[0]].add(Export(record[1], record[2]))

    return countries
