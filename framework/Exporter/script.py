import pandas as pd
from pulp import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--cluster', type=str, help='Please enter the name of the cluster to evaluate')
parser.add_argument('--budget', type=float, help='The remaining budget for the defender')
args = parser.parse_args()

# Read the CSV file
if args.cluster:
    cluster_name = args.cluster
else:
    cluster_name = input("Please enter the name of the cluster to evaluate: ")

estimator_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Estimator','results'))
df = pd.read_csv(os.path.join(estimator_path, cluster_name + '.csv'))

# Read the cost limit
if args.budget:
    C = args.budget
else:
    C = int(input("Please enter the cost limit: "))

# # Read the CSV file
# df = pd.read_csv('data.csv')

# # Read the cost limit
# C = int(input("Please enter the cost limit: "))

# Define the problem
prob = LpProblem("0-1 Integer Programming Problem", LpMaximize)

# Define the variables
items = list(df.index)
x = LpVariable.dicts('x', items, lowBound=0, upBound=1, cat='Integer')

# Define the objective function
prob += lpSum([df.loc[i, 'Risk'] * x[i] for i in items]), "Total Risk"

# Define the constraints
prob += lpSum([df.loc[i, 'Cost_Defender'] * x[i] for i in items]) <= C, "Total Cost"

# Solve the problem
prob.solve()


# Print the results
# print("Status:", LpStatus[prob.status])
print("Total Risk =", value(prob.objective))

# Save the purchased items
result = df.copy()
result['Buy'] = [int(x[i].value()) for i in items]
result = result[result['Buy'] == 1]
result = result[['Container', 'CVE', 'Cost_Defender', 'Risk']]
result.to_csv('result.csv', index=False)


# Calculate the number of purchased items
num_items = sum([int(x[i].value()) for i in items])

# Print the number of purchased items
print("Number of purchased items =", num_items)

# Calculate the remaining cost
remaining_cost = C - sum([df.loc[i, 'Cost_Defender'] * x[i].value() for i in items if x[i].value() == 1])

# Print the remaining cost
print("Remaining Cost =", remaining_cost)