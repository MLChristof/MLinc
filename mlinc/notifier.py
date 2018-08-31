import requests

file_jelle = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_jelle.txt'
file_robert = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_robert.txt'
file_christof = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_christof.txt'
file_vincent = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_vincent.txt'


# notify
def notification(fileID, message):
    file = open(fileID, 'r')
    line = file.readlines()
    event = line[0][0:-1]
    id = line[1]
    # print(event)
    # print(id)

    report = dict()
    report["value1"] = message
    requests.post("https://maker.ifttt.com/trigger/{}/with/key/{}".format(event, id), data=report)


if __name__ == '__main__':
    message = 'Twee Belgen lopen over een treinrails. Zegt die ene: “Wat een lange trap hè?” Zegt die andere :”Dat valt nog wel mee, maar de leuning zit zo laag”.'
    notification(fileID=file_robert, message=message)
    # notification(fileID=file_jelle, message=message)
    # notification(fileID=file_christof, message=message)
    # notification(fileID=file_vincent, message=message)
