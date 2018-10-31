#Import dependencies
import csv
import os

#Load File and output file
file_load = os.path.join("Resources", "budget_data.csv")
file_output = os.path.join("budget_analysis.txt")

#Open/Read CSV file
with open(file_load) as financial_data:
    reader = csv.reader(financial_data)

    next(reader)

    #Set initial values
    month_count = 0
    total_revenue = 0
    this_month_revenue = 0
    last_month_revenue = 0
    revenue_change = 0
    revenue_changes = []
    months = []

    #Gather monthly changes in revenue
    for row in reader:
        month_count = month_count + 1
        months.append(row[0])
        this_month_revenue = int(row[1])
        total_revenue = total_revenue + this_month_revenue
        if month_count > 1:
            revenue_change = this_month_revenue - last_month_revenue
            revenue_changes.append(revenue_change)
        last_month_revenue = this_month_revenue

# Analyze month by month results 
sum_rev_changes = sum(revenue_changes)
average_change = sum_rev_changes / (month_count - 1)
max_change = max(revenue_changes)
min_change = min(revenue_changes)
max_month_index = revenue_changes.index(max_change)
min_month_index = revenue_changes.index(min_change)
max_month = months[max_month_index]
min_month = months[min_month_index]

output = f"""
Financial Analysis
-----------------------------------
Total Months: {month_count}
Total Revenue: ${total_revenue}
Average Revenue Change: ${average_change}
Greatest Increase in Profit: {max_month} ${max_change}
Greatest Decrease in Profit: {min_month} ${min_change}
"""

print(output)

#output to txt
with open(file_output, "w") as txt_file:
    txt_file.write(output)