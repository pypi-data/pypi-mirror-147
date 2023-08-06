import pandas as pd
import numpy as np

TradeLIST = []
AnalysisLIST = []

from DirectoryFormulas import *

def Statistics_OPT(opt_runs, margin, Mininbars = 0):
    st0 = [s[0] for s in opt_runs]
    for s in st0:
        exp_close_od = s.analyzers.EX_CLOSE_PNL.get_analysis()  # OrderedDict
        ExpClosedf = pd.DataFrame(list(exp_close_od.items())) # not export != from Backtesting
        ExpClosedf.columns = ['time', 'exp_close']
        ExpClosedf = ExpClosedf.set_index('time', drop=True)

        MaxValue = max(ExpClosedf['exp_close'])
        MinValue = min(ExpClosedf['exp_close'])

        countneg = sum(map(lambda x: x < 0, ExpClosedf['exp_close']))
        countzero = sum(map(lambda x: x == 0, ExpClosedf['exp_close']))
        count_perc = round(DivByZero_int(countneg, (len(ExpClosedf['exp_close']) - countzero)), 5)
        # count_perc = "{:.2%}".format(count_perc)

        trade_list = s.analyzers.trade_list.get_analysis()
        TradeLIST.append(trade_list)
        TradeListDF = pd.DataFrame(trade_list)

        try:
            totalnet_pnl = round((s.analyzers.TradeAnalyzer.rets.pnl.net.total), 2)
        except:
            totalnet_pnl = np.nan

        ##Number of Trades
        try:
            TotalTrades = s.analyzers.SQN.rets.trades
        except:
            TotalTrades = 0
            print('No Trades')
        if TotalTrades == 0:
            TotalTrades = np.nan

        if TotalTrades > 0:
            ##  Total won
            try:
                WonTotal = s.analyzers.TradeAnalyzer.rets.won.total
            except:
                WonTotal = 0
                print('No winning trades')

            ##  Total lost
            try:
                LostTotal = s.analyzers.TradeAnalyzer.rets.lost.total
            except:
                LostTotal = 0
                print('No winning trades')

            ##  Pnl won total
            try:
                WonPnlTotal = s.analyzers.TradeAnalyzer.rets.won.pnl.total
            except:
                WonPnlTotal = 0
                print('No profit')

            if WonPnlTotal > 0:
                MaxWinning = s.analyzers.TradeAnalyzer.rets.won.pnl.max

            ##  Pnl lost total
            try:
                LostPnlTotal = s.analyzers.TradeAnalyzer.rets.lost.pnl.total
            except:
                LostPnlTotal = 0
                print('No Losses')

            ##  Won Trades Percentage
            try:
                won_perc = round(
                    DivByZero_int(WonTotal, TotalTrades),
                    3)
                # won_perc = "{:.2%}".format(won_perc)
            except:
                won_perc = 0
                print('No winning trades')

            ### LONG
            try:
                LongTotal = s.analyzers.TradeAnalyzer.rets.long.total
            except:
                LongTotal = 0
                print('No Trades')

            try:
                LongWon = s.analyzers.TradeAnalyzer.rets.long.won
            except:
                LongWon = 0
                print('No Trades')

            try:
                LongPnl = s.analyzers.TradeAnalyzer.rets.long.pnl.total
            except:
                LongPnl = 0
                print('No Trades')

            try:
                LongPnlWon = s.analyzers.TradeAnalyzer.rets.long.pnl.won.total
            except:
                LongPnlWon = 0
                print('No Trades')

            try:
                LongPnlLost = s.analyzers.TradeAnalyzer.rets.long.pnl.lost.total
            except:
                LongPnlLost = 0
                print('No Trades')

            ### SHORT
            try:
                ShortTotal = s.analyzers.TradeAnalyzer.rets.short.total
            except:
                ShortTotal = 0
                print('No Trades')

            try:
                ShortWon = s.analyzers.TradeAnalyzer.rets.short.won
            except:
                ShortWon = 0
                print('No Trades')

            try:
                ShortPnl = s.analyzers.TradeAnalyzer.rets.short.pnl.total
            except:
                ShortPnl = 0
                print('No Trades')

            try:
                ShortPnlWon = s.analyzers.TradeAnalyzer.rets.short.pnl.won.total
            except:
                ShortPnlWon = 0
                print('No Trades')

            try:
                ShortPnlLost = s.analyzers.TradeAnalyzer.rets.short.pnl.lost.total
            except:
                ShortPnlLost = 0
                print('No Trades')

        if TotalTrades == np.nan :
            WonTotal = np.nan
            LostTotal = np.nan
            WonPnlTotal = np.nan
            LostPnlTotal = np.nan
            MaxWinning = np.nan
            won_perc = np.nan
            LongTotal = np.nan
            LongWon = np.nan
            LongPnl = np.nan
            LongPnlWon = np.nan
            LongPnlLost = np.nan
            ShortTotal = np.nan
            ShortWon = np.nan
            ShortPnl = np.nan
            ShortPnlWon = np.nan
            ShortPnlLost = np.nan

        try:
            if TotalTrades > 1:
                if won_perc == 1:
                    ADJ_Wc = ((WonTotal - np.sqrt(WonTotal)) / WonTotal)
                    ADJ_W = ADJ_Wc * WonPnlTotal
                    ADJ_W_BW = ADJ_Wc * (WonPnlTotal - MaxWinning)
                    ADJ_L = 0
                elif won_perc == 0:
                    ADJ_W = 0
                    ADJ_W_BW = 0
                    ADJ_L = ((LostTotal - np.sqrt(LostTotal)) / LostTotal) * LostPnlTotal
                elif won_perc != 0 and won_perc != 1:
                    ADJ_Wc = ((WonTotal - np.sqrt(WonTotal)) / WonTotal)

                    ADJ_W = ADJ_Wc * WonPnlTotal
                    ADJ_W_BW = ADJ_Wc * (WonPnlTotal - MaxWinning)

                    ADJ_L = ((LostTotal - np.sqrt(LostTotal)) / LostTotal) * LostPnlTotal

            elif TotalTrades == 1:
                if won_perc == 1:
                    ADJ_W = WonPnlTotal
                    ADJ_W_BW = (WonPnlTotal - MaxWinning)
                    ADJ_L = 0
                elif won_perc == 0:
                    ADJ_W = 0
                    ADJ_W_BW = 0
                    ADJ_L = LostPnlTotal

            elif TotalTrades == np.nan:
                ADJ_W_BW = np.nan
                ADJ_W = np.nan
                ADJ_L = np.nan

            ADJ_PNL = ADJ_W + ADJ_L
            PROM = round(ADJ_PNL / margin, 3)
            PROM_BW = round((ADJ_W_BW + ADJ_L) / margin, 3)
        except:
            pass

        try:
            if won_perc == 1:
                profitfactor = np.inf
            elif won_perc == 0 :
                profitfactor = -np.inf
            elif won_perc == np.nan:
                profitfactor = np.nan
            else:
                profitfactor = round(
                    DivByZero_int(-WonPnlTotal,LostPnlTotal),3)
        except:
            profitfactor = 0
            print('No Profit')

        ##  -----------------      LONG

        won_long_perc = round(DivByZero_int(LongWon, LongTotal),3)

        if LongTotal == 0:
            won_long_perc = np.nan
        # won_long_perc = "{:.2%}".format(won_long_perc)

        if won_long_perc == 1:
            profitfactorlong = np.inf
        elif won_long_perc == 0 :
            profitfactorlong = -np.inf
        elif won_long_perc == np.nan:
            profitfactorlong = np.nan
        else:
            profitfactorlong = round(DivByZero_int(-LongPnlWon,LongPnlLost),3)

        ##  -----------------      SHORT

        won_short_perc = round(DivByZero_int(ShortWon,ShortTotal),3)
        if ShortTotal == 0:
            won_short_perc = np.nan
        # won_short_perc = "{:.2%}".format(won_short_perc)


        if won_short_perc == 1:
            profitfactorshort = np.inf
        elif won_short_perc == 0 :
            profitfactorshort = -np.inf
        elif won_short_perc == np.nan:
            profitfactorshort = np.nan
        else:
            profitfactorshort = round(DivByZero_int(-ShortPnlWon,ShortPnlLost),
                3)

        try:
            avg_bars_trade = round((TradeListDF['nbars'].mean()) * Mininbars / 60, 2)
        except:
            avg_bars_trade = np.nan

        avg_pnl = round(DivByZero_int(totalnet_pnl, TotalTrades), 3)

        PNL_MDWD = round(DivByZero_int(-totalnet_pnl, MinValue), 3)
        if totalnet_pnl > 0 and MinValue == 0:
            PNL_MDWD = np.inf
        elif PNL_MDWD == 0:
            PNL_MDWD = np.nan

        EXTFACT = round(DivByZero_int(-MaxValue, MinValue), 3)
        if MaxValue > 0 and MinValue == 0:
            EXTFACT = np.inf
        elif MaxValue == 0 and MinValue < 0:
            EXTFACT = -np.inf

        Analysislist = ([totalnet_pnl, won_perc, profitfactor,
                     round(LongPnl, 2), won_long_perc, profitfactorlong,
                     round(ShortPnl, 2), won_short_perc, profitfactorshort,
                     round(MaxValue, 2), round(MinValue, 2), EXTFACT,
                     avg_pnl, avg_bars_trade, count_perc,
                     TotalTrades, round((s.analyzers.SQN.rets.sqn), 2),
                     (s.analyzers.DrawDown.rets.max.moneydown), PNL_MDWD, PROM, PROM_BW])

        AnalysisLIST.append(Analysislist)
    return AnalysisLIST

