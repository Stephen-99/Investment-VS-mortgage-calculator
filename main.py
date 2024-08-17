
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

    print(f"Total Value when all in stocks: \t\t{formatCurrency(allStocksVal)}\n" +
          f"Total Value when min Mortgage: \t\t\t{formatCurrency(minMortgageVal)}\n" +
          f"Total Value when all in Mortgage \t\t{formatCurrency(allMortgageVal)}\n" +
          f"Total Value when switching: \t\t\t{formatCurrency(switchVal)}")


#Remember to modularise stuff! a lot of them do similare calculations, re-use stuff!
def AllInStocks():
    rent = WEEKLY_RENT * 2
    expenses = FORTNIGHTLY_EXPENSES_INCL_TAX
    income = INCOME
    totalCosts = rent + expenses
    leftOver = income/26 - totalCosts

    value = INITIAL_CAPITAL
    for ii in range(YEARS_TO_COMPARE*26):
        if INCREASE_INCOME and ii % 26 == 0:
            income = income * (1 + INCOME_INCREASE_RATE/100)
            leftOver = income/26 - totalCosts
        value = value * (1 + (STOCK_RETURN_RATE/100/26)) + leftOver

    return value

def MinimumMortgageRestInStocks():
    pass

def AllInMortgage():
    pass

def AllInMortgage_SwitchToMinimum():
    pass


def formatCurrency(amount):
    if amount != None:
        return '${:,.2f}'.format(amount)




if __name__ == "__main__":
    main()