
Metadata-Version: 2.1

Name: algomojo-fyers

Version: 0.1

Summary: A functional python wrapper for  trading api

Home-page: 

Author: Algomojo

Author-email: support@algomojo.com

License: MIT

Description: 
        ## ABOUT
        A functional python wrapper for firststock trading api.
        It is a python library for the [Algomojo Free API + Free Algo Trading Platform ](https://algomojo.com/). 
        It allows rapid trading algo development easily, with support for both REST-API interfaces. 
        Execute Orders in Reatime, Modify/Cancel Orders, Retrieve Orderbook, Tradebook, Open Positions, Squareoff Positions and much more functionalities. 
        For more details of each API behavior, Pease see the Algomojo API documentation.
        
        
        ## License
        
         Licensed under the MIT License.

        
        ## Documentation
        [Algomojo Rest API documentation ](https://algomojo.com/docs/python)
        
        
        
        
        ## Installation
        Install from PyPI
        
        	pip install algomojo-fyers
        
        Alternatively, install from source. Execute setup.py from the root directory.
        python setup.py install
        
        Always use the newest version while the project is still in alpha!
        
        
        ## Usage Examples
        In order to call Algomojo trade API, you need to sign up for an trading account with one of the partner broker and obtain API key pairs and enjoy unlimited access to the API based trading.
         Replace api_key and api_secret_key with what you get from the web console.
        
        
        
        
        ## Getting Started
        
        After downloading package import the package and create the object with api credentials
        
        
        	from algomojo import fyers
        
        
        
        
        
        ## Creating  Object
        
        For creating an object there are 3 arguments which would be passed
        
                 api_key : str
                     User Api key (logon to algomojo account to find api credentials)
                 api_secret : str
                     User Api secret (logon to algomojo account to find api credentials)
                 Broker : str
                     This takes broker it generally consists 2 letters , EX: fyers--> fy,
        
        Sample:
        	
        	at=api(api_key="20323f062bb71ca6fbb178b4df8ac5z6",
        		    api_secret="686786a302d7364d81badc233f1d22e3",
        		    broker="fy")
        
        
        
        
        
        
        ## Using Object Methods
        obj.method(mandatory_parameters)  or obj.method(madatory_parameters+required_parameters)
        
        
        # Avaliable Methods
        	
        ### 1. place_order:  
        
        		Function with mandatory parmeters: 
        				place_order(ticker,qty,ordertype,action,product)
        		
        		Function with all parametrs:       
        				place_order(self,ticker,qty,ordertype,action,product,limit,stop,dscqty,stoploss,takeprofit)
                 	 
                        Sample :        
        				at.place_order(ticker="NSE:RELIANCE-EQ",qty="1",ordertype="2",acti0n="1",product="INTRADAY")
        
        ### 2.place_multi_order(order_list)

	    Sample order_list: 
		[ 
                {
                "order_refno":"1",
                "user_apikey":"xxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "api_secret":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "strg_name": "Test Strategy",
                "ticker":"NSE:RELIANCE-EQ",
                "qty":"1",
                "ordertype":"2",
                "action":"1",
                "product":"INTRADAY",
                "limitprice":0,
                "stopprice": 0,
                "validity": "DAY",
                "dscqty": 0,
                "offlineOrder": "False",
                "stoploss": 0,
                "takeprofit": 0
                },
                {
                "order_refno":"2",
                "strg_name": "Test Strategy",
                "user_apikey":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "api_secret":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "ticker":"NSE:SBIN-EQ",
                "qty":"1",
                "ordertype":"2",
                "action":"1",
                "product":"INTRADAY",
                "limitprice":0,
                "stopprice": 0,
                "validity": "DAY",
                "dscqty": 0,
                "offlineOrder": "False",
                "stoploss": 0,
                "takeprofit": 0
                }
            ]
	Sample function call:  
		at.place_multi_order(order_list)
        
       
        
        		
        ### 3. modify_order:
        
        		Funtion with mandatory parameters:  
        			     	modify_order(orderno,qty)
        		
        		Function with all parameters:
        		 	    modify_order(orderno,ordertype,action,qty,limit):
        		
        		Sample for tradejini: `		   
        				at.modify_order(orderno="1457896512",
						        qty="70",prc="600")
        		
        		
        		
        
        
        
        ### 4. cancel_order
        
        		Funtion with mandatory parameters:   
        				cancel_order(orderno)
        
        		Function with all parameters:          
        		
        				cancel_order(orderno)
        
        		Sample:             
        				at.cancel_order(orderno="4567891523")

        
        		
        
        ### 5. profile:
        
        		Funtion with mandatory parameters:   
        					profile()
        					
        		Function with all parameters:        
        					profile()
        					
        		Sample:                              
        					profile()
        					             
        
        ### 6. funds
        
        
        		Funtion with mandatory parameters:   
        					funds()
        					
        		Function with all parameters:        
        					funds()
        					
        	        Sample:                              
        					at.funds()
        		                                    
        
        
        
        
        
        ### 7. holdings: 
        
        		Funtion with mandatory parameters:   
        					holdings()
        					
        		Function with all parameters:       
        					holdings()
        					
        		Sample:                              
        					at.holdings()
        
        
        
        ### 8. orderbook
        
        
        		Funtion with mandatory parameters:   
        					orderbook()
        		
        		Function with all parameters:        
        					orderbook()
        					
        		Sample:                             
        					at.orderbook()
        
        
        
        
        
        ### 9. tradebook
        
        
        		Funtion with mandatory parameters:   
        					tradebook()
        					
        		Function with all parameters:        
        					tradebook()
        					
        		Sample:                              
        					at.tradebook()
        
        
        
        
        ### 10. positions
                
             	Funtion with mandatory parameters:   
        					positions()
        					
        		Function with all parameters:        
        					positions()
        					
        		Sample:                              
        					at.positions()
        
                    
        					
        
        		
        		
        		
        
        
        
        
        ### 11.SquareOffPosition

                
             	Funtion with mandatory parameters:   
        					SquareOffPosition()
        					
        		Function with all parameters:        
        					SquareOffPosition()
        					
        		Sample:                              
        					at.SquareOffPosition()
        
        
        
         ### 12.SquareOffAllPositions

                
             	Funtion with mandatory parameters:   
        					SquareOffAllPositions()
        					
        		Function with all parameters:        
        					SquareOffAllPositions()
        					
        		Sample:                              
        					at.SquareOffAllPositions()
        
        
        ### 13.partial_position_conversion

                
             	Funtion with mandatory parameters:   
        					 partial_position_conversion(ticker,positionside,convertyqty,fromm,to)
        					
        		Function with all parameters:        
        					 partial_position_conversion(ticker,positionside,convertyqty,fromm,to)
        					
        		Sample:                              
        					at.partial_position_conversion(symbol="MCX:SILVERMIC20NOVFUT",
                                                                               positionSide=1,
                                                                               convertQty=1,
                                                                               convertFrom="INTRADAY",
                                                                               convertTo="CNC")

        
        
         ### 14.fetchtoken

                
             	Funtion with mandatory parameters:   
        					fetchtoken(token)
        					
        		Function with all parameters:        
        					fetchtoken(token)
        					
        		Sample:                              
        					at.fetchtoken(token="RELIANCE-EQ")

   
         ### 15.get_quote

                
             	Funtion with mandatory parameters:   
        					get_quote(symbol)
        					
        		Function with all parameters:        
        					get_quote(symbol)
        					
        		Sample:                              
        					at.get_quote(symbol="NSE:RELIANCE-EQ")





       
    
         
        
        
        
        
        
Platform: UNKNOWN
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 3
Description-Content-Type: text/markdown
