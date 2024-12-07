from requests import get
from lxml.etree import HTML
from datetime import datetime, timedelta
import json
import csv
import requests
listas1 =[]
pusl_sar = []

def check_time(a : datetime):
    return  datetime.now() < a

def duino ( f1 : str, t : int):
    pusl_sar.clear()
    listas = []
    laikas_end: datetime = datetime.now() + timedelta(seconds=t)
    #nusiskaitom kiek yra lapu
    response = get("https://www.duino.lt/64-valdikliai")
    text = response.text
    tree = HTML(text)
    puslapiai = tree.xpath(
        "//div[@class = 'top-pagination-content clearfix']/div[@id = 'pagination']/ul[@class = 'pagination']/li/a/@href")
    for pusl in puslapiai:
        pusl_sar.append(pusl)
    pusl_sar.pop(len(puslapiai) - 1)  # suformuotas lapu sarasas
    pusl_sar.append("/64-valdikliai")
    #nuskaitom info is lapo
    for i in pusl_sar:
        if check_time(laikas_end) == True:
            pageURL = i
            print(f"Nuskaitomas puslapis  {pageURL}")
            listas = []
            listas.clear()
            response = get("https://www.duino.lt" + str(pageURL))
            text = response.text
            tree = HTML(text)
            # nuskaitom reikiama info is puslapio"""
            products = tree.xpath("//div[contains(@class, 'right-block')]")
            listas = [
                {'Produktas : ': product.xpath(".//a[contains(@class, 'product-name')]/text()")[0],
                'Kaina : ': product.xpath(".//span[contains(@class, 'price product-price')]/text()")[0].strip().replace("€",                                                                                                            "")
                }
                for product in products
                    ]
            if f1 == ".txt":
                for i in listas:
                    with open("Duino.txt", "a", encoding="utf-8") as irasimas_f:
                        irasimas_f.write(str(i) + "\n")
                        irasimas_f.close()
            elif f1 == ".csv":
                for i in listas:
                    with open('Duino.csv', 'a', encoding='UTF8', newline='')  as irasimas_f:
                        field_names = ['Produktas : ', 'Kaina : ' ]
                        writer = csv.DictWriter(irasimas_f, fieldnames=field_names)
                        writer.writerow(i)

            elif f1 == ".json":
                for i in listas:
                    json_object = json.dumps(i, indent=2)
                    with open("Duino.json", "a", encoding="utf-8") as irasymas_f:
                        irasymas_f.write(json_object)
                        irasymas_f.close()
            else :
                print("Neteisingai pasirinktas formatas")
                print("Galimi formatai: .json arba .txt arba .csv")
        else:
            print("Baigesi skirtas laikas")
            break
    print("Darbas baigtas")



def skonis(f : str, t : int):
    listas = []
    laikas_end: datetime = datetime.now() + timedelta(seconds=t)
    response = get("https://www.skonis-kvapas.lt/kava")
    text = response.text
    tree = HTML(text)
    puslapiai = tree.xpath(
        "//div[@class = 'col-md-6 offset-md-2 pr-0']/ul[@class = 'page-list clearfix text-sm-center']//a[@rel = 'nofollow']/@href")
    for pusl in puslapiai:
        pusl_sar.append(pusl)
    for i in pusl_sar:
        if check_time(laikas_end) == True:
            pageURL = i
            print(f"Nuskaitomas puslapis  {pageURL}")
            listas.clear()
            response = get(pageURL)
            text = response.text
            tree = HTML(text)
            products = tree.xpath("//div[contains(@class, 'products__item  ')]")
            listas = [
                {'Produktas : ': product.xpath(".//h2[contains(@class, 'products__item-title')]/text()")[
                    0].strip().replace("\n", ""),
                 'Kaina : ': product.xpath(".//div[contains(@class, 'products__item-price')]/ins/text()")[
                     0].strip().replace("\xa0", "").replace("€", "")
                 }
                for product in products
            ]

            if f == ".txt":
                for i in listas:
                    with open("Skonis_ir_Kvapas.txt", "a", encoding="utf-8") as irasimas_f:
                        irasimas_f.write(str(i) + "\n")
                        irasimas_f.close()

            elif f == ".csv":
                for i in listas:
                    with open('Skonis_ir_Kvapas.csv', 'a', encoding='UTF8', newline='')  as irasimas_f:
                        field_names = ['Produktas : ', 'Kaina : ' ]
                        writer = csv.DictWriter(irasimas_f, fieldnames=field_names)
                        writer.writerow(i)

            elif f == ".json":
                for i in listas:
                    print("json")
                    json_object = json.dumps(i, indent=2)
                    with open("Skonis_ir_Kvapas.json", "a", encoding="utf-8") as irasymas_f:
                        irasymas_f.write(json_object)
                        irasymas_f.close()
            else:
                print("Neteisingai pasirinktas formatas")
                print("Galimi formatai: .json arba .txt arba .csv")
        else:
            print("Baigesi skirtas laikas")
            break
    print("Darbas baigtas")


def crowl(puslapis : int, formatas : str, laikas : int):
    try:
        match puslapis:
            case 1:
                print(" 1 pasirinkimas")
                print(" Nuskaitoma svetaine Duino.lt")
                duino(formatas,laikas)
            case 2:
                print("2 pasirinkta")
                print(" Nuskaitoma svetaine Skonis ir kvapas.lt")
                skonis(formatas, laikas)
            case _:
                print("Galimas pasirinkimas int 1 arba 2")
                print(" 1 - Duino.lt ")
                print(" 2 - Skonis ir Kvapas.lt ")
    except TypeError:
        print("Neteisingas formatas")
       # print("Darbas sustabdytas")

