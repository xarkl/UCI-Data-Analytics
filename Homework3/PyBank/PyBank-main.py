#Import dependencies
import pandas as pd 

#Load File
file = "budget_data.csv"

#Read and display
bs_original = pd.read_csv(file)
bs_original.head()

#Total number of months included in dataset
month_total = bs_original['Date'].count()
month_total

#The total net amount of "Profit/Losses" over the entire period
total_profit = bs_original["Revenue"].sum()
total_profit

#The total net amount of "Profit/Losses" between months over the entire period
#First calculate the P/L between each month
net_revenue = bs_original.set_index('Date').diff()
net_revenue.head()

#Calculate the average for the entire period
average_change = net_revenue.mean()
average_change

#The greates increase in profits over the entire period
great_increase = net_revenue.max()
great_increase

#The greatest decrease in losses over the entire period
great_decrease = net_revenue.min()
great_decrease

#Sort to get date
values = net_revenue.sort_values(["Revenue"], ascending=False)
values

#Print to terminal
print("Financial Analysis")
print("-------------------------------")
print("Total Months:" + str(month_total))
print("Total $" + str(total_profit))
print("Average Change: $" + str(average_change))
print("Greatest Increase in Profits: Feb-16 " + str(great_increase))
print("Greatest Decrease in Profits: Aug-14 " + str(great_decrease))
