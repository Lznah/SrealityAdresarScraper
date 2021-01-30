import re
from classes.page import Page
from classes.branches_page import BranchesPage
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

class AdresarPage(Page):
    flag = True
    limit = 2

    def scrape(self):
        try:
            if AdresarPage.flag:
                AdresarPage.flag = False
                pagination_elements = Page._driver.find_elements_by_css_selector(".numero.ng-binding")
                if len(pagination_elements) > 0:
                    delimiter = int(pagination_elements[0].text.split('–')[1])
                    total = int(pagination_elements[1].text.replace(" ", ""))
                    num_pages = int(total/delimiter)+1
                    if num_pages > AdresarPage.limit:
                        num_pages = AdresarPage.limit
                    
                    for p in range(2,num_pages+1):
                        Page._stack.append(AdresarPage("https://www.sreality.cz/adresar?strana="+str(p)))
            
            agencies = Page._driver.find_elements_by_css_selector(".texts")
            for agency in agencies:
                title = agency.find_element_by_css_selector("a.link.ng-binding")
                name = title.text
                link = title.get_attribute("href")
                address = agency.find_element_by_css_selector(".address.ng-binding").text
                estates_count = int(agency.find_element_by_css_selector(".estates-cnt.ng-binding .num").text.replace(' ', ''))

                if estates_count != 0:
                    Page._stack.append(BranchesPage(link+"/pobocky"))
                
                id = re.search('\/([0-9]*)$',link).group(1)
                Page._companies[id] = {
                    "name": name,
                    "address": address,
                    "estates_count": estates_count,
                    "branches": []
                }


        except NoSuchElementException:
            print("Element not found!")
        except TimeoutException:
            print("Loading took too much time!")