## Getting last date of data 

import pandas as pd
dfOld = pd.read_csv(
    "../textData/discord.csv", encoding="ISO-8859-1")

lastDate = dfOld['date'][0]



## getting new data to from present to lastDate

import requests
import json

headers = {
    'authorization': 'MzM0ODY3MDQ3MDIyNDYwOTMx.YnE2PA._aaRjPQKP63HqZmhIXTrqA3ZipY'
    }
end = lastDate
end = end.split("/")
endyear = end[2]
endmonth = end[1]  
if len(endmonth) == 1:
    endmonth = "0"+endmonth
endday = end[0]  
if len(endday) == 1:
    endday = "0"+endday
endcomb = endyear+endmonth+endday
endDate = int(endcomb)

# def retrive_messages(serverName, channelName, channelid, left):
#     r = requests.get('https://discord.com/api/v9/channels/' +
#                      channelid+'/messages?limit=100', headers=headers)

#     fullJson = []
#     jsonn = json.loads(r.text)
#     fullJson.extend(jsonn)

#     counter = 1
#     maxcounter = 700
#     # 1000 = total of 10,000 messages per channel if possible.
#     # if max counter = 10, we will scrape 10*100 messages

#     while len(r.text) == 100 or counter != maxcounter:
#         try:
#             lstmsg = jsonn[99]
#             lstmsgID = lstmsg['id']
#             r = requests.get('https://discord.com/api/v9/channels/' +
#                              channelid+'/messages?limit=100&before='+lstmsgID, headers=headers)
#             jsonn = json.loads(r.text)
#             fullJson.extend(jsonn)
#             print('lastMsgId', lstmsgID)
#             print("scrapping channel id: "+channelid +
#                   " 100 x "+str(counter)+" scrapped")
#             counter += 1
#             print(left, "/", total)

#         except:
#             print("end of total message")
#             break

#     cleanedRow = []
#     for i in range(0, len(fullJson)):
#         newrow = {}
#         newrow['messageID'] = fullJson[i]['id']
#         newrow['author_id'] = fullJson[i]['author']['id']
#         newrow['author_username'] = fullJson[i]['author']['username']
#         newrow['content'] = fullJson[i]['content']
#         newrow['timestamp'] = fullJson[i]['timestamp']
#         newrow['serverName'] = serverName
#         newrow['channelName'] = channelName
#         cleanedRow.append(newrow)

#     print("scrapped finished : "+serverName+"-"+channelName +
#           " total no of message:" + str(len(fullJson)))

#     count = 0
#     for emp in cleanedRow:
#         if count == 0:

#             # Writing headers of CSV file
#             header = emp.keys()
#             csv_writer.writerow(header)
#             count += 1

#         # Writing data of CSV file
#         try:
#             csv_writer.writerow(emp.values())
#         except:
#             None

# #     return True


# channelList = [
#     ['SushiSwap Community', 'Price Talk', '749777962995548210'],
#     ['SushiSwap Community', 'sushi-dao', '748033004323995680'],
#     ['SushiSwap Community', 'General', '748031363935895556'],
#     ['SushiSwap Community', 'the-road-ahead', '937318619900149780'],
#     ['SushiSwap Community', 'free-for-all', '941037888982888478'],
#     ['Aave Community', 'General', '602826300813606923'],
#     ['Aave Community', 'aavenomics', '640257206645686282'],
#     ['Aave Community', 'fa-ta-trading', '616947577253920768'],
#     ['Aave Community', 'shitpost-memes', '696320061903732817'],
#     ['r/CrpytoCurrency', 'defi', '676910097259298818'],
#     ['Compound', 'compound', '402910780670083094'],
#     ['Compound', 'ecosystem', '600821861000937476'],
#     ['Curve Finance', 'general', '729808685009731610'],
#     ['Curve Finance', 'curve-v2', '852398327341514792'],
#     ['Uniswap', 'general', '597638926152499206'],
#     ['Uniswap', 'speculation', '756005648113860668'],
# ]

