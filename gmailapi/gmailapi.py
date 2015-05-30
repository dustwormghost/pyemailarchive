'''Gmail API'''
import base64
import utils
import pprint

from apiclient import errors
from apiclient.http import BatchHttpRequest


class GmailAPI:
    '''All gmail API that I found useful for this project. Add new ones as needed'''
    def __init__(self):
        pass
    
    def get_page_of_threads(self, gmail_service, user_id):
        return gmail_service.users().threads().list(userId=user_id).execute()
    
    def get_messages_ids_with_matching_query(self, gmail_service, user_id, query=''):
        '''List all messages of the user's mailbox matching query.
        Args:
            gmail_service: Authorized Gmail API service instance
            user_id: User's email address. The special value 'me'
            query: for example 'from:user@domain.com' can be empty for all messages
            
        Returns:
            list of message ids
        '''
        try:
            response = gmail_service.users().messages().list(userId=user_id, q=query).execute()
            
            messagesIds = []
            if 'messages' in response:
                messagesIds.extend(response['messages'])
                
            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = gmail_service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
                messagesIds.extend(response['messages'])
                
            return messagesIds
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return [] 
    
    def get_messages_ids_with_matching_labels(self, gmail_service, user_id, label_ids=[]):
        '''List all messages of the user's mailbox with matching label ids.
        Args:
            gmail_service: Authorized Gmail API service instance
            user_id: User's email address. The special value 'me'
            label_ids: all messages with these label_ids
            
        Returns:
            list of message ids
        '''
        try:
            response = gmail_service.users().messages().list(userId=user_id, labelIds=label_ids).execute()
            
            messagesIds = []
            if 'messages' in response:
                messagesIds.extend(response['messages'])
                
            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = gmail_service.users().messages().list(userId=user_id, labelIds=label_ids, pageToken=page_token).execute()
                messagesIds.extend(response['messages'])
                
            return messagesIds
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return []                  
                
    def get_all_labels(self, gmail_service, user_id):
        '''Get a list of all labels in the user's Mailbox
        
        Args:
            gmail_service: Gmail API service instance
            user_id: 'me' or email address
            
        Returns:
            list of labels
        '''
        try:
            response = gmail_service.users().labels().list(userId=user_id).execute()
            return  response['labels']
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return []
        
    def get_attachments(self, gmail_service, user_id, msg_id):
        '''Get attachments for given message id
        
        Args:
            gmail_service: Gmail API service instance
            user_id: 'me' or email address
            msg_id: message id
        Returns:
            list of base64 file data
        '''
        try:
            message = gmail_service.users().messages().get(userId=user_id, id=msg_id).execute()
            
            file_data = {}
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['filename']:
                        if 'data' in part['body']:
                            data = part['body']['data']
                        else:
                            att_id = part['body']['attachmentId']
                            att = gmail_service.users().messages().attachments().get(userId=user_id, messageId=msg_id, id=att_id).execute()
                            data = att['data']
                        file_data[part['filename']] = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    
            return file_data
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return {}
                    
        
    def save_file(self, file_name, file_data, dir_path):
        '''given file name, file data and output directory, save file
        Args:
            file_name: file name
            file_data: data to output
            dir_path: destination directory
            
        Returns:
        '''
        path = ''.join([dir_path, file_name])
        
        with open(path, 'w') as oStream:
            oStream.write(file_data)
        
        return True
    
    def delete_msg(self, service, user_id, msg_id):
        '''Given user id and message id, delete Message
        Args:
            service: Gmail API service Instance
            user_id: 'me' or email  address
            msg_id: message id to be deleted
         
        Returns:
            True if all okay, False otherwise
        '''
        try:
            service.users().messages().delete(userId=user_id, id=msg_id).execute()
            return True
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return False
        
    def get_attachments_and_save_wrapper(self, service, user_id, label, out_dir):
        '''get attachments and save to local output directory
        Returns:
            list of message ids that contained attachment
        '''
        inbox_msgs = self.get_messages_ids_with_matching_labels(service, user_id, [label])    

        msgIds = []
        utils.log( 'Found ' + str(len(inbox_msgs)) + ' messages with label: ' + label )
        utils.log( 'Save attachments to ' + out_dir )
        for msg in inbox_msgs:
            att = self.get_attachments(service, user_id, msg['id'])
            if len(att) > 0:
                msgIds.append(msg['id'])
                for file_name in att:
                    self.save_file(file_name, att[file_name], out_dir)
                    print '*',
                    
        utils.log( 'Total number of attachments saved ' +  str(len(msgIds)))

        return msgIds

    def delete_msgs_wrapper(self, service, msgIds=[], user_id=''):
        utils.log( 'Delete ' + str(len(msgIds)) + ' messages')
        for msgId in msgIds:
            self.delete_msg(service, user_id, msgId)
            print '*',
            
        utils.log('Done')

    def print_msgs(self, request_id, response, exception):
        if exception is not None:
            print exception
        else:
            # for part in response['payload']['parts']:
            #     print 'PART\n'
            #     pprint.pprint(part)
            pprint.pprint(response)
            print "\n\n\n\n\n\n"

    def batch_request(self, service, user_id, msg_ids=[]):
        batch = BatchHttpRequest()
        for id in msg_ids:
            batch.add(service.users().messages().get(userId=user_id, id=id), callback=self.print_msgs)

        batch.execute()




            # if 'parts' in message['payload']:
            #     for part in message['payload']['parts']:
            #         if part['filename']:
            #             if 'data' in part['body']:
            #                 data = part['body']['data']
            #             else:
            #                 att_id = part['body']['attachmentId']
            #                 att = gmail_service.users().messages().attachments().get(userId=user_id, messageId=msg_id, id=att_id).execute()
            #                 data = att['data']
            #             file_data[part['filename']] = base64.urlsafe_b64decode(data.encode('UTF-8'))
        
