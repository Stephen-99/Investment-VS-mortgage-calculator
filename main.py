INCOME = 100000
YEARS_TO_COMPARE = 30
WEEKLY_RENT = 450
FORTNIGHTLY_EXPENSES_INCL_TAX = 2000
INITIAL_CAPITAL = 90000
HOUSE_PRICE = 500000
HOUSE_INTEREST_RATE = 5  #annual %
STOCK_RETURN_RATE = 8  #avg annual % return
HOUSE_APPRECIATION = 3  #annual average inc in value
RENT_OUT_A_ROOM = True
ROOM_RENT = 200  #Weekly 
YEARS_TO_RENT_ROOM = 5  #Currently doesn't do anything.
INCREASE_INCOME = True
INCOME_INCREASE_RATE = 3  #Annual average inc   THIS IS ACTUALLY A BAD APPROXIMATION. Income increase doesn't compound. 
                          #It also is likely to taper off somewhat. I also don't increase expenses so it's better to use a
                          #lower income increase rate and assume the rest of increased income goes to increased expenses.

#Could also try a certain pertencage of loan paid of or somethign
#Better would be to work backwards and calculate the optimal value.
#Run it as a param sweep? start with big steps and narrow down to the optimal value
MONTHS_TO_SWITCH_MORTGAGE = 6


HOUSES_NEW_VALUE = HOUSE_PRICE * (1 + HOUSE_APPRECIATION/100) ** YEARS_TO_COMPARE


# Takeaways. When homeloan interest rates are lower, a home loan is worthwhile. At higher interest rates, they become a worse investment.
# Stocks always win out in the long term. It's an asset being built that continues to compound. If a mortgage repayment is not much more than rent,
# it is worth while. in the long term stocks win out, but the amount is not enough to care about and in the medium ish term, the house wins out.
# The question is more about what type of lifestyle do you want? The freedom to easily move anywhere, or the stability of your own home and 
# freedom to do with it as you wish?
# This also doesn't factor out renting a room in your house. That could swing the balance even more in favour of buying

#Everything is compounded fortnightly
def main():
    allStocksVal = AllInStocks()
    minMortgageVal = MinimumMortgageRestInStocks()
    allMortgageVal = AllInMortgage()
    switchVal = AllInMortgage_SwitchToMinimum()

    #TODO include printout of house's new val as well as the split in house and stocks where relevant.
    #Also years till loan paid off
    print(f"Houses updated value after {YEARS_TO_COMPARE} years: \t\t{formatCurrency(HOUSES_NEW_VALUE)}\n")
    print(f"Total Value when all in stocks: \t\t{formatCurrency(allStocksVal)}\n" +
          f"Total Value when min Mortgage: \t\t\t{formatCurrency(minMortgageVal)}\n" +
          f"Total Value when all in Mortgage \t\t{formatCurrency(allMortgageVal)}\n" +
          f"Total Value when switching: \t\t\t{formatCurrency(switchVal)}")
    print(formatCurrency(calcMinimumRepayments()))

def AllInStocks():
    rent = WEEKLY_RENT * 2
    expenses = FORTNIGHTLY_EXPENSES_INCL_TAX
    totalCosts = rent + expenses
    
    return calcStocksAmount(INITIAL_CAPITAL, totalCosts)

def MinimumMortgageRestInStocks():
    mortgageRepayments = calcMinimumRepayments()
    expenses = FORTNIGHTLY_EXPENSES_INCL_TAX
    totalCosts = mortgageRepayments + expenses

    if RENT_OUT_A_ROOM:
        totalCosts -= ROOM_RENT * 2

    stocksVal = calcStocksAmount(0, totalCosts)
    mortgageVal = calcMortgage(mortgageRepayments)

    return HOUSES_NEW_VALUE - mortgageVal + stocksVal

def AllInMortgage():
    expenses = FORTNIGHTLY_EXPENSES_INCL_TAX
    if RENT_OUT_A_ROOM:
        expenses -= 2* ROOM_RENT
    fortnightsToPayOff, mortgageVal = calcTimeToPayOffMortgage(expenses)

    if not fortnightsToPayOff:
        return HOUSES_NEW_VALUE - mortgageVal
    #Invest in stocks once home is paid off
    return HOUSES_NEW_VALUE + calcStocksAmount(-mortgageVal, FORTNIGHTLY_EXPENSES_INCL_TAX, fortnightsToInvest=YEARS_TO_COMPARE*26 - fortnightsToPayOff )

def AllInMortgage_SwitchToMinimum():
    pass


#  ~~~~~~~~  HELPER FUNCTIONS ~~~~~~~~  #

#TODO create a function to update costs that takes into account the number of years. Calcs new income if needed and factors in renting a room if needed
    #Each thingo will need to pass through a function to calculate costs as it is different for each.

def calcMinimumRepayments(years=30):
    rate = HOUSE_INTEREST_RATE/100/26
    paymentPeriods = years*26
    return (HOUSE_PRICE-INITIAL_CAPITAL) * (rate * (1+rate)**paymentPeriods) / ((1+rate)**paymentPeriods - 1) + 3

def calcMortgage(repaymentAmount):
    mortgageVal = HOUSE_PRICE - INITIAL_CAPITAL
    for ii in range (YEARS_TO_COMPARE*26):
        mortgageVal = (mortgageVal - repaymentAmount) * (1 + HOUSE_INTEREST_RATE/100/26)
    return mortgageVal

def calcTimeToPayOffMortgage(expenses):
    income = INCOME
    repaymentAmount = income/26 - expenses

    mortgageVal = HOUSE_PRICE - INITIAL_CAPITAL
    fortnights = 0
    while mortgageVal > 0:
        fortnights += 1
        mortgageVal = (mortgageVal - repaymentAmount) * (1 + HOUSE_INTEREST_RATE/100/26)
        if fortnights == YEARS_TO_COMPARE * 26:
            return None, mortgageVal
        if INCREASE_INCOME and (fortnights) % 26 == 0:
            income = income * (1 + INCOME_INCREASE_RATE/100)
            repaymentAmount = income/26 - expenses

    return fortnights, mortgageVal

def calcStocksAmount(initialVal, totalCosts, fortnightsToInvest=YEARS_TO_COMPARE*26):
    income = INCOME
    leftOver = income/26 - totalCosts

    value = initialVal
    for ii in range(fortnightsToInvest):
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