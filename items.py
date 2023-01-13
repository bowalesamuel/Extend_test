# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class VerifynamesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = Field()
    officer_name = Field()
    dob = Field()
    officer_status = Field()
    officer_position = Field()
    appointed_on = Field()
    nationality = Field()
    occupation = Field()
    residence_country = Field()
    officer_address = Field()
    url = Field()
    company_house_number = Field()
    application_id = Field()

    CompetitionName = ApplicationID = ApplicationTitle = \
    ApplicantOrganisationName = ApplicantOrganisationID = \
    ApplicantCompanyHouseNumber = ApplicantOrganisationSize = ApplicantOrganisationType = IsLeadParticipant = \
    ApplicantOrganisationRegisteredPostcode = \
    ApplicantOrganisationWorkPostcode = ApplicantOrganisationWorkRegion = \
    ApplicantOrganisationWorkCountry = ApplicantOrganisationWorkNuts = \
    ContactName = CostAmount = FundingSought = FundersPanelDate = \
    FundingDecision = Project_number = Field()
    pass
