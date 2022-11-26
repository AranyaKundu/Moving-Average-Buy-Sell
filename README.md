# Moving-Average-Buy-Sell <br>
Python based simulation for moving average trading strategy. <br>
The idea is to decide buy or sell of a stock based on dual moving average crossover. One moving average chosen is 30 days (1 month) and the second moving average is 90 days (3 months).
There is a dashboard that lets the user to choose whichever stock they want to look, visualize the performance of the stock over the past three years. The dashboard also has a slider with which user can change the moving average window from 7 days (1 week) to 365 days (1 year) [May provide suggestions if the max should be limited to 252].<br>
The dashboard is built using Shiny for Python which itself is in a very nascent stage and still under development, so things might work unexpectedly at times. <br>
It breaks when used in double navset, so I could not include any other trading strategies. There might be workarounds available though. <br>
I have used pandas_datareader module to import yahoo finance data. Same can be done using "Alpha Vantage", "IEX Cloud" or any other API key. <br>
Similar strategy tutorials can be easily found on YouTube. However, the Python for Shiny community is really small as of now (Not much in YouTube also)!
