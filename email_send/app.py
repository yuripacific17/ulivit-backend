# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 08:05:48 2020

@author: sherangagamwasam
"""

from email_send import mailchimp_python_function as mpf
from email_send import newsletter_template

# =============================================================================
# audience creation
# =============================================================================

audience_creation_dictionary = {
    "audience_name" : "testAudience",
    "company" : "jky769038@gmail.com",
    "address1" : "10711 Saskachewan Dr NW",
    "city" :  "Edmonton",
    "state" : "Alberta",
    "zip_code" : "T6E4S4",
    "country" : "Canada", # FOR SRI LANKA : USE LK
    "from_name" : "menju",
    "from_email" : "jky769038@gmail.com",
    "language" : "en",
}    
'''    
audience_creation = mpf.audience_creation_function(audience_creation_dictionary)
'''
# =============================================================================
# add members to the existing audience 
# =============================================================================
'''
audience_id = audience_creation['id']
'''
# add the email list here
email_list = ['lht66823@gmail.com',
              'jaydenliaomengju@gmail.com']
'''
mpf.add_members_to_audience_function(
    audience_id = audience_creation['id'],
    email_list = email_list)
'''
# =============================================================================
# campaign creation
# =============================================================================

campaign_name = 'Test Campaign'
from_name = 'Semicolon'
reply_to = 'jky769038@gmail.com' # test1@gmail.com
'''
campaign = mpf.campaign_creation_function(campaign_name=campaign_name,
                                      audience_id=audience_creation['id'],
                                      from_name=from_name,
                                      reply_to=reply_to)
'''
# =============================================================================
# news letter tempates creation
# =============================================================================

html_code = newsletter_template.html_code           
'''
mpf.customized_template(html_code=html_code, 
                    campaign_id=campaign['id'])
'''
# =============================================================================
# send the mail campaign
# =============================================================================
'''
mpf.send_mail(campaign_id=campaign['id'])
'''
def send_email():
    audience_creation = mpf.audience_creation_function(audience_creation_dictionary)
    mpf.add_members_to_audience_function(
    audience_id = audience_creation['id'],
    email_list = email_list)
    campaign = mpf.campaign_creation_function(campaign_name=campaign_name,
                                      audience_id=audience_creation['id'],
                                      from_name=from_name,
                                      reply_to=reply_to)
    mpf.customized_template(html_code=html_code, 
                    campaign_id=campaign['id'])
    mpf.send_mail(campaign_id=campaign['id'])
           
