import backtrader as bt
import cdd_feed
from btc_strategy import SMACrossover, HODL, MeanReversion
import binance_feed
import binance_csv_feed


CASH = 1000000
COMMISSION = 0.001

def main():
    df = binance_csv_feed.load_data("BTCUSDT")
    data = bt.feeds.PandasData(dataname=df,
                               open='Open',
                               high='High',
                               low='Low',
                               close='Close',
                               volume=None,
                               openinterest=None,
                               timeframe=bt.TimeFrame.Minutes,
                               compression=1,
                               )

    # Create a Cerebro engine instance for backtrader
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(CASH)
    # cerebro.broker.setcommission(commission=COMMISSION)
    # Add the data feed and add some analyzers for statistic info
    cerebro.adddata(data)
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='areturn')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=3.95)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='myanalyzer')

    cerebro.addstrategy(MeanReversion)  # Add the strategy to Cerebro
    results = cerebro.run()  # Run the strategy
    trade_analyzer = results[0].analyzers.getbyname('myanalyzer')
    print(trade_analyzer.get_analysis())  # This should print the dictionary
    # print(f"Sharpe: {results[0].analyzers.sharperatio.get_analysis()['sharperatio']:.3f}")
    print(f"Norm. Annual Return: {results[0].analyzers.returns.get_analysis()}")
    print(results[0].analyzers.getbyname('areturn').get_analysis())
    print(f"Max Drawdown: {results[0].analyzers.drawdown.get_analysis()['max']['drawdown']:.2f}%")


if __name__ == "__main__":
    main()
