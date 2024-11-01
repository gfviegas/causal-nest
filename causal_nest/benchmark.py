from dataclasses import dataclass

from networkx import DiGraph

from causal_nest.stats import BenchmarkStats


@dataclass
class ModelBenchmark:
    """
    Class to store and display the results of a model benchmarking process.

    This class is designed to encapsulate the results of a model benchmarking process, providing
    a structured way to store and access various attributes related to the benchmarking. It is
    intended to be used in workflows where the performance of different models needs to be
    compared, stored, or analyzed further.

    Attributes:
        stats (BenchmarkStats): The statistics of the benchmark.
        model_name (str): The name of the model being benchmarked.
        out_graph (DiGraph): The output graph generated by the model.
    """

    stats: BenchmarkStats = BenchmarkStats()
    model_name: str
    out_graph: DiGraph
