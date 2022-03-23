from asyncio.windows_events import NULL
from datetime import datetime
import pandas
import ccxt
import pyti
import pickle
import time


def rule_evaluator(event,context):
    '''
        Stateless Function to Evaluate Trading Logic on the latest price data
        Event/Trigger: Cloud Scheduler

    '''

    '''
        Stock List and Corresponding Prices to be fetched from GET /stocks
    '''
    # stock_list=['BTCUSDT','ETHUSDT','BNBUSDT']
    
    # with open('sample_output.pkl', 'rb') as f:
    #     stock_prices = pickle.load(f)


    stock_list = [{
    "id": 1,
    "name": "Bitcoin",
    "ticker": "BTCUSDT",
    "prices": [42553.70,42553.70,42553.70,42553.70]
    },
    {
    "id": 2,
    "name": "Ethereum",
    "ticker": "ETHUSDT",
    "prices": [42553.70,42553.70,42553.70,42553.70]
    },
    {
    "id": 3,
    "name": "Binance",
    "ticker": "BNBUSDT",
    "prices": [42553.70,42553.70,42553.70,42553.70]
    }
    ]

    '''Hard Coded Parameters: 
            Number of Candles, 
            Interval, 
            User ID/Pwd, 
            Whether to Fetch the Last Price 
            Strategy Name/Description
            Technical Indicators Used
    '''
    # candles = 50
    # interval = '1h'
    # exchange= ccxt.binance({
    #                     'apiKey': 'INH9JYsd4Cu3kMPoONiCVHP3KlACsg3F4ehDN1cburoKohsARMpZGcq4PnQoqzyF',
    #                     'secret': 'FSVMXANswsGOj3B4Oi4NSDOlX5fsvWOJ3s56DQsWvJTjLhSuPyq1aFLbFEWoOrMt',
    #                     'enableRateLimit': True, 
    #                     'options': {'defaultType': 'future'},
    #                     'hedgeMode':True
    #                     })
    last_incomplete_candle = False
    strategy_params = {
        'strat_name':'ema_cross_over_under',
        'technical_indicators': {'fast_ema':4,'slow_ema':20}
    }

    min_input_length =   np.max([float(strategy_params['technical_inidcators']['fast_ema']),float(strategy_params['technical_inidcators']['slow_ema'])])


    user_stocks = [
                {
                    "id": 1,
                    "stock_id": 1,
                    "user_id": 1,
                    "date_opened": 1648058100,
                    "date_closed": 1648058104,
                    "open_price": "1526.32",
                    "close_price": "1621.25"
                },
                {
                    "id": 2,
                    "stock_id": 1,
                    "user_id": 1,
                    "date_opened": 1648058102,
                    "date_closed": null,
                    "open_price": "1500.32",
                    "close_price": null
                },
                {
                    "id": 3,
                    "stock_id": 1,
                    "user_id": 1,
                    "date_opened": 1648058104,
                    "date_closed": null,
                    
                    "open_price": null,
                    
                    "close_price": null
                }
            ]


    '''
        for each stock
    '''
    for stock in stocks:   

        if len(list(stock['prices'].values))<min_input_length:
            return "INPUT HAS TOO FEW stockENTS"

        closes = stock['prices'].astype(float)
        # datetimes = stock['prices']['datetime']
        # closes = closes[:-1]
        # closes['close'] = closes['close'].astype(float)

        '''Calculate "Aggregate" Indicator from all Technical Indicators'''
        indicator = pandas.DataFrame(pyti.ema(closes.tolist(),strategy_params['technical_indicators']['fast_ema'])
                                - pyti.ema(closes.tolist(),strategy_params['slow_ema']),
                                columns=['ema_diff'])
        '''Reduce Length of All Columns'''
        closes = closes[(min_input_length+1):].reset_index(drop=True)
        indicator = indicator[(min_input_length+1):].reset_index(drop=True)
        # datetimes = datetimes[(min_input_length+1):].reset_index(drop=True)
        '''Compute Signal Column (permissible values 1,-1,0)'''
        signal = [0] + [1 if float(indicator.loc[index]) > 0 and float(indicator.loc[index-1]) < 0
                        else -1 if float(indicator.loc[index]) < 0 and float(indicator.loc[index-1]) > 0  
                        else 0 for index in indicator.index[1:]]

        '''
            if signal not 0, fetch all users 
            GET /user_stocks (argument: stock id)
        '''
        if signal[-1] is not 0:
            '''
                If Non Zero Signal
                Make Transaction with 
                POST /transactions (args: user_id, stock_id)
            '''    
        
            if signal[-1] == 1:
                side = 'BUY'
                user_stocks.append({})

            if signal[-1] == -1:
                side = 'SELL'

            user_list = [user_stock for user_stock in user_stocks if user_stock['stock_id'] == stock['id'] and user_stock['date_closed']== None ]


            for user_stock in user_list:



            for user_stock in user_stocks:
                 = list()
                '''if user has stock with matching id, send a message to transaction-ms'''
                if user_stock['stock_id'] == stock['id']:
                    user_list.append()
                    
                    '''check if user has previous open position, close it'''
                    if user_stock['open_price'] is not 'null':
                        
                        user_stock['close_price'] = 50

                    else:
                        user_stock['close_price'] = 50

                    # user_stock['close_price'] = 50        

                # exchange.dapiPrivate_post_order({'symbol':,
                #                                 'type':"MARKET",
                #                                 'side':side,
                #                                 'positionSide':'BOTH' ,
                #                                 'quantity':open_position_amount})
        

            


                






'''
    
'''



    '''
    update through PUT /stocks/<stock_id>
    '''
    return df_dict
    