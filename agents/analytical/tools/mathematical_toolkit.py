"""
Mathematical Toolkit for Data Analysis
Statistics, calculations, data processing
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    from scipy import stats
    from scipy.spatial import distance
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

try:
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class MathematicalToolkit:
    """
    Mathematical and statistical operations
    
    Capabilities:
    - Basic statistics (mean, median, std, etc.)
    - Correlation analysis
    - Time series analysis
    - Distance calculations
    - Outlier detection
    - Data normalization
    """
    
    def __init__(self):
        pass
    
    # ============================================
    # BASIC STATISTICS
    # ============================================
    
    def basic_stats(self, data: List[float]) -> Dict[str, float]:
        """
        Calculate basic statistics
        
        Args:
            data: List of numbers
            
        Returns:
            Dict with mean, median, std, min, max, quartiles
        """
        arr = np.array(data)
        
        return {
            'count': len(arr),
            'mean': float(np.mean(arr)),
            'median': float(np.median(arr)),
            'std': float(np.std(arr)),
            'variance': float(np.var(arr)),
            'min': float(np.min(arr)),
            'max': float(np.max(arr)),
            'range': float(np.max(arr) - np.min(arr)),
            'q1': float(np.percentile(arr, 25)),
            'q2': float(np.percentile(arr, 50)),  # Same as median
            'q3': float(np.percentile(arr, 75)),
            'iqr': float(np.percentile(arr, 75) - np.percentile(arr, 25))
        }
    
    def correlation(self, x: List[float], y: List[float]) -> float:
        """
        Calculate Pearson correlation coefficient
        
        Args:
            x, y: Two variables
            
        Returns:
            Correlation coefficient (-1 to 1)
        """
        return float(np.corrcoef(x, y)[0, 1])
    
    def moving_average(self, data: List[float], window: int = 3) -> List[float]:
        """
        Calculate moving average
        
        Args:
            data: Time series data
            window: Window size
            
        Returns:
            Smoothed data
        """
        result = np.convolve(data, np.ones(window)/window, mode='valid')
        return result.tolist()
    
    def normalize(self, data: List[float], method: str = 'minmax') -> List[float]:
        """
        Normalize data
        
        Args:
            data: Data to normalize
            method: 'minmax' (0-1) or 'zscore' (mean=0, std=1)
            
        Returns:
            Normalized data
        """
        arr = np.array(data)
        
        if method == 'minmax':
            min_val = np.min(arr)
            max_val = np.max(arr)
            if max_val == min_val:
                return [0.5] * len(arr)
            normalized = (arr - min_val) / (max_val - min_val)
        
        elif method == 'zscore':
            mean = np.mean(arr)
            std = np.std(arr)
            if std == 0:
                return [0.0] * len(arr)
            normalized = (arr - mean) / std
        
        else:
            raise ValueError(f"Unknown normalization method: {method}")
        
        return normalized.tolist()
    
    def detect_outliers(self, data: List[float], threshold: float = 3.0) -> List[int]:
        """
        Detect outliers using z-score method
        
        Args:
            data: Data to analyze
            threshold: Z-score threshold (typically 2-3)
            
        Returns:
            List of outlier indices
        """
        arr = np.array(data)
        mean = np.mean(arr)
        std = np.std(arr)
        
        if std == 0:
            return []
        
        z_scores = np.abs((arr - mean) / std)
        outlier_indices = np.where(z_scores > threshold)[0]
        
        return outlier_indices.tolist()
    
    # ============================================
    # DISTANCE & SIMILARITY
    # ============================================
    
    def euclidean_distance(self, point1: Tuple[float, ...], 
                          point2: Tuple[float, ...]) -> float:
        """
        Calculate Euclidean distance
        
        Args:
            point1, point2: Coordinate tuples
            
        Returns:
            Distance
        """
        return float(np.linalg.norm(np.array(point1) - np.array(point2)))
    
    def distance_matrix(self, points: List[Tuple[float, ...]]) -> np.ndarray:
        """
        Calculate distance matrix between all points
        
        Args:
            points: List of coordinate tuples
            
        Returns:
            Distance matrix (n x n)
        """
        points_array = np.array(points)
        n = len(points_array)
        distances = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                distances[i, j] = np.linalg.norm(points_array[i] - points_array[j])
        
        return distances
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity
        
        Args:
            vec1, vec2: Vectors
            
        Returns:
            Similarity (0 to 1)
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        dot_product = np.dot(v1, v2)
        norm_product = np.linalg.norm(v1) * np.linalg.norm(v2)
        
        if norm_product == 0:
            return 0.0
        
        return float(dot_product / norm_product)
    
    # ============================================
    # GEOMETRIC CALCULATIONS
    # ============================================
    
    def angle_between_vectors(self, vec1: Tuple[float, ...], 
                             vec2: Tuple[float, ...]) -> float:
        """
        Calculate angle between two vectors
        
        Args:
            vec1, vec2: Vectors
            
        Returns:
            Angle in degrees
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        cos_angle = np.clip(cos_angle, -1, 1)  # Handle numerical errors
        
        angle_rad = np.arccos(cos_angle)
        angle_deg = np.degrees(angle_rad)
        
        return float(angle_deg)
    
    def bearing_between_points(self, lat1: float, lon1: float, 
                               lat2: float, lon2: float) -> float:
        """
        Calculate bearing (direction) between two geographic points
        
        Args:
            lat1, lon1: First point (degrees)
            lat2, lon2: Second point (degrees)
            
        Returns:
            Bearing in degrees (0-360, 0=North)
        """
        # Convert to radians
        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        diff_lon = np.radians(lon2 - lon1)
        
        # Calculate bearing
        x = np.sin(diff_lon) * np.cos(lat2_rad)
        y = np.cos(lat1_rad) * np.sin(lat2_rad) - \
            np.sin(lat1_rad) * np.cos(lat2_rad) * np.cos(diff_lon)
        
        bearing_rad = np.arctan2(x, y)
        bearing_deg = (np.degrees(bearing_rad) + 360) % 360
        
        return float(bearing_deg)
    
    # ============================================
    # ADVANCED STATISTICS (requires SciPy)
    # ============================================
    
    def statistical_test(self, group1: List[float], group2: List[float], 
                        test: str = 'ttest') -> Dict:
        """
        Statistical comparison of two groups
        
        Args:
            group1, group2: Data groups
            test: 'ttest' or 'mannwhitney'
            
        Returns:
            Test results
        """
        if not HAS_SCIPY:
            return {"error": "SciPy not installed"}
        
        if test == 'ttest':
            statistic, pvalue = stats.ttest_ind(group1, group2)
            test_name = "Independent t-test"
        elif test == 'mannwhitney':
            statistic, pvalue = stats.mannwhitney(group1, group2)
            test_name = "Mann-Whitney U test"
        else:
            return {"error": f"Unknown test: {test}"}
        
        return {
            'test': test_name,
            'statistic': float(statistic),
            'pvalue': float(pvalue),
            'significant_005': pvalue < 0.05,
            'significant_001': pvalue < 0.01,
            'interpretation': 'Groups differ significantly' if pvalue < 0.05 else 'No significant difference'
        }
    
    def correlation_test(self, x: List[float], y: List[float], 
                        method: str = 'pearson') -> Dict:
        """
        Test correlation significance
        
        Args:
            x, y: Variables
            method: 'pearson' or 'spearman'
            
        Returns:
            Correlation and significance
        """
        if not HAS_SCIPY:
            return {"error": "SciPy not installed"}
        
        if method == 'pearson':
            corr, pvalue = stats.pearsonr(x, y)
            test_name = "Pearson correlation"
        elif method == 'spearman':
            corr, pvalue = stats.spearmanr(x, y)
            test_name = "Spearman correlation"
        else:
            return {"error": f"Unknown method: {method}"}
        
        # Interpret strength
        abs_corr = abs(corr)
        if abs_corr > 0.7:
            strength = "strong"
        elif abs_corr > 0.4:
            strength = "moderate"
        elif abs_corr > 0.2:
            strength = "weak"
        else:
            strength = "very weak"
        
        return {
            'method': test_name,
            'correlation': float(corr),
            'pvalue': float(pvalue),
            'significant': pvalue < 0.05,
            'strength': strength,
            'direction': 'positive' if corr > 0 else 'negative'
        }
    
    # ============================================
    # CLUSTERING (requires scikit-learn)
    # ============================================
    
    def cluster_data(self, data: List[List[float]], n_clusters: int = 3) -> Dict:
        """
        Cluster data using K-Means
        
        Args:
            data: Data points (list of lists)
            n_clusters: Number of clusters
            
        Returns:
            Cluster labels and centers
        """
        if not HAS_SKLEARN:
            return {"error": "scikit-learn not installed"}
        
        data_array = np.array(data)
        
        # Normalize data
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_array)
        
        # Cluster
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(data_scaled)
        
        # Get cluster sizes
        unique, counts = np.unique(labels, return_counts=True)
        cluster_sizes = dict(zip(unique.tolist(), counts.tolist()))
        
        return {
            'labels': labels.tolist(),
            'n_clusters': n_clusters,
            'cluster_sizes': cluster_sizes,
            'inertia': float(kmeans.inertia_)  # Lower is better
        }
    
    def detect_anomalies_isolation(self, data: List[List[float]], 
                                   contamination: float = 0.1) -> Dict:
        """
        Detect anomalies using Isolation Forest
        
        Args:
            data: Data points
            contamination: Expected proportion of anomalies
            
        Returns:
            Anomaly predictions
        """
        if not HAS_SKLEARN:
            return {"error": "scikit-learn not installed"}
        
        from sklearn.ensemble import IsolationForest
        
        data_array = np.array(data)
        
        model = IsolationForest(contamination=contamination, random_state=42)
        predictions = model.fit_predict(data_array)
        
        # -1 = anomaly, 1 = normal
        anomaly_indices = np.where(predictions == -1)[0].tolist()
        
        return {
            'anomaly_indices': anomaly_indices,
            'n_anomalies': len(anomaly_indices),
            'n_normal': len(predictions) - len(anomaly_indices),
            'anomaly_ratio': len(anomaly_indices) / len(predictions)
        }
    
    # ============================================
    # UTILITY
    # ============================================
    
    def get_available_tools(self) -> Dict:
        """List available mathematical tools"""
        return {
            "basic_statistics": [
                "basic_stats (mean, median, std, quartiles, etc.)",
                "correlation",
                "moving_average",
                "normalize",
                "detect_outliers"
            ],
            "distance_similarity": [
                "euclidean_distance",
                "distance_matrix",
                "cosine_similarity"
            ],
            "geometric": [
                "angle_between_vectors",
                "bearing_between_points (for geolocation)"
            ],
            "advanced_statistics": [
                "statistical_test (requires SciPy)",
                "correlation_test (requires SciPy)"
            ],
            "machine_learning": [
                "cluster_data (requires scikit-learn)",
                "detect_anomalies_isolation (requires scikit-learn)"
            ],
            "dependencies": {
                "numpy": True,  # Always required
                "pandas": HAS_PANDAS,
                "scipy": HAS_SCIPY,
                "sklearn": HAS_SKLEARN
            },
            "status": "Ready for mathematical operations"
        }


