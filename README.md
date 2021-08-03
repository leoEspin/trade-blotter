# Trade blotter

The goal is to consume a trade blotter for a portfolio
and calculate various financial metrics, chiefly the profit made (or
loss taken).

A trade blotter contains a record of all trades that were executed on an
exchange (also called a 'fill') for a given portfolio. Each line in the
trade blotter provides the details of a fill.

Data Format
-----------

The format of the blotter is a CSV file that contains the following
fields:

LocalTime,Symbol,EventType,Side,FillSize,FillPrice,FillExchange

9:30:00.000,AES,TRADE,t,100,11.14,NYSE

9:30:01.000,AES,TRADE,b,100,11.16,NASDAQ

9:30:02.000,CX,TRADE,b,100,7.5,NASDAQ

9:30:03.000,CX,TRADE,t,100,7.51,NASDAQ

9:30:04.000,CX,TRADE,b,200,7.5,NASDAQ

9:30:05.000,CX,TRADE,t,100,7.5,NASDAQ

9:30:06.000,CX,TRADE,t,200,7.48,NASDAQ

9:30:07.000,AIG,TRADE,t,100,56.395,NASDAQ

9:30:08.000,AIG,TRADE,t,100,56.39,NYSE

9:30:09.000,AIG,TRADE,b,100,56.38,NASDAQ

9:30:10.000,AIG,TRADE,b,100,56.38,NASDAQ

9:30:11.000,AIG,TRADE,t,100,56.72,NASDAQ

 

Fields Description
------------------

The following describes each of the columns:

1.  LocalTime (string): Time of the order event in HH:MM:SS.millisecs
2.  Symbol (string): Stock ticker
3.  EventType: The specific event type
    -   This project is only concerned with the TRADE events
4.  Side (b\|s\|t): Tells whether the original order is a buy, sell, or
    short sell order
    -   b: Buy
    -   s: Sell
    -   t: Short sell
        -   For this project, you can treat Short Sell orders as Sell
            orders
5.  FillSize (unsigned integer): Number of shares that were filled
6.  FillPrice (double): Price at which the trade was executed
7.  FillExchange (string): Name of exchange where the trade was filled


## PROJECT DEFINITION

The script `calcStats.py` consumes the above CSV file and produces an
enriched version of the CSV file with the additional columns described
below.

The python script is callable in the following ways:

1.  From the command line via:

```{bash}
calcStats.py --inputFile=trades.csv --outputFile=enrichedTrades.csv
```

2.  By importing it and calling:

```{bash}
    from calcStats import calcTradeStats

    calcTradeStats(inputFile, outputFile)
```

The inputFile is a CSV file in the format described above.


The output is composed of two components:

1.  An enriched version of the input CSV file which adds the columns
    described below to the original file and populates it on a
    trade-by-trade basis
2.  A summary of relevant statistics as described below

 

Enriched Version Columns
------------------------

The output is an enriched version of the input CSV file which
adds the following columns to the original file and populates it on
a **trade-by-trade** basis:

(note the list of additional columns starts at 'h' to denote their
location at the end of the line).
 

0.  SymbolBought
    -   Number of shares of the stock bought
1.  SymbolSold
    -   Number of shares of the stock sold
2.  SymbolPosition
    -   Number of shares of a stock the portfolio currently holds or
        owes
    -   Dependent on the number of shares we bought vs. sold, the
        position can be:
        1.  Long (positive number) if we bought more shares than we sold
        2.  Short (negative number) if we sold more than we bought
        3.  Flat (zero) if we do not have a position in the given stock
3.  SymbolNotional
    -   Value of the shares bought or sold, == FillSize \* FilledPrice
4.  ExchangeBought
    -   Number of shares bought on the current exchange, across all
        symbols
5.  ExchangeSold
    -   Number of shares sold on the current exchange, across all
        symbols
6.  TotalBought
    -   Total number of shares bought across all symbols
7.  TotalSold
    -   Total number of shares sold across all symbols
8.  TotalBoughtNotional
    -   Total value (SymbolNotional) of all shares bought across all
        symbols
9.  TotalSoldNotional
    -   Total value (SymbolNotional) of all shares sold across all
        symbols


The following is enriched output for the sample data in the Data Format
section above:


LocalTime,Symbol,EventType,Side,FillSize,FillPrice,FillExchange,SymbolBought,SymbolSold,SymbolPosition,SymbolNotional,ExchangeBought,ExchangeSold,TotalBought,TotalSold,TotalBoughtNotional,TotalSoldNotional

9:30:00.000,AES,TRADE,t,100,11.14,NYSE,0,100,-100,1114.00,0,100,0,100,0.00,1114.00

9:30:01.000,AES,TRADE,b,100,11.16,NASDAQ,100,100,0,1116.00,100,0,100,100,1116.00,1114.00

9:30:02.000,CX,TRADE,b,100,7.50,NASDAQ,100,0,100,750.00,200,0,200,100,1866.00,1114.00

9:30:03.000,CX,TRADE,t,100,7.51,NASDAQ,100,100,0,751.00,200,100,200,200,1866.00,1865.00

9:30:04.000,CX,TRADE,b,200,7.50,NASDAQ,300,100,200,1500.00,400,100,400,200,3366.00,1865.00

9:30:05.000,CX,TRADE,t,100,7.50,NASDAQ,300,200,100,750.00,400,200,400,300,3366.00,2615.00

9:30:06.000,CX,TRADE,t,200,7.48,NASDAQ,300,400,-100,1496.00,400,400,400,500,3366.00,4111.00

9:30:07.000,AIG,TRADE,t,100,56.40,NASDAQ,0,100,-100,5640.00,400,500,400,600,3366.00,9751.00

9:30:08.000,AIG,TRADE,t,100,56.39,NYSE,0,200,-200,5639.00,0,200,400,700,3366.00,15390.00

9:30:09.000,AIG,TRADE,b,100,56.38,NASDAQ,100,200,-100,5638.00,500,500,500,700,9004.00,15390.00

9:30:10.000,AIG,TRADE,b,100,56.38,NASDAQ,200,200,0,5638.00,600,500,600,700,14642.00,15390.00

9:30:11.000,AIG,TRADE,t,100,56.72,NASDAQ,200,300,-100,5672.00,600,600,600,800,14642.00,21062.00