import json
import wikipediaapi
import openai
import os

openai.api_key = os.environ['openai_key']

wiki_wiki = wikipediaapi.Wikipedia('MyWikiBot','en')

def ask_openai(question, page_summary):

    prompt_text = "Answer this question {} based on the following information: {}".format(str(question),str(page_summary))
    #print('The prompt that we gave to ChatGPT was: ',prompt_text,'\n\n')
    answer = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt_text,
        temperature=0.1,
        max_tokens=500)

    response = answer['choices'][0]['text']
    #print(response)
    return response

def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    return {}

def elicit_intent(intent_request, session_attributes, message):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        'messages': [ message ] if message != None else None,
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }
    
def does_wiki_exist(subject):
    pg = wiki_wiki.page(subject)    
    if pg.exists()==False:
        print("Sorry, I couldn't find a relevant Wikipedia page. Please try again.")

    return pg.exists()

def get_wiki_content(subject):
    pg = wiki_wiki.page(subject)    
    if pg.exists()==False:
        print("Sorry, I couldn't find a relevant Wikipedia page. Please try again.")
    #print(pg.summary)
    return pg.summary

def CheckWikipedia(intent_request):
    session_attributes = get_session_attributes(intent_request)
    print('sessionattributes = ',session_attributes)
    subject = intent_request['sessionState']['intent']['slots']['subject']['value']['originalValue']
    print(subject)
    pg = wiki_wiki.page(subject)    
    if does_wiki_exist(subject)==False:
        fulfillment_state = "Failed"   
        text = 'Sorry, I was unable to find a relevant Wikipedia page. Please try again.'
    else:
        fulfillment_state = "Fulfilled"   
        text = 'OK good, I found a relevant Wikipedia page.'
        
    message =  {
            'contentType': 'PlainText',
            'content': text
        }
    session_attributes.update({'subject': subject})
    return close(intent_request, session_attributes, fulfillment_state, message)

def AnswerQuestion(intent_request):
    session_attributes = get_session_attributes(intent_request)
    question = intent_request['sessionState']['intent']['slots']['question']['value']['originalValue']
    subject = intent_request['sessionState']['sessionAttributes']['subject']
    print(question)
    print(subject)
    wiki_text = get_wiki_content(subject)
    answer = ask_openai(question, wiki_text)  
    message =  {
            'contentType': 'PlainText',
            'content': answer
        }    
    fulfillment_state = "Fulfilled"  
    return close(intent_request, session_attributes, fulfillment_state, message)
    
def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']
    if intent_name == 'CheckWikipedia':
        response = CheckWikipedia(intent_request)
        #print ('intent is CheckWikipedia')
    elif intent_name == 'AnswerQuestion':
        response = AnswerQuestion(intent_request)
        #print('intent is AnswerQuestion')
    else:
        raise Exception('Intent with name ' + intent_name + ' not supported')

    return response

def lambda_handler(event, context):
    print(event)
    response = dispatch(event)
    print(response)
    return response