# Test
if __name__ == "__main__":
    print("🧮 Mathematical Toolkit Test\n")
    
    toolkit = MathematicalToolkit()
    tools = toolkit.get_available_tools()
    
    print("Available Tools:")
    for category, tool_list in tools.items():
        if category not in ["status", "dependencies"]:
            print(f"\n{category.upper().replace('_', ' ')}:")
            for tool in tool_list:
                print(f"  ✓ {tool}")
    
    print(f"\nDependencies:")
    for dep, available in tools["dependencies"].items():
        status = "✅" if available else "❌"
        print(f"  {status} {dep}")
    
    print(f"\n{tools['status']}")
    
    # Test basic stats
    print("\n--- Test: Basic Statistics ---")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
    stats = toolkit.basic_stats(data)
    print(f"Mean: {stats['mean']:.2f}")
    print(f"Median: {stats['median']:.2f}")
    print(f"Std: {stats['std']:.2f}")
    
    outliers = toolkit.detect_outliers(data, threshold=2)
    print(f"Outliers detected at indices: {outliers}")
    print("✅ Basic statistics work!")
    
    # Test distance
    print("\n--- Test: Distance Calculation ---")
    warsaw = (52.2297, 21.0122)
    london = (51.5074, -0.1278)
    distance = toolkit.euclidean_distance(warsaw, london)
    print(f"Distance Warsaw-London: {distance:.2f} (coordinate units)")
    
    bearing = toolkit.bearing_between_points(*warsaw, *london)
    print(f"Bearing from Warsaw to London: {bearing:.1f}° (from North)")
    print("✅ Geographic calculations work!")
