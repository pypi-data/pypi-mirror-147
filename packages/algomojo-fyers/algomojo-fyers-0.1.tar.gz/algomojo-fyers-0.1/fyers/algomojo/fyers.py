import json
import requests

class api:
  def __init__(self,apikey,apisecret,broker,version="1.0"):
     self.apikey=apikey 
     self.apisecret=apisecret
     self.burl = "https://" + broker + 'api.algomojo.com/' + str(version) + '/'
  def place_order(self,ticker,qty,ordertype,action,product,limit=0,stop=0,dscqty=0,stoploss=0,takeprofit=0):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                     "strg_name": "Test Strategy",
                     "symbol":ticker,
                     "qty":qty,
                     "type":ordertype,
                     "side":action,
                     "productType":product,
                     "limitPrice":limit,
                     "stopPrice": stop,
                     "validity": "DAY",
                     "disclosedQty": dscqty,
                     "offlineOrder": "False",
                     "stopLoss":stoploss,
                     "takeProfit": takeprofit,
                   }
            } 
    url = self.burl + "PlaceOrder"   
    response = requests.post(url,json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return jsonValue


  def place_multi_order(self, order_list):
    l =order_list
    for i in range(len(l)):
      l[i]["user_apikey"]=l[i]["user_apikey"]
      l[i]["api_secret"]=str(l[i]["api_secret"])
      l[i]["symbol"]= str(l[i]["ticker"])
      l[i]["productType"]=l[i]["product"]
      l[i]["side"]=l[i]["action"]
      l[i]["type"]=l[i]["ordertype"]
      l[i]["qty"]=l[i]["qty"]
      l[i]["disclosedQty"]=l[i]["dscqty"]
      l[i]["limitPrice"]=l[i]["limitprice"] 
      l[i]["stopPrice"]=l[i]["stopprice"]
      l[i]["strg_name"]="stgname"
      l[i]["validity"]="DAY"
      l[i]["offlineOrder"]="false"
      l[i]["stopLoss"]=l[i]["stoploss"]
      l[i]["takeProfit"]=l[i]["takeprofit"]
      l[i]["order_rorder_refno"]="1"
    
             
        
    data = {
              "api_key": self.apikey,
              "api_secret": self.apisecret,
              "data":
                {
                   "orders": l
                }
            }
    print(data)     
    url = self.burl + "PlaceMultiOrder"        
    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue) 
    return jsonValue         

  
  def modify_order(self,orderno,ordertype=0,action=0,qty=0,limit=0):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "strg_name":"Test Strategy",
                   "id":orderno,
                   "qty":qty,
                   "type":ordertype,
                   "side":action,
                   "limitPrice":limit
                  }
             }
    url = self.burl + "ModifyOrder"           
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue         

  def cancel_order(self,orderno):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                     "id":orderno,
                   }
             }
    url = self.burl +"CancelOrder"          
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue        
              
  def profile(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            
             }
    url = self.burl +"profile"          
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue                  

  def funds(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
           
             }
    url = self.burl +"funds"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 

  def holdings(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
           
             }
    url = self.burl +"holdings"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue  

  def orderbook(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            
             }
    url = self.burl +"orderbook"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue       

  def tradebook(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            
             }
    url = self.burl +"tradebook"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue  

  def positions(self,client_id):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            
             }
    url = self.burl +"positions"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue             
                              
 
  def SquareOffPosition(self,orderno):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                     "id":orderno
                    
                    
                   }
             }
    url = self.burl +"SquareOffPosition"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue                                         

  def SquareOffAllPositions(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            
             }
    url = self.burl +"SquareOffAllPositions"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 


  def partial_position_conversion(self,ticker,positionside,convertyqty,fromm,to):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "symbol":ticker,
                    "positionSide":positionside,
                    "convertQty":convertqty,
                    "convertFrom":fromm,
                    "convertTo":to
                    }    
           }
    url = self.burl +"PartialPositionconvertion"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 


  def fetch_token(self,token):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "s":token
           }
          }
    url = self.burl +"fetchtoken"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 


  
  def get_quote(self,symbol):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "fy_symbol":symbol
           }
          }
    url = self.burl +"GetQuote"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 












