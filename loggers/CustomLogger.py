
import csv

action_file = "/Users/rensdur/Documents/TU Delft/BSc Computer Science and Engineering/Year 3/CSE3210 Collaborative Artificial Intelligence/Project 2/GitHub/CAI-Group38-Project2/logs/exp_strong_at_time_23h-34m-19s_date_18d-03m-2023y/world_1/actions__2023-03-18_233419.csv"

action_header = []
action_contents=[]
trustfile_header = []
trustfile_contents = []
# Calculate the unique human and agent actions
unique_agent_actions = []
unique_human_actions = []
with open(action_file) as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar="'")
    for row in reader:
        if action_header==[]:
            action_header=row
            continue
        if row[2:4] not in unique_agent_actions and row[2]!="":
            unique_agent_actions.append(row[2:4])
        if row[4:6] not in unique_human_actions and row[4]!="":
            unique_human_actions.append(row[4:6])
        if row[4] == 'RemoveObjectTogether' or row[4] == 'CarryObjectTogether' or row[4] == 'DropObjectTogether':
            if row[4:6] not in unique_agent_actions:
                unique_agent_actions.append(row[4:6])
        res = {action_header[i]: row[i] for i in range(len(action_header))}
        action_contents.append(res)

no_ticks = action_contents[-1]['tick_nr']
score = action_contents[-1]['score']
completeness = action_contents[-1]['completeness']

print("\n\n=====OUPUT=====")
print("Completeness: " + str(completeness))
print("Score: " + str(score))
print("No_ticks: " + str(no_ticks))
print("Agent_actions: " + str(len(unique_agent_actions)))
print("Human_actions: " + str(len(unique_human_actions)))
print()