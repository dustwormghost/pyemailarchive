__author__ = 'dustworm'

from oauth import OAuthGmailAPI
from gmailapi.gmailapi import GmailAPI

def run_mail_archive():
    service = OAuthGmailAPI('secret/client_secret.json', 'FULL').get_gmail_service()
    gmail_api = GmailAPI()

    messagesIds = gmail_api.get_messages_ids_with_matching_query(service, 'me', '')
    ids = []
    for msg in messagesIds:
        ids.append(msg['id'])

    gmail_api.batch_request(service, 'me', ids)




run_mail_archive()




'''
TABLE:

t1 = {
thread_id
message_id
}

t2 = {
    message_id

}


'''