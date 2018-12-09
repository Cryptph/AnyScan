import requests

address = "0x861c9B0aB53847aC8D9C27897824a2D36D298da3"
url = "http://api.etherscan.io/api?module=account&action=txlist&address=" + address + \
      "&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken"

response = requests.get(url)
content = response.json()
result = content.get("result")

for n, tx in enumerate(result):
      tx_timeStamp = tx.get("timeStamp")
      tx_hash      = tx.get("hash")
      tx_from      = tx.get("from")
      tx_to        = tx.get("to")
      tx_value     = tx.get("value")

      print("Transaction: ", n)
      print("timeStamp:\t", tx_timeStamp)
      print("hash:\t\t", tx_hash)
      print("from:\t\t", tx_from)
      print("to:\t\t\t", tx_to)
      print("value:\t\t", tx_value)

      if tx_from == address:
            print("sending")
      else:
            print("receiving")
      print("\n")