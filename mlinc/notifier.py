import requests

# file_jelle = 'C:/Data/2. Jelle Personal/personal_python_projects/ifttt_info_jelle.txt'
file_jelle = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_jelle.txt'
file_robert = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_robert.txt'

files = [file_jelle, file_robert]


# notify
def notification(fileID, message):
    file = open(fileID, 'r')
    line = file.readlines()
    event = line[0][0:-1]
    id = line[1]

    report = dict()
    report["value1"] = message
    requests.post("https://maker.ifttt.com/trigger/{}/with/key/{}".format(event, id), data=report)


if __name__ == '__main__':
    notification(fileID=file_robert, message='Gozertje!!! We gaan pompon!!! 16:45 in de Gym! Lets goooooooo...!!')
    notification(fileID=file_jelle, message='Gozertje!!! We gaan pompon!!! 16:45 in de Gym! Lets goooooooo...!!')