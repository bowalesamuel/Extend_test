import os
import scrapy
import pandas as pd
from ..items import VerifynamesItem

df = pd.read_csv("./Loan_applicants.csv")
# n = 10
dfa = df.iloc[:,:].copy()
company_house_number = dfa.ApplicantCompanyHouseNumber.str.upper().tolist()
numbers = []
for i in company_house_number:
    v = str(i)
    if len(v) == 7:
        val = "0" + v
    else:
        val = v
    numbers.append(val)
application_id = df.ApplicationID.astype('str').tolist()
data = df.values
directors = df.ContactName
column_names = df.columns
link_url = "https://beta.companieshouse.gov.uk/company/{}/officers"



class EmployeeCheckSpider(scrapy.Spider):
    name = 'employee_check'
    allowed_domains = ['api.company-information.service.gov.uk']
    start_urls = [link_url.format(i) for i in numbers]

    def start_requests(self):
       for u, id, number,name,individual in zip(self.start_urls, application_id, numbers, directors,data):
        id = str(id)
        number = str(number)
        value = list(individual)
        contact = name

        yield scrapy.Request(u, callback = self.parse, 
        errback = self.errback_httpbin, 
        dont_filter=True,
        meta={'application_id':id, 'company_house_number':number, 'value':value, 'contact':contact})

    def errback_httpbin(self, failure): 
        # logs failures 
        request = failure.request 
        self.logger.error(repr(failure))
        print(request)

    
    def parse(self, response):
        print(os.getcwd())
        print(response.css(".heading-xlarge::text").get())
        print(response.xpath("//p[@id='company-number']/strong//text()").get())
        print(response.css("h2#company-appointments::text").get())
        print(response.xpath("//h2[@class='heading-medium']/text()").get())
        print(response.xpath("//*[text()[contains(.,'resignations')]]/text()").get())
        print(response.css(".appointment-4::text").get())
        print(response.css(".appointment-4::text").get() == None)
        print(type(response.css(".appointment-4::text").get()))
        r = 1
        end = True
        
        while end == True:
            end_check = response.css(".appointment-{}::text".format(r))
            if end_check == []:
                break

            officer_name_2 = response.xpath("//span[@id='officer-name-{}']/a/text()".format(r)).get().strip().upper()
            name_check = 0
            scraped = False
            contact_name_split = str(response.meta['contact']).replace("\xa0", "").upper().split(" ")
            for name in contact_name_split:
                if name in officer_name_2:
                    name_check+=1
                pass
            if name_check > 1:
                items = self.parse_found_data(response=response, r=r)
                scraped = True
                yield items
                break
                
            
            r+=1

        if scraped == False:
            items = self.parse_not_found_data(response=response)
            yield items
        pass


    def parse_found_data(self, response, r) -> VerifynamesItem:
        items = VerifynamesItem()
        company_name = response.css("p.heading-xlarge::text").get() #

        officer_name_2 = response.xpath("//span[@id='officer-name-{}']/a/text()".format(r)).get() #

        dob = response.css("#officer-date-of-birth-{}::text".format(r)).get() #
        
        officer_status = response.css("#officer-status-tag-{}::text".format(r)).get() #
        
        officer_position = response.css("#officer-role-{}::text".format(r)).get() #
        
        appointed_on = response.css("#officer-appointed-on-{}::text".format(r)).get() #
        
        nationality = response.css("#officer-nationality-{}::text".format(r)).get() #
        
        occupation = response.css("#officer-occupation-{}::text".format(r)).get() #
        
        residence_country = response.css("#officer-country-of-residence-{}::text".format(r)).get() #
        
        officer_address = response.css("#officer-address-value-{}::text".format(r)).get()


        items['company_name'] = company_name
        items['officer_name'] = officer_name_2
        try:
            items['dob'] = dob.replace("\n", "").strip()
        except:
            items['dob'] = dob
        try:
            items['officer_position'] = officer_position.replace("\n", "").strip()
        except:
            items['officer_position'] = officer_position
        try:
            items['appointed_on'] = appointed_on.replace("\n", "").strip()
        except:
            items['appointed_on'] = appointed_on
        try:
            items['officer_address'] = officer_address.replace("\n", "").strip()
        except:
            items['officer_address'] = officer_address
        try:
            items['nationality'] = nationality.replace("\n", "").strip()
        except:
            items['nationality'] = nationality
        try:
            items['occupation'] = occupation.replace("\n", "").strip()
        except:
            items['occupation'] = occupation
        try:
            items['residence_country'] = residence_country.replace("\n", "").strip()
        except:
            items['residence_country'] = residence_country

        items['officer_status'] = officer_status
        items['url'] = response.request.url
        items['application_id'] = response.meta['application_id']
        items['company_house_number'] = response.meta['company_house_number']

        for v,i in enumerate(column_names):
            if i != "Project number":
                items[i] = list(response.meta['value'])[v]
            else:
                items['Project_number'] = list(response.meta['value'])[v]
            pass

        
        return items

    def parse_not_found_data(self, response) -> VerifynamesItem:
        items = VerifynamesItem()
        items['company_name'] = ""
        items['officer_name'] = ''
        items['dob'] = "2023"
        items['officer_status'] = ""
        items['officer_position'] = ""
        items['appointed_on'] = ""
        items['officer_address'] = ""
        items['nationality'] = ""
        items['occupation'] = ""
        items['residence_country'] = ""
        items['url'] = response.request.url
        items['application_id'] = response.meta['application_id']
        items['company_house_number'] = response.meta['company_house_number']

        for v,i in enumerate(column_names):
            if i != "Project number":
                items[i] = list(response.meta['value'])[v]
            else:
                items['Project_number'] = list(response.meta['value'])[v]
            pass

        
        return items
