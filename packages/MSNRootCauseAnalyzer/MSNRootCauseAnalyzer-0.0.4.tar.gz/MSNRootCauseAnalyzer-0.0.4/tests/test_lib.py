# test lib
import holidays


country_code = "JP"  # Country code:https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
year = 2024

country_holidays = holidays.CountryHoliday(country_code, years=year)
for date, name in sorted(country_holidays.items()):
    print(f"Date: {date}, Holiday: {name}")


country_code = "US"  # 选择国家代码
year = 2024

country_holidays = holidays.CountryHoliday(country_code, years=year)
for date, name in sorted(country_holidays.items()):
    print(f"Date: {date}, Holiday: {name}")

country_code = "CN"  # 选择国家代码
year = 2024

country_holidays = holidays.CountryHoliday(country_code, years=year)
for date, name in sorted(country_holidays.items()):
    print(f"Date: {date}, Holiday: {name}")


from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)
# 定义关键词和地理位置
pytrends = TrendReq(hl='en-US', tz=360)   # 时区指定为“中央标准时区”，即“ 360”
# category = 0，它对应于与关键字相关的所有类别
pytrends.build_payload(['weather','Weather'], cat=0, timeframe='2024-01-01 2024-11-10',  gprop='', geo='US-NY')
df = pytrends.interest_over_time()
df.head()