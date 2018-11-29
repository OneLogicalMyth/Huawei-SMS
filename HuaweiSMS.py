from requests import Session
from re import findall
import xmltodict
import datetime

# Built for the Huawei E3372h Dongle
# Tested on Ubuntu 16.04 LTS and on Raspberry Pi 3
class HuaweiSMS(object):

    # Allow for IP change should it differ between devices
    def __init__(self,ip='192.168.8.1'):
        self.url = 'http://{}'.format(ip)

    def get_csrf(self, session):
        url = '{}/html/smsinbox.html'.format(self.url)
        content = session.get(url).content
        #the page seems to always have 2 csrf tokens but only 1 is needed?!
        csrf_token = findall('name="csrf_token"\scontent="(.*?)"', content)[0]
        return csrf_token

    def login(self):
        # login fresh for each request, to help with expiry
        session = Session()
        url = '{}/html/index.html'.format(self.url)
        return session

    # core GET request function
    def get_page(self,url):
        session = self.login()
        csrf_token = self.get_csrf(session)
        token = {'__RequestVerificationToken': csrf_token}
        content = session.get(url, headers=token).content
        return xmltodict.parse(content)

    # core POST request function
    def post_page(self,url,data):
        session = self.login()
        csrf_token = self.get_csrf(session)
        token = {'__RequestVerificationToken': csrf_token}
        content = session.post(url, headers=token, data=data).content
        return xmltodict.parse(content)

    # The below functions make use of the core functions above
    def get_info(self):
        url = '{}/api/monitoring/status'.format(self.url)
        return self.get_page(url)

    def get_sms(self,readcount='20'):
        url = '{}/api/sms/sms-list'.format(self.url)
        data = '<?xml version="1.0" encoding="UTF-8"?><request><PageIndex>1</PageIndex><ReadCount>{}</ReadCount><BoxType>1</BoxType><SortType>0</SortType><Ascending>0</Ascending><UnreadPreferred>0</UnreadPreferred></request>'.format(readcount)
        return self.post_page(url,data)

    def get_unread(self):
        notify = self.get_notifications()
        if 'response' in notify:
            if notify['response']['UnreadMessage'] != '0':
                return self.get_sms(notify['response']['UnreadMessage'])
        return None

    def set_read(self,index):
        url = '{}/api/sms/set-read'.format(self.url)
        data = '<?xml version="1.0" encoding="UTF-8"?><request><Index>{}</Index></request>'.format(index)
        return self.post_page(url,data)

    def send_sms(self,number,message):
        url = '{}/api/sms/send-sms'.format(self.url)
        length = len(message)
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = '<?xml version="1.0" encoding="UTF-8"?><request><Index>-1</Index><Phones><Phone>{}</Phone></Phones><Sca></Sca><Content>{}</Content><Length>{}</Length><Reserved>1</Reserved><Date>{}</Date></request>'.format(number,message,length,date)
        return self.post_page(url,data)

    def get_notifications(self):
        url = '{}/api/monitoring/check-notifications'.format(self.url)
        return self.get_page(url)


# Example getting unread SMS messages
SMS = HuaweiSMS()
print SMS.get_unread()
