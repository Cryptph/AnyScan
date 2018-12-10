import requests
from collections import defaultdict
from datetime import datetime
import threading

address         = "0xC3Dd90F7BD1cB523b4D6BC4bA81706e92F7Ff821"
address2        = "0x861c9b0ab53847ac8d9c27897824a2d36d298da3"
contractQRX     = "0x1d5a98162a497cd204948bc5e00e98b44abc7cd4"
contractTUSD    = "0x8dd5fbce2f6a956c3022ba3663759011dd51e73e"

####################################################################
#Func: Get transaction list by address
#Ret: Transaction list
####################################################################
def GetTxByAddress(address):
    url = "http://api.etherscan.io/api?module=account&action=txlist&address=" + address + \
          "&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken"

    url2 = "http://api.etherscan.io/api?module=account&action=txlist&contractaddress=" + contractQRX + \
           "&address=" + address + "&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken"

    response = requests.get(url2)
    content = response.json()
    result = content.get("result")

    data = defaultdict(dict)
    for n, tx in enumerate(result):
        tx_timeStamp = int(tx.get("timeStamp"))
        tx_hash      = tx.get("hash")
        tx_from      = tx.get("from")
        tx_to        = tx.get("to")
        tx_value     = tx.get("value")

        data[n]["timeStamp"]    = datetime.utcfromtimestamp(tx_timeStamp).strftime('%Y-%m-%d %H:%M:%S')
        data[n]["hash"]         = tx_hash
        data[n]["from"]         = tx_from
        data[n]["to"]           = tx_to
        data[n]["value"]        = tx_value

    return data

####################################################################
#Func: Get token balance of specific address
#Ret: balance
####################################################################
def GetTokenBalance(address, tokenContract):
    url     = "http://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" + tokenContract + \
              "&address=" + address + "&tag=latest&apikey=YourApiKeyToken"

    response = requests.get(url)
    content = response.json()
    result  = content.get("result")
    return result

####################################################################
#Func: Get token information
#Ret: token information
####################################################################
def GetTokenInfo(tokenContract):
    url     = "http://api.ethplorer.io/getTokenInfo/" + tokenContract + "?apiKey=freekey"
    response = requests.get(url)
    content = response.json();
    return content

#Transaction count of last query

####################################################################
#Func: Main function
#Ret: nothing
####################################################################
def Main():
    lastTxCnt = 0
    threading.Timer(5.0, Main).start()  # called every 5 seoconds

    #Get token information
    content = GetTokenInfo(contractTUSD)
    curTxCnt = int(content.get("transfersCount"))
    if curTxCnt > lastTxCnt:
        print("Something new !! lastTxCnt: ",lastTxCnt, "curTxCnt: ", curTxCnt)
        lastTxCnt = curTxCnt
        print("After show !! lastTxCnt: ", lastTxCnt, "curTxCnt: ", curTxCnt)

Main()


