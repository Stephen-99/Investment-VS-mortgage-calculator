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
HOUSES_NEW_VALUE = HOUSE_PRICE * (1 + HOUSE_APPRECIATION/100) ** YEARS_TO_COMPARE

#Everything is compounded fortnightly
def main():
    allStocksVal = AllInStocks()
    minMortgageVal = MinimumMortgageRestInStocks()
    allMortgageVal = AllInMortgage()
    switchVal = AllInMortgage_SwitchToMinimum()

    #TODO include printout of house's new val as well as the split in house and stocks where relevant.
    print(f"Houses updated value after {YEARS_TO_COMPARE} years: \t\t{formatCurrency(HOUSES_NEW_VALUE)}\n")
    print(f"Total Value when all in stocks: \t\t{formatCurrency(allStocksVal)}\n" +
          f"Total Value when min Mortgage: \t\t\t{formatCurrency(minMortgageVal)}\n" +
          f"Total Value when all in Mortgage \t\t{formatCurrency(allMortgageVal)}\n" +
          f"Total Value when switching: \t\t\t{formatCurrency(switchVal)}")

def AllInStocks():
    rent = WEEKLY_RENT * 2
    expenses = FORTNIGHTLY_EXPENSES_INCL_TAX
    totalCosts = rent + expenses
    
    return calcStocksAmount(INITIAL_CAPITAL, totalCosts)

def MinimumMortgageRestInStocks():
    mortgageRepayments = 1135   #TODO find an alg to calc this...
    expenses = FORTNIGHTLY_EXPENSES_INCL_TAX
    totalCosts = mortgageRepayments + expenses

    stocksVal = calcStocksAmount(0, totalCosts)
    mortgageVal = calcMortgage(mortgageRepayments)

    return HOUSES_NEW_VALUE - mortgageVal + stocksVal

def AllInMortgage():
    #TODO: doesn't factor in changing income...
    return HOUSES_NEW_VALUE - calcMortgage(INCOME/26 - FORTNIGHTLY_EXPENSES_INCL_TAX)
    
    #Factor in investing in stocks if it's paid off within the timeframe.

def AllInMortgage_SwitchToMinimum():
    pass


#  ~~~~~~~~  HELPER FUNCTIONS ~~~~~~~~  #


def calcMortgage(repaymentAmount):
    mortgageVal = HOUSE_PRICE - INITIAL_CAPITAL
    for ii in range (YEARS_TO_COMPARE*26):
        mortgageVal = (mortgageVal - repaymentAmount) * (1 + HOUSE_INTEREST_RATE/100/26)
    return mortgageVal

def calcTimeToPayOffMortgage(repaymentAmount):
    mortgageVal = HOUSE_PRICE - INITIAL_CAPITAL
    fortnights = 0
    while mortgageVal > 0:
        fortnights += 1
        mortgageVal = (mortgageVal - repaymentAmount) * (1 + HOUSE_INTEREST_RATE/100/26)

    return fortnights, mortgageVal



def calcStocksAmount(initialVal, totalCosts):
    income = INCOME
    leftOver = income/26 - totalCosts

    value = initialVal
    for ii in range(YEARS_TO_COMPARE*26):
        value = value * (1 + (STOCK_RETURN_RATE/100/26)) + leftOver
        if INCREASE_INCOME and (ii+1) % 26 == 0:
            income = income * (1 + INCOME_INCREASE_RATE/100)
            leftOver = income/26 - totalCosts

    return value

def formatCurrency(amount):
    if amount != None:
        return '${:,.2f}'.format(amount)




if __name__ == "__main__":
    main()