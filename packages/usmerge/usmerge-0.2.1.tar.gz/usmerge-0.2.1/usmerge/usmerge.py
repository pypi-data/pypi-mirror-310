import math
import random
from typing import Union, List, Tuple, Sequence
import numpy as np
import pandas as pd

def _convert_to_list(data: Union[List, Tuple, np.ndarray, pd.Series, pd.DataFrame, Sequence]) -> List[float]:
    """Convert different input formats to list of floats
    
    Args:
        data: Input data in various formats including pandas Series/DataFrame
        
    Returns:
        List of float values
    """
    if isinstance(data, pd.Series):
        return data.values.tolist()
    elif isinstance(data, pd.DataFrame):
        if data.shape[1] != 1:
            raise ValueError("DataFrame must have exactly one column")
        return data.iloc[:, 0].values.tolist()
    elif isinstance(data, np.ndarray):
        return data.flatten().tolist()
    elif isinstance(data, (list, tuple)):
        return [float(x) for x in data]
    elif hasattr(data, '__iter__'):
        return [float(x) for x in data]
    else:
        raise TypeError("Input data must be array-like, pandas Series, or single-column DataFrame")

def equal_wid_merge(data: Union[List, Tuple, np.ndarray, Sequence], n: int) -> Tuple[List[int], List[float]]:
    """Equal width binning merge
    
    Args:
        data: Input data in various formats
        n: Number of bins
        
    Returns:
        Tuple containing:
            labels: Bin labels for each data point
            edges: Bin edges including leftmost and rightmost edges
    """
    data = _convert_to_list(data)
    
    min_val = min(data)
    max_val = max(data)
    width = (max_val - min_val) / n
    
    edges = [min_val + i * width for i in range(n+1)]
    labels = []
    
    for x in data:
        for i in range(n):
            if edges[i] <= x <= edges[i+1]:
                labels.append(i)
                break
    
    return labels, edges

def equal_fre_merge(data: Union[List, Tuple, np.ndarray, Sequence], n: int) -> Tuple[List[int], List[float]]:
    """Equal frequency binning merge
    
    Args:
        data: Input data in various formats
        n: Number of bins
        
    Returns:
        Tuple containing:
            labels: Bin labels for each data point
            edges: Bin edges including leftmost and rightmost edges
    """
    data = _convert_to_list(data)
    
    sorted_data = sorted(data)
    bin_size = len(data) // n
    edges = [sorted_data[0]]
    
    for i in range(1, n):
        edges.append(sorted_data[i * bin_size])
    edges.append(sorted_data[-1])
    
    labels = []
    for x in data:
        for i in range(n):
            if edges[i] <= x <= edges[i+1]:
                labels.append(i)
                break
                
    return labels, edges

def kmeans_merge(data: Union[List, Tuple, np.ndarray, Sequence], 
                n: int, 
                max_iter: int = 100) -> Tuple[List[int], List[float]]:
    """K-means clustering merge
    
    Args:
        data: Input data in various formats
        n: Number of clusters
        max_iter: Maximum iterations
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            edges: Cluster boundaries
    """
    data = _convert_to_list(data)
    
    # Initialize centroids
    min_val = min(data)
    max_val = max(data)
    centroids = [min_val + i*(max_val-min_val)/(n-1) for i in range(n)]
    
    prev_centroids = None
    iteration = 0
    
    while iteration < max_iter:
        # Assign points to nearest centroid
        clusters = [[] for _ in range(n)]
        labels = []
        
        for x in data:
            distances = [abs(x - c) for c in centroids]
            nearest = distances.index(min(distances))
            clusters[nearest].append(x)
            labels.append(nearest)
            
        # Update centroids
        prev_centroids = centroids.copy()
        for i in range(n):
            if clusters[i]:
                centroids[i] = sum(clusters[i]) / len(clusters[i])
                
        # Check convergence
        if prev_centroids == centroids:
            break
            
        iteration += 1
    
    # Calculate edges between clusters
    sorted_centroids = sorted(centroids)
    edges = [min_val]
    for i in range(len(sorted_centroids)-1):
        edges.append((sorted_centroids[i] + sorted_centroids[i+1])/2)
    edges.append(max_val)
    
    return labels, edges

