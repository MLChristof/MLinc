import requests

file = open('C:/Data/2. Jelle Personal/personal_python_projects/ifttt_info.txt', 'r')
line = file.readlines()
event = line[0][0:-1]
id = line[1]


# notify
def notification(priority, stock):
    report = dict()
    report["value1"] = priority
    report["value2"] = stock
    requests.post("https://maker.ifttt.com/trigger/{}/with/key/{}".format(event, id), data=report)

notification(priority="HIGH", stock="MLinc_futures")