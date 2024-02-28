from graph_of_thoughts.thoughts.operations import OperationType, Aggregate, Generate, Improve, Split

class OperationFactory:
    @staticmethod
    def create_operation(**o_kwargs):
        if o_kwargs["type"] == OperationType.aggregate:
            return Aggregate(
                num_try=o_kwargs["num_try"]
            )
        elif o_kwargs["type"] == OperationType.generate:
            return Generate(
                num_try=o_kwargs["num_try"],
                num_choice=o_kwargs["num_choice"],
                part=0 if "part" not in o_kwargs.keys() else o_kwargs["part"]
            )
        elif o_kwargs["type"] == OperationType.improve:
            return Improve(
                num_try=o_kwargs["num_try"],
                num_choice=o_kwargs["num_choice"],
                part=0 if "part" not in o_kwargs.keys() else o_kwargs["part"]
            )
        elif o_kwargs["type"] == OperationType.split:
            return Split(
                num_split=o_kwargs["num_split"]
            )
        else:
            raise Exception(f"""Type: {o_kwargs["type"]} is not supported""")