from HuaweiSMS import HuaweiSMS

# Grab info
SMS = HuaweiSMS()
Traffic = SMS.get_traffic()['response']
Device  = SMS.get_info()['response']

ConnectTime = int(Traffic['CurrentConnectTime']) / 60
ConnectTime = "%.f" % round(ConnectTime,0)

print """
Huawei Device Info:
	IP Address: {}
	Signal Strengh: {}/5
	Minutes Connected: {}
	DNS Servers: {}
		     {}
""".format(Device['WanIPAddress'],Device['SignalIcon'],ConnectTime,Device['PrimaryDns'],Device['SecondaryDns'])
