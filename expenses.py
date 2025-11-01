#This is simply for modeeling my expenses and income to see how much I can afford to make in repayments/investments

# ORIGINAL EXPENSES (for our current household of 4)
WATER = 340     #Every 2 months
ELEC = 450      #Every 2 months
GAS = 220       #Every 3 months
RATES = 3200    #Yearly 
FOOD = 400      #Weekly

OTHER_EXPENSES = 375 + 490  #Fortnightly (expenses + donations)

#TBC
FORTNIGHTLY_INCOME = 3318


def CalcForntighlyExpensesEstimate():
    water = WATER * 4/5 * 6/26
    elec = ELEC/3 * 6/26
    gas = GAS/3 * 4/26
    food = FOOD/3 * 2
    rates = RATES * 2/3 /26
    other = OTHER_EXPENSES
    expenses = water + elec + gas + food + rates + other
    print(f"Fortnightly expenses\nWater: {water:.2f}\nPower: {elec:.2f}\nGas: {gas:.2f}\nFood: {food:.2f}\nRates: {rates:.2f}\nOther: {other:.2f}\nHouse related total: {expenses-other:.2f}\nTotal: {expenses:.2f}")

    return expenses

if __name__ == "__main__":
    expenses = CalcForntighlyExpensesEstimate()
    print(f"Available funds fortnighly: {FORTNIGHTLY_INCOME-expenses:.2f}")