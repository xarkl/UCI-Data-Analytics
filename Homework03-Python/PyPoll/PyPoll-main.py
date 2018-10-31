#Import 
import os
import csv

#Load and Output CSV file
file_load = os.path.join('Resources','election_data.csv')
file_output = os.path.join('election_analysis.txt')

#Open/Read CSV file
with open(file_load) as election_data:
    reader = csv.reader(election_data)

    next(reader)

    #Set initial values
    total_votes = 0
    candidate = ""
    candidate_votes = {}
    candidate_percentages = {}
    winner_votes = 0
    winner = ""

    #Count votes
    for row in reader:
        total_votes = total_votes + 1
        candidate = row[2]
        if candidate in candidate_votes:
            candidate_votes[candidate] = candidate_votes[candidate] + 1
        else:
            candidate_votes[candidate] = 1

#Calculate vote percentages
for person, vote_count in candidate_votes.items():
    candidate_percentages[person] = '{0:.0%}'.format(vote_count / total_votes)
    if vote_count > winner_votes:
        winner_votes = vote_count
        winner = person

#Results
output1 = f"""
Election Results
-------------------------
Total Votes: {total_votes}
-------------------------
"""

output2 = []
for person,vote_count in candidate_votes.items():
    output2.append(f"{person}: {candidate_percentages[person]} ({vote_count})")

output2_breakdown = f"""
{output2[0]}
{output2[1]}
{output2[2]}
{output2[3]}
"""  
    
output3 = f"""
------------------------
Winner: {winner}
------------------------
"""

output_final = f"""
{output1}
{output2_breakdown}
{output3}
"""

print(output_final)

#output
with open(file_output, "w") as txt_file:
    txt_file.write(output_final)



