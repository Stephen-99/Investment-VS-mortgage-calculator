def setConstants():
    global INCOME, INITIAL_TAX, YEARS_TO_COMPARE, WEEKLY_RENT, FORTNIGHTLY_EXPENSES, INITIAL_CAPITAL, HOUSE_PRICE
    global HOUSE_INTEREST_RATE, STOCK_RETURN_RATE, HOUSE_APPRECIATION, RENT_OUT_A_ROOM, ROOM_RENT, YEARS_TO_RENT_ROOM
    global INCREASE_INCOME, INCOME_INCREASE_RATE, MONTHS_TO_SWITCH_MORTGAGE, HOUSES_NEW_VALUE

    INCOME = 100000
    INITIAL_TAX = calculateTax(INCOME)
    YEARS_TO_COMPARE = 30 #Only whole numbers
    WEEKLY_RENT = 450
    FORTNIGHTLY_EXPENSES = 1000
    INITIAL_CAPITAL = 90000
    HOUSE_PRICE = 500000
    HOUSE_INTEREST_RATE = 5  #annual %
    STOCK_RETURN_RATE = 8  #avg annual % return
    HOUSE_APPRECIATION = 3  #annual average inc in value
    RENT_OUT_A_ROOM = True
    ROOM_RENT = 250  #Weekly 
    YEARS_TO_RENT_ROOM = 2
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
    expenses = FORTNIGHTLY_EXPENSES
    totalCosts = rent + expenses
    
    return calcStocksAmount(INITIAL_CAPITAL, totalCosts, stocksOnlyExpenses)

def MinimumMortgageRestInStocks():
    mortgageRepayments = calcMinimumRepayments()
    expenses = FORTNIGHTLY_EXPENSES
    totalCosts = mortgageRepayments + expenses

    if RENT_OUT_A_ROOM:
        totalCosts -= ROOM_RENT * 2

    mortgageVal = calcMortgage(mortgageRepayments)
    stocksVal = calcStocksAmount(0, totalCosts, minimumMortgageCosts)

    return HOUSES_NEW_VALUE - mortgageVal + stocksVal

def AllInMortgage():
    expenses = FORTNIGHTLY_EXPENSES
    if RENT_OUT_A_ROOM:
        expenses -= 2* ROOM_RENT
    fortnightsToPayOff, mortgageVal = calcTimeToPayOffMortgage(expenses)

    if not fortnightsToPayOff:
        return HOUSES_NEW_VALUE - mortgageVal
    #Invest in stocks once home is paid off
    #A little bit broken since it resets the 'year' to 0 in terms of increasing income etc. To fix, should make the update expenses method run fortnightly
    return HOUSES_NEW_VALUE + calcStocksAmount(-mortgageVal, expenses, mortgageCosts, fortnightsToInvest=YEARS_TO_COMPARE*26 - fortnightsToPayOff)

def AllInMortgage_SwitchToMinimum():
    expenses = FORTNIGHTLY_EXPENSES
    if RENT_OUT_A_ROOM:
        expenses -= 2* ROOM_RENT

    repaymentAmount = (INCOME-INITIAL_TAX)/26 - expenses
    mortgageVal = HOUSE_PRICE - INITIAL_CAPITAL
    for ii in range (int(MONTHS_TO_SWITCH_MORTGAGE/12*26)):
        mortgageVal = (mortgageVal - repaymentAmount) * (1 + HOUSE_INTEREST_RATE/100/26)
        if mortgageVal < 0:
            return mortgageVal
        if (ii+1) % 26 == 0:
            repaymentAmount, expenses = updateAmountLeftOver((ii+1)/26, mortgageCosts, expenses)
            #TODO will need to update to /fortnight to allow for switching after so many months
    return mortgageVal


#  ~~~~~~~~  HELPER FUNCTIONS ~~~~~~~~  #


def calcMinimumRepayments(years=30):
    rate = HOUSE_INTEREST_RATE/100/26
    paymentPeriods = years*26
    return (HOUSE_PRICE-INITIAL_CAPITAL) * (rate * (1+rate)**paymentPeriods) / ((1+rate)**paymentPeriods - 1) + 3

def calcMortgage(repaymentAmount):
    mortgageVal = HOUSE_PRICE - INITIAL_CAPITAL
    for ii in range (YEARS_TO_COMPARE*26):
        mortgageVal = (mortgageVal - repaymentAmount) * (1 + HOUSE_INTEREST_RATE/100/26)
        if mortgageVal < 0:
            return mortgageVal
    return mortgageVal

def calcTimeToPayOffMortgage(expenses):
    repaymentAmount = (INCOME-INITIAL_TAX)/26 - expenses
    mortgageVal = HOUSE_PRICE - INITIAL_CAPITAL

    fortnights = 0
    while mortgageVal > 0:
        fortnights += 1
        mortgageVal = (mortgageVal - repaymentAmount) * (1 + HOUSE_INTEREST_RATE/100/26)
        if fortnights == YEARS_TO_COMPARE * 26:
            return None, mortgageVal
        if fortnights % 26 == 0:
            repaymentAmount, expenses = updateAmountLeftOver(fortnights/26, mortgageCosts, expenses)

    return fortnights, mortgageVal

def calcStocksAmount(initialVal, totalCosts, costFn, fortnightsToInvest=None):
    if not fortnightsToInvest:
        fortnightsToInvest = YEARS_TO_COMPARE*26
    leftOver = (INCOME-INITIAL_TAX)/26 - totalCosts

    value = initialVal
    for ii in range(fortnightsToInvest):
        value = value * (1 + (STOCK_RETURN_RATE/100/26)) + leftOver
        if (ii+1) % 26 == 0:
            leftOver, totalCosts = updateAmountLeftOver(int((ii+1) / 26), costFn, totalCosts)
    return value

def updateAmountLeftOver(years, costsFn, currentExpenses):
    income = INCOME
    if INCREASE_INCOME:
        income = INCOME * (1 + INCOME_INCREASE_RATE/100) ** years
    income -= calculateTax(income)
    expenses = costsFn(years, currentExpenses)
    return income /26 - expenses, expenses

#Could add modelling for increasing different expenses
def stocksOnlyExpenses(years, currentExpenses):
    return currentExpenses

def mortgageCosts(years, currentExpenses):
    if RENT_OUT_A_ROOM and years == YEARS_TO_RENT_ROOM:
        return currentExpenses + 2 * ROOM_RENT
    return currentExpenses

def minimumMortgageCosts(years, currentExpenses):
    if RENT_OUT_A_ROOM and years == YEARS_TO_RENT_ROOM:
        currentExpenses = currentExpenses + 2 * ROOM_RENT
    if years == 30:
        currentExpenses -=calcMinimumRepayments()
    return currentExpenses

def calculateTax(income):
    if income > 190000:
        return 51638 + 0.45 * (income-190000)
    if income > 135000:
        return 31288 + 0.37 * (income-135000)
    if income > 45000:
        return 4288 + 0.30 * (income-45000)
    if income > 18200:
        return 0.16 * (income-18200)
    return 0

def formatCurrency(amount):
    if amount != None:
        return '${:,.2f}'.format(amount)


if __name__ == "__main__":
    setConstants()
    main()
