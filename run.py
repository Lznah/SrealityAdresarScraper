import json
import time
from datetime import date
from classes.page import Page
from classes.adresar_page import AdresarPage

curr_time = str(int(time.time()))
print("#Started webscrape on: "+date.today().strftime("%B %d, %Y")+" - file: "+curr_time+".json")
Page.addPage(AdresarPage("https://www.sreality.cz/adresar?strana=1"))
Page.run()
# f = open("/root/statistiky/data/"+curr_time+".json", "w")
f = open("./"+curr_time+".json", "w")
f.write(json.dumps(Page.getCompanies()))
f.close()