def som_k_merge(data: Union[List, Tuple, np.ndarray, Sequence],
               n: int,
               learning_rate: float = 0.5,
               sigma: float = 0.5,
               epochs: int = 500) -> Tuple[List[int], List[float]]:
    """SOM followed by K-means clustering
    
    Args:
        data: Input data in various formats
        n: Number of clusters
        learning_rate: Initial learning rate
        sigma: Neighborhood radius
        epochs: Number of training epochs
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            edges: Cluster boundaries
    """
    data = _convert_to_list(data)
    
    # Simple 1D SOM implementation
    min_val = min(data)
    max_val = max(data)
    weights = [min_val + i*(max_val-min_val)/(n-1) for i in range(n)]
    
    for epoch in range(epochs):
        lr = learning_rate * (1 - epoch/epochs)
        sig = sigma * (1 - epoch/epochs)
        
        # Shuffle data each epoch
        data_epoch = data.copy()
        random.shuffle(data_epoch)
        
        for x in data_epoch:
            # Find BMU
            distances = [abs(x - w) for w in weights]
            bmu_idx = distances.index(min(distances))
            
            # Update weights
            for i in range(n):
                dist = abs(i - bmu_idx)
                influence = math.exp(-dist**2 / (2*sig**2))
                weights[i] += lr * influence * (x - weights[i])
    
    # Use trained weights as initial centroids for k-means
    centroids = weights
    prev_centroids = None
    
    while True:
        # Assign points to nearest centroid
        clusters = [[] for _ in range(n)]
        labels = []
        
        for x in data:
            distances = [abs(x - c) for c in centroids]
            nearest = distances.index(min(distances))
            clusters[nearest].append(x)
            labels.append(nearest)
            
        # Update centroids
        prev_centroids = centroids.copy()
        for i in range(n):
            if clusters[i]:
                centroids[i] = sum(clusters[i]) / len(clusters[i])
                
        # Check convergence
        if prev_centroids == centroids:
            break
    
    # Calculate edges between clusters
    sorted_centroids = sorted(centroids) 
    edges = [min_val]
    for i in range(len(sorted_centroids)-1):
        edges.append((sorted_centroids[i] + sorted_centroids[i+1])/2)
    edges.append(max_val)
    
    return labels, edges

def calculate_variance(data):
    """Helper function to calculate variance for Jenks breaks"""
    if not data:
        return 0
    mean = sum(data) / len(data)
    return sum((x - mean) ** 2 for x in data) / len(data)

def jenks_breaks_merge(data: Union[List, Tuple, np.ndarray, Sequence], n: int) -> Tuple[List[int], List[float]]:
    """Jenks Natural Breaks optimization clustering
    
    Args:
        data: Input data in various formats
        n: Number of clusters
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            edges: Cluster boundaries
    """
    data = _convert_to_list(data)
    sorted_data = sorted(data)
    
    # Initialize matrices for dynamic programming
    n_data = len(sorted_data)
    variance_combinations = np.zeros((n_data, n))
    lower_class_limits = np.zeros((n_data, n))
    
    # Initialize first variance combination
    variance_combinations[0][0] = calculate_variance(sorted_data[:1])
    for i in range(1, n_data):
        variance_combinations[i][0] = calculate_variance(sorted_data[:(i+1)])
        lower_class_limits[i][0] = 0
    
    # Complete the dynamic programming matrix
    for j in range(1, n):
        for i in range(j, n_data):
            min_val = float('inf')
            min_idx = 0
            
            for k in range(j-1, i):
                val = variance_combinations[k][j-1] + \
                      calculate_variance(sorted_data[(k+1):(i+1)])
                if val < min_val:
                    min_val = val
                    min_idx = k
                    
            variance_combinations[i][j] = min_val
            lower_class_limits[i][j] = min_idx
    
    # Get the break points
    edges = [min(data)]
    k = n_data - 1
    for j in range(n-1, 0, -1):
        idx = int(lower_class_limits[k][j])
        edges.insert(1, sorted_data[idx + 1])
        k = idx
    edges.append(max(data))
    
    # Assign labels
    labels = []
    for x in data:
        for i in range(n):
            if edges[i] <= x <= edges[i+1]:
                labels.append(i)
                break
    
    return labels, edges

def quantile_merge(data: Union[List, Tuple, np.ndarray, Sequence], n: int) -> Tuple[List[int], List[float]]:
    """Quantile-based clustering
    
    Args:
        data: Input data in various formats
        n: Number of clusters
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            edges: Cluster boundaries
    """
    data = _convert_to_list(data)
    sorted_data = sorted(data)
    
    # Calculate quantile positions
    positions = [int(len(data) * i / n) for i in range(n+1)]
    positions[-1] = len(data) - 1
    
    # Get edges from quantiles
    edges = [sorted_data[pos] for pos in positions]
    
    # Assign labels
    labels = []
    for x in data:
        for i in range(n):
            if edges[i] <= x <= edges[i+1]:
                labels.append(i)
                break
                
    return labels, edges

