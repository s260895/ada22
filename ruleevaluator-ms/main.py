from datetime import datetime
import pandas
import ccxt
import pyti
import pickle

def rule_evaluator(event,context):
    '''
        Stateless Function to Evaluate Trading Logic on the latest price data
        Event/Trigger: Cloud Scheduler

    '''


    '''
        Stock List and Corresponding Prices to be fetched from GET /stocks
    '''
    stock_list=['BTCUSDT','ETHUSDT','BNBUSDT']
    
    with open('sample_output.pkl', 'rb') as f:
        stock_prices = pickle.load(f)


    '''Hard Coded Parameters: 
            Number of Candles, 
            Interval, 
            User ID/Pwd, 
            Whether to Fetch the Last Price 
            Strategy Name/Description
            Technical Indicators Used
    '''
    candles = 50
    interval = '1h'
    exchange= ccxt.binance({
                        'apiKey': 'INH9JYsd4Cu3kMPoONiCVHP3KlACsg3F4ehDN1cburoKohsARMpZGcq4PnQoqzyF',
                        'secret': 'FSVMXANswsGOj3B4Oi4NSDOlX5fsvWOJ3s56DQsWvJTjLhSuPyq1aFLbFEWoOrMt',
                        'enableRateLimit': True, 
                        'options': {'defaultType': 'future'},
                        'hedgeMode':True
                        })
    last_incomplete_candle = False
    strategy_params = {
        'strat_name':'ema_cross_over_under'
        'technical_indicators': {'fast_ema':4,'slow_ema':20},



    }

    min_input_length =   np.max([float(strategy_params['technical_inidcators']['fast_ema']),float(strategy_params['technical_inidcators']['slow_ema'])])

    '''
        for each stock
    '''
    for stock in stock_list:   

        if len(list(stock_prices[stock]['closes'].values))<min_input_length:
            return "INPUT HAS TOO FEW ELEMENTS"

        closes = stock_prices[stock]['closes'].astype(float)
        datetimes = stock_prices[stock]['datetime']
        # closes = closes[:-1]
        # closes['close'] = closes['close'].astype(float)

        '''Calculate "Aggregate" Indicator from all Technical Indicators'''
        indicator = pandas.DataFrame(pyti.ema(closes.tolist(),strategy_params['technical_indicators']['fast_ema'])
                                - pyti.ema(closes.tolist(),strategy_params['slow_ema']),
                                columns=['ema_diff'])
        '''Reduce Length of All Columns'''
        closes = closes[(min_input_length+1):].reset_index(drop=True)
        indicator = indicator[(min_input_length+1):].reset_index(drop=True)
        datetimes = datetimes[(min_input_length+1):].reset_index(drop=True)
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
            
            '''Go Long / BUY Stock'''
            '''Go Short / SELL Stock'''
            
            while True:
            try:
                exchange.dapiPrivate_post_order({'symbol':symbol,
                                                'type':"MARKET",
                                                'side':close_side,
                                                'positionSide':'BOTH' ,
                                                'quantity':open_position_amount})
                break
            except Exception as e:
                print("Error while trying to close open order for "+str(asset_name)+": "+str(e))
                print("Retrying in 60 Seconds...")
                time.sleep(60)
        

            


                






'''
    
'''



    '''
    update through PUT /stocks/<stock_id>
    '''
    return df_dict
    