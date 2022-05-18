import json

config = str("./config/config.json")
# meta_options = list()
# date_format = ""

with open(config) as f:
    data = json.load(f)
    date_format = data.get("date_format")
    meta_options = data.get("meta_options")
# hey turns out that's way simpler than I thought it would be. 


print(date_format)
print(meta_options)