def dbscan_1d_merge(data: Union[List, Tuple, np.ndarray, Sequence], 
                    n: int,
                    eps: float = None,
                    min_samples: int = 5,
                    max_iter: int = 50) -> Tuple[List[int], List[float]]:
    """DBSCAN clustering adapted for 1D data with target number of clusters
    
    Args:
        data: Input data in various formats
        n: Target number of clusters
        eps: The maximum distance between points (if None, will be automatically adjusted)
        min_samples: The number of samples in a neighborhood for a point to be considered core
        max_iter: Maximum iterations for eps adjustment
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point (-1 represents noise)
            edges: Cluster boundaries
    """
    data = _convert_to_list(data)
    
    if eps is None:
        # Initialize eps based on data range and target clusters
        data_range = max(data) - min(data)
        eps = data_range / (2 * n)
    
    def run_dbscan(eps_val):
        neighbors = []
        for i in range(len(data)):
            point_neighbors = []
            for j in range(len(data)):
                if abs(data[i] - data[j]) <= eps_val:
                    point_neighbors.append(j)
            neighbors.append(point_neighbors)
        
        labels = [-1] * len(data)
        cluster_id = 0
        
        # Find core points and expand clusters
        for i in range(len(data)):
            if labels[i] != -1:
                continue
                
            if len(neighbors[i]) >= min_samples:
                labels[i] = cluster_id
                stack = neighbors[i].copy()
                
                while stack:
                    point = stack.pop()
                    if labels[point] == -1:
                        labels[point] = cluster_id
                        if len(neighbors[point]) >= min_samples:
                            for neighbor in neighbors[point]:
                                if labels[neighbor] == -1:
                                    stack.append(neighbor)
                
                cluster_id += 1
        
        return labels, cluster_id
    
    # Binary search to find appropriate eps
    current_eps = eps
    iteration = 0
    while iteration < max_iter:
        labels, num_clusters = run_dbscan(current_eps)
        
        if num_clusters == n:
            break
        elif num_clusters < n:
            current_eps *= 0.8  # Decrease eps to get more clusters
        else:
            current_eps *= 1.2  # Increase eps to get fewer clusters
            
        iteration += 1
    
    # Calculate cluster boundaries
    if max(labels) < 0:  # No clusters found
        return labels, [min(data), max(data)]
    
    cluster_points = [[] for _ in range(max(labels) + 1)]
    for i, label in enumerate(labels):
        if label != -1:
            cluster_points[label].append(data[i])
    
    # Calculate edges between clusters
    edges = [min(data)]
    cluster_bounds = [(min(points), max(points)) for points in cluster_points if points]
    cluster_bounds.sort()
    
    for i in range(len(cluster_bounds)-1):
        edges.append((cluster_bounds[i][1] + cluster_bounds[i+1][0])/2)
    edges.append(max(data))
    
    return labels, edges

def fcm_merge(data: Union[List, Tuple, np.ndarray, Sequence], 
              n: int, 
              m: float = 2.0,
              max_iter: int = 100,
              epsilon: float = 1e-6) -> Tuple[List[int], List[float]]:
    """Fuzzy C-Means clustering for 1D data
    
    Args:
        data: Input data in various formats
        n: Number of clusters
        m: Fuzziness coefficient (m > 1)
        max_iter: Maximum number of iterations
        epsilon: Convergence threshold
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            edges: Cluster boundaries
    """
    data = _convert_to_list(data)
    
    # Initialize centroids
    min_val = min(data)
    max_val = max(data)
    centroids = [min_val + i*(max_val-min_val)/(n-1) for i in range(n)]
    
    # Initialize membership matrix
    membership = [[0.0 for _ in range(n)] for _ in range(len(data))]
    
    for iteration in range(max_iter):
        old_centroids = centroids.copy()
        
        # Update membership matrix
        for i in range(len(data)):
            distances = [abs(data[i] - c) for c in centroids]
            
            # Handle the case when point equals centroid
            if min(distances) == 0:
                for j in range(n):
                    membership[i][j] = 1.0 if distances[j] == 0 else 0.0
                continue
                
            # Calculate memberships
            for j in range(n):
                denominator = sum((distances[j]/distances[k])**(2/(m-1)) 
                               for k in range(n))
                membership[i][j] = 1.0 / denominator
        
        # Update centroids
        for j in range(n):
            numerator = sum(membership[i][j]**m * data[i] 
                          for i in range(len(data)))
            denominator = sum(membership[i][j]**m 
                            for i in range(len(data)))
            centroids[j] = numerator / denominator
        
        # Check convergence
        if all(abs(old - new) < epsilon for old, new in zip(old_centroids, centroids)):
            break
    
    # Calculate boundaries
    edges = [min(data)]
    for i in range(n-1):
        edges.append((centroids[i] + centroids[i+1])/2)
    edges.append(max(data))
    
    # Assign labels
    labels = []
    for x in data:
        for i in range(n):
            if edges[i] <= x <= edges[i+1]:
                labels.append(i)
                break
    
    return labels, edges

