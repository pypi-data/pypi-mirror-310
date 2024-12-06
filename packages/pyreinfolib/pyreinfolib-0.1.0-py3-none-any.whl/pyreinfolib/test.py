from pyreinfolib import Client
from pyreinfolib.enums import UseDivision, LandTypeCode

c = Client("5d1cf2e03da64b6db532b25f366d8a49")
# res1 = c.get_municipalities(area=13)
# print(res1)

#res2 = c.get_real_estate_prices(year=2024, quarter=5, price_classification="01", city="13109")
# print(res2)

# res3 = c.get_appraisal_reports(year=2024, area="13", division=UseDivision.INDUSTRIAL_LAND)
# print(res3)

res4 = c.get_real_estate_prices_point(
    z=11, x=1819, y=806, period_from=20241, period_to=20241,price_classification="01",
    land_type_code=[
        LandTypeCode.LAND,
        LandTypeCode.FOREST_LAND,
    ]
)
#print(res4)

# res5 = c.get_land_price_public_notices_and_surveys_point(
#     z=13, x=7312, y=3008,year=2020,price_classification="0",use_category_code=[UseDivision.RESIDENTIAL_LAND]
# )
# print(res5)
