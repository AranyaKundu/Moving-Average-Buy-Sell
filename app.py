from shiny import *
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader as dr
import pandas as pd


beginDate = dt.datetime.now() - dt.timedelta(days=365 * 3)
endDate = dt.datetime.now()
rfpath = "e:\\Python Learning\\Quant Finance\\algorithmic-trading-python-master\\starter_files\\sp_500_stocks.csv"
stocks = pd.read_csv(rfpath)
stock = stocks['Ticker'].tolist()


ui = ui.page_fluid(
        ui.tags.style(
            """
            .container-fluid{
                overflow: hidden;
                margin: 0;
                padding-bottom: 10px;
                padding-top: -20px;
                background-color: black;
                box-sizing: border-box;
                width: 100%;
            }
            .container-fluid h1{
                text-align: center;
                font-style: italic;
                color: white;
            }
            .new-container{
                background-color: white;
            }
            .myNav a{
                font-size:20px;
                font-family: Lucida;
            }
            .myNav :hover{
                background-color: #d0d0d0;
            }
            """
        ),
        ui.navset_pill_card(
            ui.nav_control({"class": "myNav"},
                ui.a("Movinfg Average Investment Simulation Strategy", href = "#", style="color: black")
            ),
            ui.nav_spacer(),
            ui.nav("Data Visualization",
                ui.layout_sidebar(
                    ui.panel_sidebar(
                        ui.input_select("ticker", "Stock Name", stock),
                        ui.input_slider("ma_1", "Moving Average 1", 7, 365, 30),
                        ui.input_slider("ma_2", "Moving Average 2", 7, 365, 90)
                    ), 
                    ui.panel_main(ui.output_plot("my_plot_1")
                    )
                )
            ),
            ui.nav("Buy/Sell Strategy",
                ui.layout_sidebar(
                    ui.panel_sidebar(
                        ui.input_select("ticker_1", "Stock Name", stock),
                        ui.input_slider("ma_3", "Moving Average 1", 7, 365, 30),
                        ui.input_slider("ma_4", "Moving Average 2", 7, 365, 90)
                    ), 
                    ui.panel_main(ui.output_plot("my_plot_2"),
                    )
                )
            ),
            ui.nav("Data Table",
                ui.page_fluid({"class":"new-container"},
                    ui.row(
                        ui.column(2, ui.input_select("ticker_2", "Stock Name", stock)),
                        ui.column(2, ui.input_numeric("row_count", "Number of rows", 7)),
                        ui.column(2, ui.input_radio_buttons("top", "Part of Table", {"Top" : "Head Part", "Bottom": "Tail Part"})),
                        ui.column(3, ui.input_slider("ma_5", "Moving Average 1", 7, 365, 30)),
                        ui.column(3, ui.input_slider("ma_6", "Moving Average 2", 7, 365, 90))
                    ),
                    ui.row(
                        ui.column(2),
                        ui.column(8, ui.output_table("table_1"))
                    )
                )
            )
        )
    )



def server(input, output, session):

    @output
    @render.plot(alt="A Visualization")
    def my_plot_1() -> object:
        data = dr.DataReader(input.ticker(), 'yahoo', beginDate, endDate)
        data[f'MAP_{input.ma_1()}'] = data['Adj Close'].rolling(window = input.ma_1()).mean()
        data[f"MAP_{input.ma_2()}"] = data["Adj Close"].rolling(window = input.ma_2()).mean()
        data = data.iloc[input.ma_2():]

        fig_1 = plt.style.use("dark_background")
        plt.plot(data['Adj Close'], label = f"Share Price {input.ticker()}", color = "aliceblue")
        plt.plot(data[f'MAP_{input.ma_1()}'], label = f'MAP_{input.ma_1()}', color = "purple")
        plt.plot(data[f"MAP_{input.ma_2()}"], label = f"MAP_{input.ma_2()}", color = "green")
        plt.legend(loc = "upper left")
        return fig_1

    @output
    @render.plot(alt = "A buy/sell Strategy")
    def my_plot_2() -> object:
        st_data = dr.DataReader(input.ticker_1(), 'yahoo', beginDate, endDate)
        st_data[f'MAP_{input.ma_3()}'] = st_data['Adj Close'].rolling(window = input.ma_3()).mean()
        st_data[f"MAP_{input.ma_4()}"] = st_data["Adj Close"].rolling(window = input.ma_4()).mean()
        st_data = st_data.iloc[input.ma_4():]
        buy, sell =[], []
        decision = 0
        for i in range (len(st_data)):
            if st_data[f'MAP_{input.ma_3()}'].iloc[i] > st_data[f'MAP_{input.ma_4()}'].iloc[i] and decision != 1:
                buy.append(st_data['Adj Close'].iloc[i])
                sell.append(float('nan'))
                decision = 1
            elif st_data[f'MAP_{input.ma_3()}'].iloc[i] < st_data[f'MAP_{input.ma_4()}'].iloc[i] and decision != -1:
                buy.append(float('nan'))
                sell.append(st_data['Adj Close'].iloc[i])
                decision = -1
            else:
                buy.append(float('nan'))
                sell.append(float('nan'))

        st_data['Buy Decisions'] = buy
        st_data['Sell Decisions'] = sell

        fig_2 = plt.style.use("dark_background")
        plt.plot(st_data['Adj Close'], label = f"Share Price {input.ticker_1()}", color = "white", lw = 0.5)
        plt.plot(st_data[f'MAP_{input.ma_3()}'], label = f"MAP_{input.ma_3()}", color = "purple")
        plt.plot(st_data[f'MAP_{input.ma_4()}'], label = f"MAP_{input.ma_4()}", color = "orange")
        plt.scatter(st_data.index, st_data['Buy Decisions'], label = "Buy Decisions", marker = "^", color = "green", lw = 2)
        plt.scatter(st_data.index, st_data['Sell Decisions'], label = "Sell Decisions", marker = "v", color = "red", lw = 2)
        plt.legend(loc = "upper left")
        return fig_2


    @output
    @render.table
    def table_1():
        stock_data = dr.DataReader(input.ticker_2(), 'yahoo', beginDate, endDate)
        stock_data[f'MAP_{input.ma_5()}'] = stock_data['Adj Close'].rolling(window = input.ma_5()).mean()
        stock_data[f"MAP_{input.ma_6()}"] = stock_data["Adj Close"].rolling(window = input.ma_6()).mean()
        stock_data.reset_index(inplace=True)
        stock_data = stock_data.iloc[input.ma_6():]
        if (input.top() == 'Top'):
            return stock_data.head(input.row_count()) 
        else: return stock_data.tail(input.row_count())

app = App(ui, server, debug = True)