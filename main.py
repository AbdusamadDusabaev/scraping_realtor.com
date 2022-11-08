import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv

cities = ["wilmington_de", "dover_de", "newark_de", "milford_de", "middletown_de", "bear_de", "glasgow_de",
          "hockessin_de", "brookside_de", "smyrna_de", "pike-creek-valley_de", "claymont_de", "wilmington-manor_de",
          "seaford_de", "north-star_de", "georgetown_de", "millsboro_de", "pike-creek_de", "edgemoor_de",
          "elsmere_de", "new-castle_de", "camden_de", "rising-sun-lebanon_de", "laurel_de", "clayton_de",
          "highland-acres_de", "harrington_de", "dover-base-housing_de", "milton_de", "lewes_de", "selbyville_de",
          "long-neck_de", "townsend_de", "ocean-view_de", "bridgeville_de", "riverview_de", "greenville_de",
          "woodside-east_de", "delmar_de", "cheswold_de", "millville_de", "delaware-city_de", "kent-acres_de",
          "wyoming_de", "felton_de", "blades_de", "bellefonte_de", "rodney-village_de", "rehoboth-beach_de",
          "frederica_de", "st.-georges_de", "greenwood_de", "bethany-beach_de", "dagsboro_de", "newport_de",
          "frankford_de", "lincoln_de", "ellendale_de", "south-bethany_de", "arden_de", "houston_de", "dewey-beach_de",
          "odessa_de", "fenwick-island_de", "port-penn_de", "ardentown_de", "bethel_de", "bowers_de", "kenton_de",
          "little-creek_de", "woodside_de", "leipsic_de", "henlopen-acres_de", "viola_de", "farmington_de", "hartly_de",
          "ardencroft_de"]
urls = list()
headers = {"user-agent": UserAgent().chrome}
domain = "https://www.realtor.com"
file_name = "realtors.csv"
fields = ["Full Name", "Phone", "URL", "Company"]
with open(file_name, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(fields)

for city in cities:
    url = f"https://www.realtor.com/realestateagents/{city}"
    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionResetError:
        try:
            response = requests.get(url=url, headers=headers)
        except ConnectionResetError:
            continue
    bs_object = BeautifulSoup(response.content, "lxml")
    pages = bs_object.find_all(name="a", class_="item btn")
    last_page = pages[-2]["href"].split("-")[-1]
    for index in range(1, int(last_page) + 1):
        url = f"https://www.realtor.com/realestateagents/{city}/pg-{index}"
        try:
            response = requests.get(url=url, headers=headers)
        except ConnectionResetError:
            try:
                response = requests.get(url=url, headers=headers)
            except ConnectionResetError:
                continue
        bs_object = BeautifulSoup(response.content, "lxml")
        realtors_block = bs_object.find(name="div", class_="jsx-2317458496 cardWrapper")
        if realtors_block is not None:
            realtors_list = realtors_block.find_all(name="div", class_="jsx-2317458496")
            for realtor in realtors_list:
                link = domain + realtor.a["href"]
                if link not in urls:
                    urls.append(link)
                    full_name = realtor.find(name="div", class_="jsx-3970352998 agent-list-card-title-text clearfix").a.text.strip()
                    full_name = full_name.split(",")[0]
                    company = realtor.find(name="div", class_="jsx-3970352998 agent-group text-semibold ellipsis").text.strip()
                    phone = realtor.find(name="div", class_="jsx-3970352998 agent-phone hidden-xs hidden-xxs")
                    if phone is None:
                        phone = "Undefined"
                    else:
                        phone = f"+1 {phone.text.strip()}"
                    result = [full_name, phone, link, company]
                    with open(file_name, "a", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(result)
