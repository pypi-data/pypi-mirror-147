import json
import requests

class api:
  def __init__(self,apikey,apisecret,broker,version="1.0"):
     self.apikey=apikey 
     self.apisecret=apisecret
     self.burl = "https://" + broker + 'api.algomojo.com/' + str(version) + '/'
  def place_order(self,ticker,exchange,action,ordertype,qty,product,prc=0,dscqty=0,trgprc="0"):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                        "strg_name":"Test Order",
                        "variety":"regular",
                        "tradingsymbol":ticker,
                        "exchange":exchange,
                        "transaction_type":action,        
                        "order_type":ordertype,
                        "quantity":qty,
                        "product":product,
                        "price":prc,
                        "trigger_price":trgprc,
                        "disclosed_quantity":dscqty,                    
                        "validity":"DAY",
                        "tag":"amorder"
                   }
            } 
    url = self.burl + "PlaceOrder"   
    response = requests.post(url,json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue


  def place_multi_order(self, order_list):
    l =order_list
    for i in range(len(l)):
      l[i]["exchange"]=l[i]["exchange"]
      l[i]["tradingsymbol"]=str(l[i]["ticker"])
      l[i]["quantity"]=str(l[i]["qty"])
      l[i]["product"]=l[i]["product"]
      l[i]["price"]= str(l[i]["price"])
      l[i]["transaction_type"]=l[i]["action"]
      l[i]["order_type"]=l[i]["ordertype"]
      l[i]["disclosed_quantity"]=l[i]["discqty"]
      l[i]["trigger_price"]=l[i]["trigprc"]
      l[i]["tag"]= "amorder" 
      l[i]["variety"]="regular"
      l[i]["strg_name"]="stgname"
      l[i]["validity"]="DAY"
      l[i]["user_apikey"]=l[i]["user_apikey"]
      l[i]["api_secret"]=l[i]["api_secret"]
      
    
             
        
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
    return  jsonValue          
    
  
      
      
     
  def place_split_order(self,spot,exchange,action,ordertype,qty,product,prc=0,trgprc=0,dscqty=0):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
             "api_key":apikey,
             "api_secret":apisecret,
             "data":{ 
                       "strg_name":"Test Order",
                       "variety":"regular",
                       "tradingsymbol":spot,
                       "exchange":exchange,
                       "transaction_type":action,        
                       "order_type":ordertype,
                       "quantity":qty,
                       "product":product,
                       "price":prc,
                       "trigger_price":trgprc,
                       "disclosed_quantity":dscqty,                    
                       "validity":"DAY",
                       "tag":"amorder"
                     
                    }
           }
    url = self.burl + "PlaceFOOptionsOrder"     
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue
  def modify_order(self,orderno,qty,ordertype=0,dscqty=0,prc=0,trgprc=0):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                     "variety":"regular",
                     "order_id":orderno,
                     "order_type":ordertype,
                     "quantity":qty,
                     "price":prc,
                     "trigger_price":trgprc,
                     "disclosed_quantity":dscqty,                    
                     "validity":"DAY"
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
                    "variety":"regular",
                    "order_id":orderno
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
    url = self.burl +"Profile"          
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue                  

  def limits(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
           
             }
    url = self.burl +"Limits"         
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
    url = self.burl +"Holdings"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue  

  def order_book(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
           
             }
    url = self.burl +"OrderBook"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue       

  def order_history(self,orderno):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                   
                    "order_id":orderno
                    
                   }
             }
    url = self.burl +"OrderHistory"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue  

  def positions(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                   "pos_type":"NET"
                   }
         
             }
    url = self.burl +"Positions"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue             
                              
 
  def trade_book(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            
             }
    url = self.burl +"Tradebook"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue                                         

  def fetch_token(self,tokenname):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "s":tokenname
                    }
             }
    url = self.burl +"fetchtoken"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 


  def get_quote(self,exchange,symbol):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                     "exchange":exchange,
                     "symbol":symbol
                   }
             }
    url = self.burl +"GetQuote"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 












