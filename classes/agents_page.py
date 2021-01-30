import re
from classes.page import Page
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from unidecode import unidecode

class AgentsPage(Page):
    def __init__(self, url, agent_arr):
        Page.__init__(self, url)
        self._agent_arr = agent_arr

    def scrape(self):
        try:
            if self.isNot404():
                agents = self._driver.find_elements_by_css_selector(".seller-contact")
                for agent in agents:
                    title = agent.find_element_by_css_selector("a.link.ng-binding")
                    name = title.text
                    try:
                        ic = agent.find_element_by_css_selector(".contact-item[ng-if='data.brokerIco'] .value").text
                    except NoSuchElementException:
                        ic_replacement = name.replace(' ', "-").replace(',','').replace('.','')
                        # remove accents
                        ic = unidecode(ic_replacement)
                        ic = ic.lower()
                    self._agent_arr.append({
                        'ic': ic,
                        'name': name,
                        'estates_count': 0 #todo
                    })

                if not re.match(".*strana=[0-9]*",  self._url):
                    pagination_elements = Page._driver.find_elements_by_css_selector(".numero.ng-binding")
                    if len(pagination_elements) > 0:
                        delimiter = int(pagination_elements[0].text.split('–')[1])
                        total = int(pagination_elements[1].text.replace(" ", ""))
                        num_pages = int(total/delimiter)+1
                        
                        for p in range(2,num_pages+1):
                            Page._stack.append(AgentsPage(self._url+"?strana="+str(p), self._agent_arr))
        
        except NoSuchElementException:
            print("Element not found!")
        except TimeoutException:
            print("Loading took too much time!")