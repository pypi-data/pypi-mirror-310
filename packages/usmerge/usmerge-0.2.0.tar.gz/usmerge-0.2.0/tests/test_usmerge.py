import numpy as np
import pytest
from usmerge import (
    equal_wid_merge,
    equal_fre_merge,
    kmeans_merge,
    som_k_merge,
    fcm_merge,
    kernel_density_merge,
    information_merge,
    gaussian_mixture_merge,
    hierarchical_density_merge
)
import pandas as pd

@pytest.fixture
def sample_data():
    np.random.seed(42)
    return np.concatenate([
        np.random.normal(0, 0.3, 50),
        np.random.normal(5, 0.4, 50),
        np.random.normal(10, 0.3, 50)
    ])

def test_equal_width_binning(sample_data):
    labels, edges = equal_wid_merge(sample_data, n=3)
    assert len(labels) == len(sample_data)
    assert len(edges) == 4
    assert all(isinstance(x, int) for x in labels)
    assert all(0 <= x < 3 for x in labels)

def test_fcm_merge(sample_data):
    labels, edges = fcm_merge(sample_data, n=3)
    assert len(labels) == len(sample_data)
    assert len(edges) == 4
    assert all(isinstance(x, int) for x in labels)
    assert all(0 <= x < 3 for x in labels)

def test_kmeans_merge(sample_data):
    labels, edges = kmeans_merge(sample_data, n=3)
    assert len(labels) == len(sample_data)
    assert len(edges) == 4
    assert all(isinstance(x, int) for x in labels)
    assert all(0 <= x < 3 for x in labels)

def test_information_merge(sample_data):
    labels, edges = information_merge(sample_data, n=3)
    assert len(labels) == len(sample_data)
    assert len(edges) == 4
    assert all(isinstance(x, int) for x in labels)
    assert all(0 <= x < 3 for x in labels)

def test_input_formats():
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    
    # Test different input formats
    pd_series = pd.Series(data)
    pd_df = pd.DataFrame(data)
    np_array = np.array(data)
    
    labels1, _ = equal_wid_merge(pd_series, n=2)
    labels2, _ = equal_wid_merge(pd_df, n=2)
    labels3, _ = equal_wid_merge(np_array, n=2)
    
    assert len(labels1) == len(data)
    assert len(labels2) == len(data)
    assert len(labels3) == len(data)