def retrive_messages(serverName,channelName, channelid):
    r = requests.get('https://discord.com/api/v9/channels/' +
                    channelid+'/messages?limit=100', headers=headers)

    fullJson = []
    jsonn = json.loads(r.text)
    fullJson.extend(jsonn)

    counter = 1
    maxcounter = 700 # if max counter = 10, we will scrape 10*100 messages
    

    while len(r.text) == 100 or counter != maxcounter:
        try:
            lstmsg = jsonn[99]
            lstmsgID = lstmsg['id']
            r = requests.get('https://discord.com/api/v9/channels/' +
                        channelid+'/messages?limit=100&before='+lstmsgID, headers=headers)
            jsonn = json.loads(r.text)
            
            ## check if data has been caught up
            lastTimestamp = jsonn[len(jsonn)-1]['timestamp']
            dateData = lastTimestamp.split("T")[0].split("-")
            year = dateData[0]
            month = dateData[1]    
            day = dateData[2]   
            comb = year+month+day
            comb = int(comb)
            print(comb ,endDate)
            if comb <= endDate:
                print("hit last date")
                break
            else:    
                fullJson.extend(jsonn)
                print('lastMsgId', lstmsgID)
                print("scrapping channel id: "+channelid +
                      " 100 x "+str(counter)+" scrapped")
                counter += 1
        except:
            print("end of total message")
            break

    for i in range(0, len(fullJson)):
        fullJson[i]['serverName'] = serverName
        fullJson[i]['channelName'] = channelName

    print("scrapped finished : "+serverName+"-"+channelName +
          " total no of message:" + str(len(fullJson)))
    return fullJson


channelList = [
    ['SushiSwap Community', 'Price Talk', '749777962995548210'],
    ['SushiSwap Community', 'sushi-dao', '748033004323995680'],
    ['SushiSwap Community', 'General', '748031363935895556'],
    ['SushiSwap Community', 'the-road-ahead', '937318619900149780'],
    ['SushiSwap Community', 'free-for-all', '941037888982888478'],
    ['Aave Community', 'General', '602826300813606923'],
    ['Aave Community', 'aavenomics', '640257206645686282'],
    ['Aave Community', 'fa-ta-trading', '616947577253920768'],
    ['Aave Community', 'shitpost-memes', '696320061903732817'],
    ['r/CrpytoCurrency', 'defi', '676910097259298818'],
    ['Compound', 'compound', '402910780670083094'],
    ['Compound', 'ecosystem', '600821861000937476'],
    ['Curve Finance', 'general', '729808685009731610'],
    ['Curve Finance', 'curve-v2', '852398327341514792'],
    ['Uniswap', 'general', '597638926152499206'],
    ['Uniswap', 'speculation', '756005648113860668'],
]

mainList = []

left = 1
total = len(channelList)
for channelDetails in channelList:
    mainList.extend(retrive_messages(channelDetails[0], channelDetails[1] ,channelDetails[2]))
    print(left,"/",total)
    left += 1


dfNew=pd.DataFrame.from_records(mainList)
messageID = dfNew['id']
author_id = []
author_username = []
content = dfNew['content']
timestamp = dfNew['timestamp']
serverName = dfNew['serverName']
channelName = dfNew['channelName']
date = []
for i in dfNew['author']:
    author_id.append(i['id'])
    author_username.append(i['username'])    

for i in dfNew['timestamp']:
    dateData = i.split("T")[0].split("-")
    year = dateData[0]
    month = dateData[1]    
    day = dateData[2]   
    output = day+'/'+month+'/'+year
    date.append(output)

d = {'messageID':messageID,'author_id':author_id,'author_username':author_username,'content':content,'timestamp':timestamp,'serverName':serverName,'channelName':channelName,'date':date}
df = pd.DataFrame(data=d)

finalDF = pd.concat([df,dfOld])
dfOld.to_csv("../textData/Olddiscord.csv")
finalDF.to_csv("../textData/discord.csv")