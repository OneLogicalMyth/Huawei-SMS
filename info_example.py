from HuaweiSMS import HuaweiSMS
import datetime

# Grab info
SMS = HuaweiSMS()
Traffic = SMS.get_traffic()['response']
Device  = SMS.get_info()['response']

ConnectTime = int(Traffic['CurrentConnectTime'])
ConnectTime = str(datetime.timedelta(seconds=ConnectTime))

print """
Huawei Device Info:
	IP Address: {}
	Signal Strengh: {}/5
	Duration: {} (Hours:Minutes:Seconds)
	DNS Servers: {}
		     {}
""".format(Device['WanIPAddress'],Device['SignalIcon'],ConnectTime,Device['PrimaryDns'],Device['SecondaryDns'])
