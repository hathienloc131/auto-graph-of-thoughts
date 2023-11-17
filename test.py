from graph_of_thoughts.thoughts import OperationType, GraphOfOperations, Generate, Split, Aggregate

graph = GraphOfOperations()

graph.append_operation(Split(2))
for i in range(len(graph.leaves)):
    if graph.leaves[i].operation_type == OperationType.split:
        split_node: Split = graph.leaves[i]
        for _ in range(split_node.num_split):
            generate_thought = Generate(5, 1)
            generate_thought.add_predecessor(split_node)

            graph.add_operation(generate_thought)
graph.append_operation(Aggregate(2))

graph.leaves[0].execute()