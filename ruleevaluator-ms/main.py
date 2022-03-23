from datetime import datetime
import pandas
import ccxt


def rule_evaluator(event,context):
    '''
        Stateless Function to fetch latest price data of all stocks
        Event/Trigger: Cloud Scheduler

    '''


   min_input_length =   np.max([float(strat_params['fast_ema']),float(strat_params['slow_ema'])])

    if len(list(current_input['closes'].values))<min_input_length:
        return "INPUT HAS TOO FEW ELEMENTS"
    
    closes = current_input['closes'].astype(float)
    datetimes = current_input['datetime']
    # closes = closes[:-1]
    # closes['close'] = closes['close'].astype(float)

    indicator = pd.DataFrame(ema(closes.tolist(),strat_params['fast_ema']) - ema(closes.tolist(),strat_params['slow_ema']),columns=['ema_diff'])
    p = strat_params['slow_ema']+1
    closes = closes[p:].reset_index(drop=True)
    indicator = indicator[p:].reset_index(drop=True)
    datetimes = datetimes[p:].reset_index(drop=True)
    signal = [0] + [1 if float(indicator.loc[index]) > 0 and float(indicator.loc[index-1]) < 0 else -1 if float(indicator.loc[index]) < 0 and float(indicator.loc[index-1]) > 0  else 0 for index in indicator.index[1:]]



    '''
        Stock List and Corresponding Prices to be fetched from GET /stocks
    '''
    stock_list=['BTCUSDT','ETHUSDT','BNBUSDT']
    df_dict = {'BTCUSDT':[],
                'ETHUSDT':[],
                'BNBUSDT':[]}


    '''Hard Coded Parameters: 
            Number of Candles, 
            Interval, 
            User ID/Pwd, 
            Whether to Fetch the Last Price 
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
    


    '''
        For Each Stock: Store the fetched Price Values and Datetimes as a Pandas Dataframe 
    '''
    df_dict = dict()
    for symbol in stock_list:    
        if last_incomplete_candle == False:
            closes = [[datetime.datetime.utcfromtimestamp(float(elem[0]) / 1000.),elem[4]] 
            for elem in exchange.fapiPublic_get_klines({'symbol':symbol,'interval':interval})][-candles:-1]
        if last_incomplete_candle == True:
            closes = [[datetime.datetime.utcfromtimestamp(float(elem[0]) / 1000.),elem[4]] 
            for elem in exchange.fapiPublic_get_klines({'symbol':symbol,'interval':interval})][-(candles-1):]
        dates = [elem[0] for elem in closes]
        values = [float(elem[1]) for elem in closes]
        df = pandas.DataFrame([(elem[0],elem[1]) for elem in zip(dates,values)],columns=['datetime','closes'])
        df_dict[symbol]=df
    

    '''
    update through PUT /stocks/<stock_id>
    '''
    return df_dict
    