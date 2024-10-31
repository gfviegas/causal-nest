import time
from concurrent.futures import FIRST_COMPLETED, TimeoutError, wait
from dataclasses import replace
from multiprocessing import cpu_count
from timeit import default_timer as timer
from typing import Dict, List

from pebble import ProcessPool

from causal_nest.problem import Problem
from causal_nest.refutation_models import PlaceboPermute, RandomCommonCause, RefutationMethodModel, SubsetRemoval
from causal_nest.results import EstimationResult

known_methods = [PlaceboPermute, RandomCommonCause, SubsetRemoval]


def refute_with_model(problem: Problem, estimation_result: EstimationResult, model: RefutationMethodModel):
    start = timer()
    m = model()
    result = m.refute_estimate(problem.dataset, estimation_result)
    end = timer()

    result.runtime = end - start

    return result


def refute_estimation(problem: Problem, er: EstimationResult, timeout: int = 180):
    response = {"model": er.model, "results": []}
    start_time = time.time()

    for m in known_methods:
        if time.time() - start_time > timeout:
            # If timeout thershold is reached, then return the results up to that point
            return response

        r = refute_with_model(problem, er, m)
        response["results"].append(r)

    return response


def refute_all_results(
    problem: Problem,
    max_seconds_global: int = 180,
    max_seconds_model: int = 25,
    verbose: bool = False,
    max_workers=None,
):
    sorted_results = list(
        sorted(
            filter(lambda x: x, [item for sublist in problem.estimation_results.values() for item in sublist]),
            key=lambda x: x.estimate.value,
            reverse=True,
        )
    )
    refutation_results = {key: [] for key in problem.estimation_results.keys()}

    if max_workers is None:
        max_workers = cpu_count()

    start_time = time.time()
    elapsed_time = 0

    with ProcessPool(max_workers=max_workers) as pool:
        futures = []

        for er in sorted_results:
            futures.append(pool.schedule(refute_estimation, args=(problem, er, max_seconds_model)))

        for future in futures:
            remaining_time = max_seconds_global - elapsed_time
            if remaining_time <= 0:
                break

            # Wait for the future to complete with the remaining global timeout
            done, _ = wait([future], timeout=remaining_time, return_when=FIRST_COMPLETED)

            for future in done:
                try:
                    future_result = future.result()
                    if future_result is not None:
                        refutation_results[future_result["model"]] = (
                            refutation_results[future_result["model"]] + future_result["results"]
                        )
                except TimeoutError:
                    pass
                except Exception as e:
                    print(f'e: {e}')
                    pass

            elapsed_time = time.time() - start_time

    return replace(problem, refutation_results=refutation_results)