def quantum_clustering(data: Union[List[List], np.ndarray], 
                      n_clusters: int,
                      sigma: float = 1.0,
                      h_bar: float = 1.0,
                      max_iter: int = 100) -> Tuple[List[int], List[List[float]]]:
    """Quantum Clustering based on Schrödinger equation
    
    Args:
        data: Input data matrix (n_samples, n_features)
        n_clusters: Number of clusters
        sigma: Width parameter of Gaussian wave function
        h_bar: Planck's constant analog
        max_iter: Maximum iterations
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            centroids: Final cluster centroids
    """
    data = np.array(data)
    n_samples, n_features = data.shape
    
    # Initialize wave function centers
    centers = data[np.random.choice(n_samples, n_clusters, replace=False)]
    
    for _ in range(max_iter):
        # Calculate potential field
        V = np.zeros(n_samples)
        for i in range(n_samples):
            psi = 0
            for center in centers:
                dist = np.sum((data[i] - center)**2)
                psi += np.exp(-dist/(4*sigma**2))
            V[i] = -h_bar**2/(2*sigma**2) * (psi/sigma**2 - n_features/(2*sigma**2))
        
        # Update centers using gradient descent
        new_centers = []
        for j in range(n_clusters):
            grad = np.zeros(n_features)
            for i in range(n_samples):
                dist = np.sum((data[i] - centers[j])**2)
                weight = np.exp(-dist/(4*sigma**2))
                grad += weight * (data[i] - centers[j])
            new_centers.append(centers[j] + grad/n_samples)
        
        if np.allclose(centers, new_centers):
            break
        centers = np.array(new_centers)
    
    # Assign labels based on closest center
    labels = []
    for point in data:
        distances = [np.sum((point - center)**2) for center in centers]
        labels.append(np.argmin(distances))
    
    return labels, centers.tolist()

def topological_clustering(data: Union[List[List], np.ndarray],
                         n_clusters: int,
                         persistence_threshold: float = 0.1) -> Tuple[List[int], List[List[float]]]:
    """Topological Data Analysis based clustering
    
    Args:
        data: Input data matrix (n_samples, n_features)
        n_clusters: Number of clusters
        persistence_threshold: Threshold for persistent homology
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            centroids: Representative points for each cluster
    """
    data = np.array(data)
    n_samples = len(data)
    
    # Compute distance matrix
    dist_matrix = np.zeros((n_samples, n_samples))
    for i in range(n_samples):
        for j in range(i+1, n_samples):
            dist = np.sqrt(np.sum((data[i] - data[j])**2))
            dist_matrix[i,j] = dist_matrix[j,i] = dist
    
    # Build filtration
    filtration = []
    for eps in np.sort(np.unique(dist_matrix)):
        if eps > 0:
            connected = dist_matrix <= eps
            filtration.append(connected)
    
    # Find persistent components
    birth_times = np.zeros(n_samples)
    death_times = np.inf * np.ones(n_samples)
    
    for t, connected in enumerate(filtration):
        components = _find_components(connected)
        
        # Track births and deaths
        for comp in components:
            min_birth = min(birth_times[list(comp)])
            if min_birth == 0:
                for i in comp:
                    birth_times[i] = t
            
        # Handle merging
        if t > 0:
            old_components = _find_components(filtration[t-1])
            for old_comp in old_components:
                if not any(old_comp.issubset(new_comp) for new_comp in components):
                    for i in old_comp:
                        death_times[i] = t
    
    # Select persistent features
    persistence = death_times - birth_times
    significant = persistence > persistence_threshold
    
    # Cluster based on persistent features
    labels = np.zeros(n_samples, dtype=int)
    current_label = 0
    
    for i in range(n_samples):
        if significant[i] and labels[i] == 0:
            cluster = {i}
            for j in range(n_samples):
                if significant[j] and abs(birth_times[i] - birth_times[j]) < persistence_threshold:
                    cluster.add(j)
            for j in cluster:
                labels[j] = current_label
            current_label += 1
    
    # Compute centroids
    centroids = []
    for i in range(max(labels) + 1):
        mask = labels == i
        centroids.append(np.mean(data[mask], axis=0))
    
    return labels.tolist(), centroids

