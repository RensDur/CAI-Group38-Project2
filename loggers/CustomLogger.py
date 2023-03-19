
import csv

action_file = "C:\Users\julie\OneDrive\Documents\university\CAI38\logs\exp_normal_at_time_12h-00m-26s_date_19d-03m-2023y\world_1\actions__2023-03-19_120027.csv"

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