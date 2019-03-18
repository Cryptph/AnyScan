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

top70Whales = ['0x007ca1f6bc026b1043fb78d0af0b2ee0ce94c55f', \
                '0x788cdc97403a5cafa60d9aaa7e8265f83d629df5', \
                '0xaf807eec8c0ca8456b1230ebec123983da56cf0b', \
                '0x8d5a28b1940dfffa053d1798c551fbd6d5e9cea8', \
                '0x1f1202592f175500568689370eef5d7db4d58ccf', \
                '0x8a09e5f6cd2f7fc6465009b7d502287e3a2b8d2f', \
                '0xf676684f5cabc2a4eb7ab9241ef3dba144745240', \
                '0xf928a46f5d6460d2bd9ef5f285722c246682f03a', \
                '0x4a4bd49efc67c99bb18d67b8887f76ed55ab92ca', \
                '0xbcfd4bba37ed4a31eef60f3f38568c768b929377', \
                '0x1bcd3db13c02f21bb91dd815c1279e1c422cb738', \
                '0xc34b8ed64e661e8e04692a6911cf826cb2820b85', \
                '0x5bedad97da35c16dc635065d20e3456cae27d49c', \
                '0xd8a67e4266d73a62dba1fb94cfa6220f1fb45095', \
                '0xb1fdac616ab95777b115c80d8d14b3b0cf325f4f', \
                '0x6ce57618c834422b90a0f338c712e7b6eb608e03', \
                '0xbaf739e2f5fc19da60537b5b13923f4016d1a4d2', \
                '0x739e0e6b24d70ee23c615ab7114e3224249ea6f5', \
                '0x7288e4d737550edb6a156bd9bcd0576c5b7f2459', \
                '0x680072190eea8205aa04fe4935913b57d0014045', \
                '0xc7d55e7366fc99d1c568ed3c451ad9f15c0a9a5b', \
                '0x8f1dcac2e21b500aaf37b1210303d579e6c64f12', \
                '0x8cc848e40d507c3fcfd57922320053441d905c14', \
                '0xca87939e19beb0184fbecdb5468dfc72a272dace', \
                '0x3c70a722cf8eedafb1db0b7dd0ed211850b2aa12', \
                '0x0d1c87a87ed9503d5139d6ed29530865b8a938ba', \
                '0x7afad35d23bbd5b7c18fbb9e94a736b1d2bcafbe', \
                '0xcc4d714cb325ef00d7734d309db67e41ae2fd89b', \
                '0x3c6c39631f91f7e2131291599a6c667499601569', \
                '0x0ae146982b2657b1304b4d4827cd4db1236f57d4', \
                '0xbc86338823887876d5d5aeb57d7abf16130a93cf', \
                '0xd65d33ba85f81c7c580195bc52672754ff3e202a', \
                '0xbfc01ad0df3804d1430b52a67ce20dc8689a3774', \
                '0xde2c27d6e7145918bc8105cfba492030bd3dd4c9', \
                '0xaf18bdf259d0fdbf0f23c6acf0625e90f83d5691', \
                '0xad87d559a26383adcc376f0a23f0d0243f4d5740', \
                '0xb9d69ac2c8a51096cbd6c80353e5f4908ef274df', \
                '0x54a4a021c2fa8a5d5d5b9272e488e2654591c8e6', \
                '0x861c9b0ab53847ac8d9c27897824a2d36d298da3', \
                '0x9b3ea3e126df183ef03c32bef0e0dd35b111baf3', \
                '0xe97096ca5df30dbbf57dd28a32e93313dead711b', \
                '0x2bff971f4cef2cae7fcebaba569e0310156fcda7', \
                '0x8e2870b6527259ea49df2e52a7528656afd2d570', \
                '0x750bfe79ba426802627740adad818f0ca1dafa71', \
                '0xf5539e72d915df9e77711a76a4f4ce6396fb8b06', \
                '0xf7683fb9114ad7c07ff39314a693829b66bd1b54', \
                '0xf9fe21352a0e6d8fd85dd94b2250b8e56561bd88', \
                '0x21c7a16beeea35c06cd1688da477893945cdd1d3', \
                '0x5b9d5fe8e2468632378113b921b58cf9ed7e3c4a', \
                '0xa34a3c3043300ee7634f4080937469b215ea610f', \
                '0x647258719cc4d821590fe0bd787f9c456651aa55', \
                '0x39f3afb033bb57ebfb4ff8ac528ace81c821b5eb', \
                '0xf150fab708a286fab33f925f34710543b0f6589e', \
                '0xe66fee6b3a4fe5b055082eae8d2bbfb9fb333af3', \
                '0x7c27c9a9a961b9e6a4443b16dd4b3e2f807ccf9f', \
                '0xe7b878617dc7f21e28336741b8a581d4ed46fdd2', \
                '0xa8a88765bc4aac1cd51e40dcd259d0a8f5c420d7', \
                '0x61554fc81beb72630fc75a85cac91605bab7ef00', \
                '0x6a36188daf1b672fd9e639790dc8470f0621ab6f', \
                '0xdcbd31a3fd254902e64de2e626375e4965864444', \
                '0x6d23771fa539f3d6fc0303ee1a497dcb0c2e2640', \
                '0x7e28be6eeb93edda3d901cb6bf6cf895040ddb0b', \
                '0x1ba4d36a917036eff453e0508942c8ae09c90b7c', \
                '0xa0bea35b33868f02c7d2254902531a14fe400c4c', \
                '0x25dd4725470bef010094441e71c7402caca5701c', \
                '0x4a04ee323e9e4e4b485d840ec38b7ec5cacc1ca4', \
                '0xe605db87c96f5b46eb6b8e39d9569a0b9154ae3c', \
                '0xc905f4cf4bcc27fa79f71dde66e64807b83054df', \
                '0xe04dcb45ee24badc7d96431792c014bf8145494e', \
                '0xac40fd0c5419e2233f29eac0191e72174b0d1e81', \
    ]
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

    datetime.now()
    print("datetime: ", datetime.now())
    #Notify only if have new transactions
    if curTxCnt > lastTxCnt:
        #Date time
        txDateTime = datetime.utcfromtimestamp(curTxInfo["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')

        #Check sender/receiver
        txFrom = curTxInfo["from"]
        txTo = curTxInfo["to"]

        txAlert = ""
        if txFrom in top70Whales:
            txAlert += "Whale[" + top70Whales.index(txFrom) + "] --> out "
        if txTo in top70Whales:
            txAlert +=  "--> in Whale[" + top70Whales.index(txTo) + "]"

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
        notifyText = txDateTime + " " + txAlert + " " + txCaption + " " + str(txValue) + "(" + txTokenSymbol + ")\n"
        notifyTele(notifyText, ChatGroupId, teleAnyScanBotToken)
        print(notifyText)
        lastTxCnt = curTxCnt
    threading.Timer(2.0, ScanToken).start()  # called every 2.0 seconds

ScanToken()