def _find_components(adjacency):
    """Helper function to find connected components"""
    n = len(adjacency)
    visited = set()
    components = []
    
    for i in range(n):
        if i not in visited:
            component = set()
            stack = [i]
            while stack:
                v = stack.pop()
                if v not in component:
                    component.add(v)
                    visited.add(v)
                    stack.extend(j for j in range(n) if adjacency[v,j] and j not in component)
            components.append(component)
    
    return components

def kernel_density_merge(data: Union[List, Tuple, np.ndarray, Sequence], 
                        n: int,
                        bandwidth: float = None) -> Tuple[List[int], List[float]]:
    """Kernel Density Estimation based clustering
    
    Args:
        data: Input data in various formats
        n: Number of clusters
        bandwidth: Kernel bandwidth (if None, Scott's rule is used)
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            edges: Cluster boundaries
    """
    data = _convert_to_list(data)
    
    if bandwidth is None:
        # Scott's rule for bandwidth selection
        bandwidth = len(data)**(-1/5) * np.std(data)
    
    # Compute density estimate
    x_grid = np.linspace(min(data), max(data), 1000)
    density = np.zeros_like(x_grid)
    
    for x in data:
        kernel = np.exp(-0.5 * ((x_grid - x) / bandwidth)**2)
        density += kernel / (bandwidth * np.sqrt(2 * np.pi))
    density /= len(data)
    
    # Find density peaks and valleys
    peaks = []
    valleys = []
    for i in range(1, len(density)-1):
        if density[i] > density[i-1] and density[i] > density[i+1]:
            peaks.append(x_grid[i])
        elif density[i] < density[i-1] and density[i] < density[i+1]:
            valleys.append(x_grid[i])
    
    # Select n-1 deepest valleys as cluster boundaries
    if len(valleys) >= n-1:
        valley_depths = [min(density[np.abs(x_grid - v).argmin()] 
                           for v in [valleys[i], valleys[i+1]]) 
                        for i in range(len(valleys)-1)]
        edges = [min(data)] + sorted(valleys)[:n-1] + [max(data)]
    else:
        # Fall back to equal width if not enough valleys
        width = (max(data) - min(data)) / n
        edges = [min(data) + i * width for i in range(n+1)]
    
    # Assign points to clusters
    labels = []
    for x in data:
        for i in range(n):
            if edges[i] <= x <= edges[i+1]:
                labels.append(i)
                break
    
    return labels, edges

def information_merge(data: Union[List, Tuple, np.ndarray, Sequence], 
                     n: int,
                     alpha: float = 0.5) -> Tuple[List[int], List[float]]:
    """Information theoretic clustering using MDL principle
    
    Args:
        data: Input data in various formats
        n: Number of clusters
        alpha: Trade-off parameter between compression and accuracy
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            edges: Cluster boundaries
    """
    data = _convert_to_list(data)
    sorted_data = sorted(data)
    
    def calculate_description_length(cluster):
        if not cluster:
            return 0
        std = np.std(cluster) if len(cluster) > 1 else 0
        # MDL = model complexity + encoding length
        return (np.log2(len(cluster)) + 
                len(cluster) * np.log2(std + 1e-10) if std > 0 else 0)
    
    # Dynamic programming to find optimal boundaries
    n_points = len(data)
    dp = [[float('inf')] * (n+1) for _ in range(n_points+1)]
    split_points = [[0] * (n+1) for _ in range(n_points+1)]
    
    dp[0][0] = 0
    
    for i in range(1, n_points+1):
        for k in range(1, min(i+1, n+1)):
            for j in range(k-1, i):
                cluster = sorted_data[j:i]
                cost = calculate_description_length(cluster)
                total_cost = dp[j][k-1] + alpha * cost
                
                if total_cost < dp[i][k]:
                    dp[i][k] = total_cost
                    split_points[i][k] = j
    
    # Reconstruct boundaries
    edges = [min(data)]
    pos = n_points
    for k in range(n, 0, -1):
        pos = split_points[pos][k]
        if k > 1:
            edges.append(sorted_data[pos])
    edges.append(max(data))
    edges.sort()
    
    # Assign labels
    labels = []
    for x in data:
        for i in range(n):
            if edges[i] <= x <= edges[i+1]:
                labels.append(i)
                break
    
    return labels, edges

