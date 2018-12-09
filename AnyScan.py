import requests
from collections import defaultdict
from datetime import datetime

address = "0xC3Dd90F7BD1cB523b4D6BC4bA81706e92F7Ff821"

####################################################################
#Func: Get transaction list by address
#Ret: Transaction list
####################################################################
def GetTxByAddress(address):
      url = "http://api.etherscan.io/api?module=account&action=txlist&address=" + address + \
            "&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken"

      response = requests.get(url)
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
####################################################################

txDataList = GetTxByAddress(address)
#last transaction:
print(txDataList[0])