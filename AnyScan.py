import requests
from collections import defaultdict
from datetime import datetime
import threading
import telegram
import json


addForkDelta    = "0x8d12a197cb00d4747a1fe03395095ce2a5cc6819"
address         = "0xC3Dd90F7BD1cB523b4D6BC4bA81706e92F7Ff821"
address2        = "0x861c9b0ab53847ac8d9c27897824a2d36d298da3"
contractQRX     = "0x1d5a98162a497cd204948bc5e00e98b44abc7cd4"
contractTUSD    = "0x8dd5fbce2f6a956c3022ba3663759011dd51e73e"
teleAnyScanBotToken = "620177198:AAGwyaIOPNl3nR29FI9n5a6EG6vS5ZTy8Ug"   #@AnyScanBotId
ChatGroupId     = "-359727681"

####################################################################
#Func: Send message to telegram bot
#Ret: nothing
####################################################################
def notifyTele(msg, chat_id, token):
    url = "https://api.telegram.org/bot" + token +"/sendMessage?chat_id=" + chat_id + "&text=" + msg
    response = requests.get(url)
    print(response)

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

####################################################################
#Func: Get token history
#Ret: token history as format below
"""
operations: [
{
    timestamp: 1544443601,
    transactionHash: "0x810bac087d7fdabd70125f17f6d1a972e8861a8aabf5f1e491ba70a614858051",
    tokenInfo: {
        address: "0xff71cb760666ab06aa73f34995b42dd4b85ea07b",
        name: "THBEX",
        decimals: "4",
        symbol: "THBEX",
        totalSupply: "9020000000",
        owner: "0x2cfc4e293e82d48a2c04bf89baaa98572c01c172",
        txsCount: 1367,
        transfersCount: 1747,
        lastUpdated: 1524471272655,
        issuancesCount: 4,
        holdersCount: 156,
        image: "https://ethplorer.io/images/everex.png",
        description: "THBEX is the original test version of electronic digital currency (eTHB) that represents one unit of the Thailand national currency, Baht (THB). THBEX is issued on Ethereum blockchain in the form of ERC20 digital token and governed by secured smart contract. THBEX has indefinite pegged exchange rate of 1:1 to THB. THBEX is underwritten by licensed financial institutions in Thailand and is guaranteed 100% by physical currency reserves, surety bonds, or the underwriters' own capital. Financial guarantee and proof of funds documentation is available in specific issuance records.",
        website: "https://everex.io",
        ethTransfersCount: 0,
        price: {
            rate: 0.030525030525031,
            diff: -0.0012512650523151,
            ts: 1544586606,
            onlyPrice: 1,
            currency: "USD"
        }
    },
    type: "transfer",
    value: "100000",
    from: "0xc0a3ac852fe47c5667ae0427de3c6f3e6eb8bf18",
    to: "0x3df83f9b6fd6eb18fce93a06741557a18156a4d8"
},
...
{
    ...
}
"""
####################################################################
def GetTokenHistory(tokenContract):
    url     = "http://api.ethplorer.io/getTokenHistory/" + tokenContract + "?apiKey=freekey"
    response = requests.get(url)
    content = response.json();
    return content

#Transaction count of last query
lastTxCnt = 0

####################################################################
#Func: Main function
#Ret: nothing
####################################################################
def ScanToken():
    #content = GetTokenInfo(contractQRX)
    # curTxCnt = int(content.get("transfersCount"))
    content = GetTokenHistory(contractQRX)
    global lastTxCnt

    curTxInfo       = content['operations'][0]
    curTxTokenInfo  = curTxInfo.get('tokenInfo')
    curTxCnt        = curTxTokenInfo.get('transfersCount')


    print("curTxCnt: ", curTxCnt)
    #Notify only if have new transactions
    if curTxCnt > lastTxCnt:
        #Date time
        txDateTime = datetime.utcfromtimestamp(curTxInfo["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')

        #Check sender/receiver
        txFrom = curTxInfo["from"]
        txTo = curTxInfo["to"]
        txCaption = "Transaction to somewhere -->"
        if txFrom == addForkDelta:
            txCaption = "ForkDelta --> out"
        if txTo == addForkDelta:
            txCaption = "ForkDelta <-- in"

        #Token symbol
        txTokenSymbol = curTxTokenInfo["symbol"]

        #Transaction value:
        txValue = float(curTxInfo["value"])/1000000000000000000

        #notifyText = txCaption + "\n" + ''.join('{}: {}\n'.format(key, val) for key, val in curTxTokenInfo.items())
        notifyText = txDateTime + " " + txCaption + " " + str(txValue) + "(" + txTokenSymbol + ")\n"
        notifyTele(notifyText, ChatGroupId, teleAnyScanBotToken)
        print(notifyText)
        lastTxCnt = curTxCnt
    threading.Timer(60.0, ScanToken).start()  # called every 60 seconds

ScanToken()