import json
import time
import os
from datetime import date
from classes.page import Page
from classes.adresar_page import AdresarPage

try:
    data_path = os.environ['SREALITY_SCAPPER_DATAPATH']
    curr_time = str(int(time.time()))
    print("#Started webscrape on: "+date.today().strftime("%B %d, %Y")+" - file: "+curr_time+".json")
    Page.addPage(AdresarPage("https://www.sreality.cz/adresar?strana=1"))
    Page.run()
    f = open(data_path+curr_time+".json", "w")
    f.write(json.dumps(Page.getCompanies()))
    f.close()
except KeyError:
    print('Set SREALITY_SCAPPER_DATAPATH environment variable.')

