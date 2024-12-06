**Example**
```python
from precision_tree.nodes import DecisionNode, ChanceNode, PayoffNode
from precision_tree.tree import TreeWrapper


root = DecisionNode("Start Decision")

# Big Factory
big_factory = ChanceNode("Big Factory", cost=700, years=5)
high_demand = PayoffNode("High Demand", 280)
low_demand = PayoffNode("Low Demand", -80)
big_factory.add_branch("High Demand", high_demand, 0.8)
big_factory.add_branch("Low Demand", low_demand, 0.2)

# Small Factory
small_factory = ChanceNode("Small Factory", cost=300, years=5)
high_demand_small = PayoffNode("High Demand Small", 180)
low_demand_small = PayoffNode("Low Demand Small", -55)
small_factory.add_branch("High Demand", high_demand_small, 0.8)
small_factory.add_branch("Low Demand", low_demand_small, 0.2)

# Stop by Year
stop_by_year = DecisionNode("Stop by Year")
negative_info = PayoffNode("Negative Info", 0)

positive_info = DecisionNode("Positive Info")
big_factory_1 = ChanceNode("Big Factory 1", cost=700, years=4)
high_demand_1 = PayoffNode("High Demand 1", 280)
low_demand_1 = PayoffNode("Low Demand 1", -80)
big_factory_1.add_branch("High Demand 1", high_demand_1, 0.9)
big_factory_1.add_branch("Low Demand 1", low_demand_1, 0.1)

small_factory_1 = ChanceNode("Small Factory 1", cost=300, years=4)
high_demand_small_1 = PayoffNode("High Demand Small 1", 1800)
low_demand_small_1 = PayoffNode("Low Demand Small 1", -55)
small_factory_1.add_branch("High Demand 1", high_demand_small_1, 0.9)
small_factory_1.add_branch("Low Demand 1", low_demand_small_1, 0.1)

positive_info.add_branch("Big Factory", big_factory_1)
positive_info.add_branch("Small Factory", small_factory_1)

stop_by_year.add_branch("Positive Info", positive_info, 0.7)
stop_by_year.add_branch("Negative Info", negative_info, 0.3)

root.add_branch("Big Factory", big_factory)
root.add_branch("Small Factory", small_factory)
root.add_branch("Stop by Year", stop_by_year)

best_value = root.calculate_value()
print(f"Expected Value of the best strategy: {best_value:.2f}")
print(f"Optimal branch: {root.best_branch}")

tree = TreeWrapper(root)
tree.show("Factory Decision Tree")
```
