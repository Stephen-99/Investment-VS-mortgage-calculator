
#can turn these into named cmd line args with default valeus when not provided
INCOME = 100000
YEARS_TO_COMPARE = 10
WEEKLY_RENT = 450
FORTNIGHTLY_EXPENSES_INCL_TAX = 2000
INITIAL_CAPITAL = 90000
HOUSE_PRICE = 500000
HOUSE_INTEREST_RATE = 6 #annual %
STOCK_RETURN_RATE = 8   #avg annual % return
HOUSE_APPRECIATION = 3  #annual average inc in value

#Could also try a certain pertencage of loan paid of or somethign
#Better would be to work backwards and calculate the optimal value.
#Run it as a param sweep? start with big steps and narrow down to the optimal value
MONTHS_TO_SWITCH_MORTGAGE = 6

INCREASE_INCOME = False
INCOME_INCREASE_RATE = 3  #Annual average inc

#Everything ic compounded fortnightly
#Can create an optional toggle to income increase and calc for it only at the start of a year.
def main():
    allStocksVal = AllInStocks()
    minMortgageVal = MinimumMortgageRestInStocks()
    allMortgageVal = AllInMortgage()
    switchVal = AllInMortgage_SwitchToMinimum()

    print(f"Total Value when all in stocks: \t\t\t{allStocksVal}\n" +
          f"Total Value when min Mortgage: \t\t\t{minMortgageVal}\n" +
          f"Total Value when all in Mortgage \t\t\t{allMortgageVal}\n" +
          f"Total Value when switching: \t\t\t{switchVal}")


def AllInStocks():
    pass

def MinimumMortgageRestInStocks():
    pass

def AllInMortgage():
    pass

def AllInMortgage_SwitchToMinimum():
    pass







if __name__ == "__main__":
    main()