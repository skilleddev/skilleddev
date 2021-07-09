import numpy as np

class MultidimensionalTransdimensional(QCAlgorith):

    def Initalize(self):
        self.SetCash(100000)

        self.SetStartDate(2021,7,8)
        self.SetEndDate(2021,7,9)

        self.symbol = self.AddEquity("SPY" Resolution.Daily).Symbol

        self.lookback= 20

        self.ceiling, self.floor = 30, 10

        self.initialStopRisk = 0.98
        self.trailingStopRisk = 0.9

        self.Schedule.On(self.DateRules.Everyday(self,symbol), \
                        self.TimeRules.AfterMarketOpen(self.symbol, 20), \
                        Action(self.EveryMArketOpen))

        def OnData(self, data):
            self.Plot("Data chart", self.symbol, selfSecurities[self.symbol].Close)

        def EveryMarketOpen(self):
            close = self.History(self.symbol, 31, Resolution.Daily)["close"]
            todayvol= np.std(close[1:31])
            yesterdayvol = np.std(close[0:30])
            deltavol = (todayvol - yesterdayvol) / todayvol
            sel.lookback = round(self.lookback * (1 + deltavol))

            if self.lookback > self.ceiling: 
                self.lookback = self.ceiling
            elif self.lookback < self.floor:
                self.lookback = self.floor

            self.high = self.History(self.symbol, self.lookback, Resolution.Daily)["high"]

            if not self.Securities[self.symbol].Invested and \
                self.Securities[self.symbol].Close >= max(self.high[:-1]):
               self.SetHoldings(self.symbol, 1)
               self.breakoutlvl = max(self.high[:-1])
               self.highestPrice = self.breakoutlvl

            if self.Securities[self.symbol].Invested:
                if not self.Transsactiond.GetOpenOrders(self.symbol):
                    self.stopMarketTicket = self.StopMarketOrder(self.symbol, \
                                            -self.Portfolio[self.symbol].Quantity, \
                                            self.initialStopRisk * self.breakoutlvl)
                
                if self.Securities[self.symbol].Close > self.highestPRice and \
                    self.initialStopRisk * self.breakoutlvl < self.Securities[self.symbol].Close * self.trailingStopRisk:
                self.highestPrice = self.Securities[self.symbol].Close 
                updateFields = UpdateOrderFields()
                updateFields.StopPrice = self.Securities[self.symbol].CLose * self.trailingStopRisk
                self.stopMarketTicket.Update(update.Fields)

                self.Debug(updateFields.StopPrice)

            self.Plot("Data Char", "Stop Price", self.stopMarketTicket.Get(OrderField.StopPrice))
