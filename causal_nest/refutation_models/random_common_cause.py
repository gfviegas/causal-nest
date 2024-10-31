from dowhy import CausalModel

from causal_nest.problem import Dataset
from causal_nest.refutation_models.refutation_method_model import RefutationMethodModel
from causal_nest.results import EstimationResult, RefutationResult


class RandomCommonCause(RefutationMethodModel):
    def refute_estimate(self, dataset: Dataset, estimation_result: EstimationResult, **kwargs):
        model = CausalModel(data=dataset.data, outcome=dataset.target, treatment=estimation_result.treatment)

        r = model.refute_estimate(
            estimation_result.estimand, estimation_result.estimate, method_name="random_common_cause"
        )

        return RefutationResult(
            treatment=estimation_result.treatment,
            model="RandomCommonCause",
            p_value=r.refutation_result["p_value"],
            estimated_effect=r.estimated_effect,
            new_effect=r.new_effect,
        )