def gaussian_mixture_merge(data: Union[List, Tuple, np.ndarray, Sequence],
                         n: int,
                         max_iter: int = 100,
                         tol: float = 1e-4) -> Tuple[List[int], List[float]]:
    """Gaussian Mixture Model based clustering for 1D data
    
    Args:
        data: Input data in various formats
        n: Number of components
        max_iter: Maximum iterations
        tol: Convergence tolerance
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            edges: Cluster boundaries
    """
    data = _convert_to_list(data)
    
    # Initialize parameters
    means = np.linspace(min(data), max(data), n)
    variances = [np.var(data)/n] * n
    weights = [1/n] * n
    
    for _ in range(max_iter):
        # E-step: Calculate responsibilities
        resp = np.zeros((len(data), n))
        for i, x in enumerate(data):
            for k in range(n):
                resp[i,k] = weights[k] * np.exp(-(x-means[k])**2/(2*variances[k])) / np.sqrt(2*np.pi*variances[k])
        resp /= resp.sum(axis=1, keepdims=True)
        
        # M-step: Update parameters
        old_means = means.copy()
        for k in range(n):
            weights[k] = resp[:,k].mean()
            means[k] = np.average(data, weights=resp[:,k])
            variances[k] = np.average((np.array(data) - means[k])**2, weights=resp[:,k])
            
        if np.allclose(old_means, means, rtol=tol):
            break
            
    # Calculate boundaries between components
    edges = [min(data)]
    sorted_means = sorted(means)
    for i in range(len(sorted_means)-1):
        edges.append((sorted_means[i] + sorted_means[i+1])/2)
    edges.append(max(data))
    
    # Assign labels
    labels = []
    for x in data:
        for i in range(n):
            if edges[i] <= x <= edges[i+1]:
                labels.append(i)
                break
                
    return labels, edges

def hierarchical_density_merge(data: Union[List, Tuple, np.ndarray, Sequence],
                             n: int,
                             min_cluster_size: int = 5) -> Tuple[List[int], List[float]]:
    """Hierarchical density-based clustering for 1D data
    
    Args:
        data: Input data in various formats
        n: Number of clusters
        min_cluster_size: Minimum points per cluster
        
    Returns:
        Tuple containing:
            labels: Cluster labels for each data point
            edges: Cluster boundaries
    """
    data = _convert_to_list(data)
    sorted_data = sorted(data)
    
    # Calculate point density using adaptive radius
    data_range = max(data) - min(data)
    radius = data_range / (4 * n)  # Adaptive radius
    
    densities = []
    for x in data:
        density = sum(1 for y in data if abs(x - y) <= radius)
        densities.append((density, x))
    
    # Sort points by density
    density_points = sorted(densities, reverse=True)
    
    # Initialize clusters with high density points
    clusters = []
    used_points = set()
    
    for density, point in density_points:
        if point not in used_points:
            # Start new cluster
            cluster = [point]
            used_points.add(point)
            
            # Expand cluster
            for other_density, other_point in density_points:
                if other_point not in used_points:
                    if abs(other_point - point) <= radius:
                        cluster.append(other_point)
                        used_points.add(other_point)
            
            if len(cluster) >= min_cluster_size:
                clusters.append(cluster)
                
            if len(clusters) == n:
                break
    
    # Handle remaining points
    for x in data:
        if x not in used_points:
            # Assign to nearest cluster
            min_dist = float('inf')
            nearest_cluster = None
            
            for i, cluster in enumerate(clusters):
                dist = min(abs(x - c) for c in cluster)
                if dist < min_dist:
                    min_dist = dist
                    nearest_cluster = i
                    
            clusters[nearest_cluster].append(x)
            used_points.add(x)
    
    # Calculate boundaries
    edges = [min(data)]
    cluster_bounds = []
    for cluster in clusters:
        cluster_bounds.append((min(cluster), max(cluster)))
    cluster_bounds.sort()
    
    for i in range(len(cluster_bounds)-1):
        edges.append((cluster_bounds[i][1] + cluster_bounds[i+1][0])/2)
    edges.append(max(data))
    
    # Assign labels
    labels = []
    for x in data:
        for i in range(n):
            if edges[i] <= x <= edges[i+1]:
                labels.append(i)
                break
    
    return labels, edges
















