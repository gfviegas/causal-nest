import random
import re

import numpy as np
import pandas as pd
import pytest
from networkx import DiGraph

from causal_nest.discovery_models import IAMB
from causal_nest.dataset import Dataset, FeatureType, FeatureTypeMap


# Is method allowed
def test_is_method_allowed_validates_dataset_as_cn_instance():
    with pytest.raises(ValueError, match=r"Field 'dataset' must be a CausalNest `Dataset` instance"):
        c = IAMB()
        c.is_method_allowed([1, 2, 3])


def test_is_method_allowed_returns_true_with_non_numeric_feature_present():
    df = pd.DataFrame(data=np.random.normal(0, 5, size=(100, 3)), columns=["foo", "bar", "test"])
    df["random_column"] = [random.choice(["a", "b", "c", "d"]) for _i in range(0, 100)]

    dataset = Dataset(
        data=df,
        target="test",
        feature_mapping=[
            FeatureTypeMap(feature="foo", type=FeatureType.CONTINUOUS),
            FeatureTypeMap(feature="bar", type=FeatureType.CONTINUOUS),
            FeatureTypeMap(feature="random_column", type=FeatureType.CATEGORICAL),
        ],
    )

    c = IAMB()
    assert c.is_method_allowed(dataset)


def test_is_method_allowed_returns_true_with_non_normal_feature_present():
    df = pd.DataFrame(data=np.random.normal(0, 5, size=(100, 3)), columns=["foo", "bar", "test"])
    df["non_normal"] = [(random.randint(0, 200) if random.random() < 0.1 else 0) for _i in range(0, 100)]

    dataset = Dataset(
        data=df,
        target="test",
        feature_mapping=[
            FeatureTypeMap(feature="foo", type=FeatureType.CONTINUOUS),
            FeatureTypeMap(feature="bar", type=FeatureType.CONTINUOUS),
            FeatureTypeMap(feature="non_normal", type=FeatureType.CONTINUOUS),
        ],
    )

    c = IAMB()
    assert c.is_method_allowed(dataset)


@pytest.mark.skip(reason="TODO: Encontrar uma base pra teste não-linear")
def test_is_method_allowed_returns_true_with_non_linear_relationship_present():
    df = pd.DataFrame(data=np.random.normal(0, 5, size=(100, 3)), columns=["foo", "bar", "test"])
    df["non_linear"] = np.random.uniform(-5000, 5000, size=(100, 1))

    dataset = Dataset(
        data=df,
        target="non_linear",
        feature_mapping=[
            FeatureTypeMap(feature="foo", type=FeatureType.CONTINUOUS),
            FeatureTypeMap(feature="bar", type=FeatureType.CONTINUOUS),
            FeatureTypeMap(feature="test", type=FeatureType.CONTINUOUS),
        ],
    )

    c = IAMB()
    assert c.is_method_allowed(dataset)


def test_is_method_allowed_returns_true_with_valid_input():
    df = pd.DataFrame(data=np.random.normal(0, 5, size=(100, 3)), columns=["foo", "bar", "test"])

    dataset = Dataset(
        data=df,
        target="test",
        feature_mapping=[
            FeatureTypeMap(feature="foo", type=FeatureType.CONTINUOUS),
            FeatureTypeMap(feature="bar", type=FeatureType.CONTINUOUS),
        ],
    )

    c = IAMB()
    assert c.is_method_allowed(dataset)


# Create graph from data
def test_create_graph_from_data_validates_dataset_as_cn_instance():
    with pytest.raises(ValueError, match=r"Field 'dataset' must be a CausalNest `Dataset` instance"):
        c = IAMB()
        c.create_graph_from_data([1, 2, 3])


def test_create_graph_from_data_generates_valid_graph_with_valid_input():
    df = pd.DataFrame(data=np.random.normal(0, 5, size=(100, 3)), columns=["foo", "bar", "test"])

    dataset = Dataset(
        data=df,
        target="test",
        feature_mapping=[
            FeatureTypeMap(feature="foo", type=FeatureType.CONTINUOUS),
            FeatureTypeMap(feature="bar", type=FeatureType.CONTINUOUS),
        ],
    )

    c = IAMB()
    graph = c.create_graph_from_data(dataset)
    assert isinstance(graph, DiGraph)
