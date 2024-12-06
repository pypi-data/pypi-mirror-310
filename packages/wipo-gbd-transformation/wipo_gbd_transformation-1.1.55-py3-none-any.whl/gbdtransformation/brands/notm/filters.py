import re

def translate_kind(kind):
    if not kind: return ['Individual']

    if kind == 'Individual mark': return ['Individual']
    if kind == 'Collective mark': return ['Collective']

    raise Exception('kind "%s" is not mapped.' % kind)

def translate_status(status):
    if not status: return 'Ended'

    if status in ['Registered',
                  'Granted']: 
        return 'Registered'

    if status in ['Pending']:
        return 'Pending'

    if status in ['Refused',
                  'Shelved',
                  'Finally shelved',
                  'Ceased',
                  'Ceased/cancelled',
                  'Withdrawn']:
        return 'Ended'

    #return 'Unknown'
    raise Exception('Status "%s" unmapped' % status)

def translate_feature(feature):
    """translation of mark feature"""
    if not feature: return 'Undefined'
    feature = feature.upper()
    if feature == 'COMBINED/FIGURATIVE MARK': return 'Combined'
    if feature == 'WORD MARK': return 'Word'
    if feature == '3D-MARK': return "Three dimensional"

    #return 'Unknown'

    # raise Exception to recognize unmapped values
    raise Exception('Feature "%s" unmapped' % feature)

def get_local_text(node):
    if "$" in node:
        return node["$"]

def get_local_texts(nodes):
    text = ""
    start = True
    for node in nodes:
        if "$" in node:
            if start:
                start = False
            else:
                text += ", "
            text += node["$"]
    return text

"""
def get_registration_nb(trademark, tmstatus):
    if trademark.RegistrationNumber:
        return trademark.RegistrationNumber

    # default registration number to application number
    # in case none is provided
    if tmstatus in ['Registered', 'Expired']:
        return trademark.ApplicationNumber.ApplicationNumberText
"""

def get_full_address(postalStructuredAddress):
    result = ""
    if "addressLineText" in postalStructuredAddress:
        for addressLineText in postalStructuredAddress["addressLineText"]:
            """
            if hasattr(addressLineText, '__value'):
                if len(result) > 0:
                    result += ", "
                result += addressLineText.__value
            """
    if "cityName" in postalStructuredAddress:
        if len(result) > 0:
            result += ", "
        result += postalStructuredAddress["cityName"]
    if "countryCode" in postalStructuredAddress:
        result += ", " + postalStructuredAddress["countryCode"]
    if "postalCode" in postalStructuredAddress:
        result += " " + postalStructuredAddress["postalCode"]
    if len(result) == 0:
        return
    else: 
        return result.strip()

"""
def select_priority_date(priority):
    if priority == None:
        return None
    if "PriorityApplicationFilingDate" in priority:
        return priority["PriorityApplicationFilingDate"]
    elif "PriorityRegistrationDate" in priority:
        return priority["PriorityRegistrationDate"]
    else:
        return None

def clean_verbal_element(element_text):
    if element_text == None:
        return None
    element_text = element_text.replace("((fig.))", "")
    return element_text.strip()
"""

def local_guess_language(content):    
    if content == None:
        return None
    from langdetect import detect
    return detect(content)