AnalysisLIST_Index2 = ['PNL', 'Total_Won %', 'ProfitFactor',
                      'PNL_LONG', 'Long_Won %', 'PF_Long',
                      'PNL_SHORT', 'Short_Won %', 'PF_Short',
                      'Max_Pnl', 'Min_Pnl', 'Extremes_Factor',
                      'Avg_pnl', 'Avg Hours', 'Time_Loss%',
                      'Trades', 'SQN',
                      'Max_drawdown', 'PNL/Min_Pnl',
                       'PROM', 'PROM_BWin']

def Trasform_DF_HM(Final_Realized_List, Ind_X_str, Ind_Y_str):

    DF = DataFrame(Final_Realized_List)
    DF.columns = [Ind_X_str, Ind_Y_str, 'PNL']
    HeatMap = DF.pivot_table(index=Ind_X_str, columns=Ind_Y_str, values='PNL', sort=False)
    return DF, HeatMap

def MinutePNLS(MinutePNL_Series, Variables_LIST):
    TEST = (list(MinutePNL_Series))
    AAA = pd.DataFrame(TEST)
    MinutePNLCum_DF = AAA.T
    MinutePNL_DF = MinutePNLCum_DF.diff()
    MinutePNL_DF = MinutePNL_DF.iloc[1:]  # Erase first row of nan after diff()

    # Localize rows and column without all zeroes
    # AAATB = AAATB.loc[(AAATB.sum(axis=1) != 0, (AAATB.sum(axis=0) != 0))]

    MinutePNLCum_DF.columns = Variables_LIST
    MinutePNLCum_DF.info()
    print(MinutePNLCum_DF.tail(2))
    MinutePNL_DF.columns = Variables_LIST
    MinutePNL_DF.info()
    print(MinutePNL_DF.tail(2))
    return MinutePNL_DF, MinutePNLCum_DF

