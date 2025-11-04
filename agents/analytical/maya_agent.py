"""
Maya Patel - Data Analyst
Statistical Analysis and Visualization Expert
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class MayaAgent(BaseAgent):
    """
    Maya Patel - Data Analyst
    
    Role: Statistical Analysis and Visualization Expert
    Specialization: Data analysis, statistical modeling, visualization,
                   data quality assessment, predictive analytics
    
    Capabilities:
    - Descriptive statistics
    - Correlation and regression analysis
    - Hypothesis testing
    - Data visualization and dashboards
    - Predictive modeling
    - Data quality assessment
    """
    
    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Maya Patel",
            role="Data Analyst",
            specialization="Statistical analysis, Data visualization, Predictive analytics, Data quality",
            project_id=project_id
        )
        
        # Initialize Data Analysis Toolkit
        from agents.analytical.tools.data_analysis_toolkit import DataAnalysisToolkit
        self.toolkit = DataAnalysisToolkit()
        self.tools = self.toolkit.get_available_tools()
    
    def _execute_work(self, task: Task) -> TaskResult:
        """Execute data analysis work"""
        
        start_time = datetime.now()
        task_lower = task.description.lower()
        
        context = self.load_context(task.description, limit=3)
        
        if any(word in task_lower for word in ["statistics", "statistical", "descriptive"]):
            result = self._statistical_analysis(task, context)
        elif any(word in task_lower for word in ["visualization", "chart", "dashboard", "graph"]):
            result = self._data_visualization(task, context)
        elif any(word in task_lower for word in ["quality", "cleaning", "clean data"]):
            result = self._data_quality_assessment(task, context)
        elif any(word in task_lower for word in ["predict", "forecast", "model", "machine learning"]):
            result = self._predictive_analytics(task, context)
        elif any(word in task_lower for word in ["correlation", "relationship", "regression"]):
            result = self._correlation_analysis(task, context)
        else:
            result = self._general_data_analysis(task, context)
        
        return result
    
    def _statistical_analysis(self, task: Task, context: list) -> TaskResult:
        """Statistical analysis and hypothesis testing"""
        
        thoughts = f"""
📊 STATISTICAL ANALYSIS - Maya Patel

Request: {task.title}

STATISTICAL ANALYSIS FRAMEWORK:

🔍 Descriptive Statistics:

MEASURES OF CENTRAL TENDENCY:
- Mean (average) - sum / count
- Median (middle value) - 50th percentile
- Mode (most frequent) - peak of distribution
- Use: Mean for normal data, median for skewed

MEASURES OF DISPERSION:
- Range (max - min) - spread of data
- Variance (σ²) - average squared deviation
- Standard Deviation (σ) - typical deviation from mean
- IQR (Q3 - Q1) - middle 50% spread
- Coefficient of Variation (CV) - σ/μ normalized spread

MEASURES OF SHAPE:
- Skewness - symmetry measure
  * Negative: left tail (mean < median)
  * Zero: symmetric (normal)
  * Positive: right tail (mean > median)
- Kurtosis - tail heaviness
  * Leptokurtic: heavy tails (outliers)
  * Mesokurtic: normal tails
  * Platykurtic: light tails

📈 Inferential Statistics:

1. HYPOTHESIS TESTING:

   Framework:
   - Null Hypothesis (H₀): No effect/difference
   - Alternative Hypothesis (H₁): Effect exists
   - Significance Level (α): Usually 0.05 (5%)
   - P-value: Probability of observing data if H₀ true
   
   Decision Rule:
   - If p-value < α: Reject H₀ (statistically significant)
   - If p-value ≥ α: Fail to reject H₀ (not significant)

2. COMMON TESTS:

   T-TEST (comparing means):
   - One-sample: Compare sample mean to known value
   - Two-sample: Compare two group means
   - Paired: Compare before/after measurements
   - Assumptions: Normal distribution, equal variances
   
   Example: "Is average customer satisfaction higher after redesign?"
   - H₀: No change in satisfaction
   - H₁: Satisfaction increased
   - Run paired t-test on before/after scores

   CHI-SQUARE TEST (categorical data):
   - Test independence of two variables
   - Example: "Is purchase behavior independent of age group?"
   - Assumptions: Expected frequency ≥ 5 in each cell

   ANOVA (comparing 3+ groups):
   - One-way: One factor, multiple levels
   - Example: "Do sales differ across 4 regions?"
   - Post-hoc tests if significant (Tukey, Bonferroni)

   MANN-WHITNEY U (non-parametric):
   - Alternative to t-test when not normal
   - Compares distributions without normality assumption

3. CONFIDENCE INTERVALS:

   95% Confidence Interval:
   - "We are 95% confident the true value lies in this range"
   - Narrower CI = more precise estimate
   - Larger sample = narrower CI
   
   Interpretation:
   - [45, 55]: Plausible range for true parameter
   - If CI doesn't include 0: Statistically significant effect

4. EFFECT SIZE:

   Beyond p-values (practical significance):
   - Cohen's d: Standardized mean difference
     * Small: 0.2
     * Medium: 0.5
     * Large: 0.8
   - R²: Proportion of variance explained
   - Correlation strength:
     * Weak: |r| < 0.3
     * Moderate: 0.3 ≤ |r| < 0.7
     * Strong: |r| ≥ 0.7

📊 Data Distribution Analysis:

NORMALITY TESTS:
- Visual: Histogram, Q-Q plot
- Statistical: Shapiro-Wilk, Kolmogorov-Smirnov
- Rule of thumb: n > 30 → approximate normality (CLT)

OUTLIER DETECTION:
- IQR method: <Q1-1.5×IQR or >Q3+1.5×IQR
- Z-score: |z| > 3 (for normal data)
- Visual: Box plot, scatter plot

TOOLS AVAILABLE:
✓ {self.toolkit.descriptive_statistics.__name__} - Full descriptive stats
✓ {self.toolkit.correlation_analysis.__name__} - Pearson correlation
✓ {self.toolkit.hypothesis_test.__name__} - Various hypothesis tests
✓ {self.toolkit.outlier_detection.__name__} - IQR and Z-score methods

STATISTICAL ANALYSIS DELIVERABLES:

1. Descriptive Statistics Report:
   - Summary statistics table
   - Distribution visualizations
   - Outlier identification

2. Hypothesis Test Results:
   - Test selection rationale
   - Assumptions validation
   - Test statistic and p-value
   - Effect size
   - Confidence intervals
   - Interpretation in business context

3. Recommendations:
   - Statistical significance
   - Practical significance
   - Sample size considerations
   - Data quality notes

COLLABORATION:
- Sofia (Market Research): Survey data analysis
- Marcus (Financial): Financial metrics analysis
- Lucas (Report Writer): Statistical report writing

Ready for statistical analysis! 📊
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "analysis_type": "Statistical Analysis",
                "capabilities": ["Descriptive stats", "Hypothesis testing", "Confidence intervals", "Effect size"],
                "tests_available": ["t-test", "Chi-square", "ANOVA", "Mann-Whitney"],
                "tools": list(self.tools.get("statistical_analysis", []))
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "statistical_analysis_report.pdf",
                "descriptive_stats.xlsx",
                "hypothesis_test_results.pdf",
                "data_visualizations.png"
            ],
            next_steps="Provide dataset for statistical analysis"
        )
    
    def _data_visualization(self, task: Task, context: list) -> TaskResult:
        """Data visualization and dashboard creation"""
        
        thoughts = f"""
📈 DATA VISUALIZATION - Maya Patel

Request: {task.title}

VISUALIZATION DESIGN FRAMEWORK:

🎨 Chart Selection Guide:

1. COMPARISON (comparing values):
   
   BAR CHART (categorical comparison):
   - Use when: Comparing categories
   - Example: Sales by region, product ratings
   - Orientation: Horizontal for long labels, vertical for time
   
   COLUMN CHART (time comparison):
   - Use when: Comparing over time periods
   - Example: Monthly revenue, quarterly growth
   
   GROUPED BAR (multi-series comparison):
   - Use when: Comparing multiple series across categories
   - Example: Sales by region and product line

2. DISTRIBUTION (showing spread):
   
   HISTOGRAM (frequency distribution):
   - Use when: Showing distribution of continuous variable
   - Example: Age distribution, response time distribution
   - Bins: 5-20 bins typically
   
   BOX PLOT (quartile distribution):
   - Use when: Comparing distributions, showing outliers
   - Shows: Min, Q1, median, Q3, max, outliers
   - Example: Salary by department
   
   VIOLIN PLOT (density + distribution):
   - Combines: Box plot + density curve
   - Use when: Detailed distribution comparison

3. RELATIONSHIP (showing correlation):
   
   SCATTER PLOT (two variables):
   - Use when: Exploring correlation between variables
   - Example: Price vs quality rating, age vs income
   - Add: Trend line for relationship
   
   BUBBLE CHART (three variables):
   - X-axis: Variable 1
   - Y-axis: Variable 2
   - Size: Variable 3
   - Example: Revenue vs profit (size = market share)
   
   CORRELATION MATRIX (multiple variables):
   - Use when: Exploring all pairwise correlations
   - Heatmap format with color intensity

4. COMPOSITION (showing parts of whole):
   
   PIE CHART (proportions):
   - Use when: Showing parts of 100%
   - Limit: 5-7 slices maximum
   - Alternative: Donut chart
   - ⚠️ Use sparingly: Hard to compare angles
   
   STACKED BAR (composition over categories):
   - Use when: Parts + categories
   - Example: Revenue by product line over years
   
   TREEMAP (hierarchical composition):
   - Use when: Nested proportions
   - Example: Budget breakdown by department and category

5. TREND (showing change over time):
   
   LINE CHART (continuous time series):
   - Use when: Showing trend over time
   - Example: Stock price, website traffic
   - Multiple lines: Compare trends
   
   AREA CHART (cumulative trends):
   - Use when: Showing magnitude + trend
   - Stacked: Multiple series composition
   
   SPARKLINES (inline mini-charts):
   - Use when: Showing trend in table context
   - Very compact, no axes

6. ADVANCED VISUALIZATIONS:
   
   HEATMAP (matrix intensity):
   - Use when: Large matrix data
   - Example: Correlation matrix, time-of-day patterns
   
   SANKEY DIAGRAM (flow):
   - Use when: Showing flow between stages
   - Example: Customer journey, budget allocation
   
   NETWORK GRAPH (relationships):
   - Use when: Showing connections
   - Example: Social network, transaction flows

📊 Dashboard Design:

LAYOUT PRINCIPLES:

1. HIERARCHY:
   - Top: Key metrics (KPIs) in cards
   - Middle: Primary visualizations (large)
   - Bottom: Detail/drill-down (smaller)
   - Left-to-right, top-to-bottom reading flow

2. KPI CARDS (top row):
   ┌──────────┬──────────┬──────────┬──────────┐
   │ Revenue  │ Customers│ Growth % │ Churn %  │
   │ $1.2M    │ 5,432    │ +15%     │ 3.2%     │
   │ ↑ +12%   │ ↑ +8%    │ ↑        │ ↓ -0.5%  │
   └──────────┴──────────┴──────────┴──────────┘

3. MAIN VISUALIZATIONS (middle):
   ┌──────────────────────┬──────────────┐
   │  Revenue Trend       │  Top Products│
   │  (Line Chart)        │  (Bar Chart) │
   │                      │              │
   └──────────────────────┴──────────────┘

4. INTERACTIVITY:
   - Date range selector
   - Category filters
   - Drill-down on click
   - Export options (PDF, Excel, PNG)

DESIGN BEST PRACTICES:

COLOR SCHEME:
✓ Use consistent color palette (3-5 colors)
✓ Color-blind friendly (avoid red-green only)
✓ Use color meaningfully (e.g., red = negative)
✓ Neutral background (white or light gray)

TYPOGRAPHY:
✓ Clear, readable fonts (Arial, Helvetica)
✓ Hierarchy: Title 18pt, subtitle 14pt, body 11pt
✓ Bold for emphasis, not decoration

VISUAL CLARITY:
✓ Remove chartjunk (unnecessary elements)
✓ Direct labeling > legend (when possible)
✓ Clear axis labels with units
✓ Source attribution
✓ High contrast (text on background)

DATA-INK RATIO:
- Maximize data ink (actual data points)
- Minimize non-data ink (gridlines, borders)
- Remove every element that doesn't add information

📊 Tools and Technologies:

PYTHON STACK:
- matplotlib: Static plots, publication quality
- seaborn: Statistical visualizations, attractive defaults
- plotly: Interactive plots, web-ready
- pandas: Built-in plotting (quick EDA)

JAVASCRIPT/WEB:
- Chart.js: Simple, responsive charts
- D3.js: Custom, complex visualizations
- Plotly.js: Interactive scientific plots
- Highcharts: Professional business charts

BUSINESS INTELLIGENCE:
- Tableau: Enterprise dashboards
- Power BI: Microsoft ecosystem
- Looker: Data exploration
- Metabase: Open source BI

TOOLS AVAILABLE:
✓ {self.toolkit.create_chart_config.__name__} - Chart configuration
✓ {self.toolkit.dashboard_layout.__name__} - Dashboard design

VISUALIZATION DELIVERABLES:

1. Static Charts (PDF/PNG):
   - High resolution (300 DPI for print)
   - Professional styling
   - Clear annotations

2. Interactive Dashboard (HTML):
   - Web-based, shareable link
   - Filters and drill-downs
   - Responsive design (mobile-friendly)

3. Dashboard Specification:
   - Layout mockup
   - Data requirements
   - Interactivity design
   - Refresh schedule

COLLABORATION:
- Sofia (Market Research): Market trend visualizations
- Marcus (Financial): Financial dashboards
- Lucas (Report Writer): Charts for reports

Ready for data visualization! 📈
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "analysis_type": "Data Visualization",
                "chart_types": ["Bar", "Line", "Scatter", "Pie", "Heatmap", "Dashboard"],
                "tools": ["matplotlib", "seaborn", "plotly", "Chart.js", "D3.js"],
                "deliverables": ["Static charts", "Interactive dashboard", "Dashboard spec"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "data_visualizations.pdf",
                "interactive_dashboard.html",
                "dashboard_specification.pdf",
                "chart_data.xlsx"
            ],
            next_steps="Provide data and visualization requirements"
        )
    
    def _data_quality_assessment(self, task: Task, context: list) -> TaskResult:
        """Data quality assessment and cleaning"""
        
        thoughts = f"""
🧹 DATA QUALITY ASSESSMENT - Maya Patel

Request: {task.title}

DATA QUALITY FRAMEWORK:

📊 Quality Dimensions:

1. COMPLETENESS (Missing Data):
   
   Assessment:
   - % of missing values per column
   - Patterns in missingness (MCAR, MAR, MNAR)
   - Critical vs non-critical fields
   
   Handling Strategies:
   - Delete: If <5% missing and MCAR
   - Impute: Mean/median (numeric), mode (categorical)
   - Model: Predict missing values
   - Flag: Keep but mark as missing
   
   Example:
   | Column        | Missing | Strategy      |
   |---------------|---------|---------------|
   | Customer ID   | 0%      | None needed   |
   | Email         | 15%     | Required field|
   | Phone         | 40%     | Optional, keep|
   | Purchase Date | 2%      | Delete rows   |

2. ACCURACY (Correctness):
   
   Validation Checks:
   - Range checks (age: 0-120)
   - Format checks (email regex)
   - Business rule checks (end date > start date)
   - Cross-field validation (city matches zip code)
   
   Common Issues:
   - Typos and misspellings
   - Wrong data type (text in numeric field)
   - Invalid values (negative age)
   - Referential integrity violations

3. CONSISTENCY (Uniformity):
   
   Issues:
   - Units inconsistency (USD vs EUR, km vs miles)
   - Date format variance (MM/DD vs DD/MM)
   - Capitalization (New York vs NEW YORK vs new york)
   - Duplicate representations (USA vs US vs United States)
   
   Standardization:
   - Choose canonical format
   - Apply transformations
   - Document standards

4. UNIQUENESS (Duplicates):
   
   Detection:
   - Exact duplicates (all fields identical)
   - Near duplicates (fuzzy matching)
     * Levenshtein distance
     * Phonetic matching (Soundex)
   
   Resolution:
   - Keep most recent record
   - Merge records (combine information)
   - Flag for manual review
   
   Example:
   - "John Smith, jsmith@email.com"
   - "J. Smith, jsmith@email.com" ← Likely duplicate

5. TIMELINESS (Currency):
   
   Assessment:
   - Data age (time since collection)
   - Update frequency
   - Staleness indicators
   
   Actions:
   - Refresh stale data
   - Archive outdated records
   - Set expiration dates

6. VALIDITY (Conformance):
   
   Schema Validation:
   - Data types correct
   - Required fields present
   - Constraints satisfied
   - Foreign keys valid

🔍 Data Profiling:

UNIVARIATE ANALYSIS (per column):
- Data type (string, integer, float, date)
- Distinct values count
- Missing value count
- Min/max/mean/median
- Most frequent values
- Outliers

MULTIVARIATE ANALYSIS (across columns):
- Correlation matrix
- Dependency detection
- Referential integrity
- Business rule validation

📋 Data Quality Score:

Weighted Scoring:
- Completeness: 30%
- Accuracy: 25%
- Consistency: 20%
- Uniqueness: 15%
- Timeliness: 10%

Total Score: 0-100
- 90-100: Excellent
- 75-89: Good
- 60-74: Fair
- <60: Poor (remediation required)

TOOLS AVAILABLE:
✓ {self.toolkit.data_quality_report.__name__} - Comprehensive DQ assessment
✓ {self.toolkit.data_transformation_plan.__name__} - ETL pipeline design

DATA CLEANING WORKFLOW:

1. PROFILE:
   - Run data quality assessment
   - Identify issues
   - Prioritize by impact

2. CLEAN:
   - Remove duplicates
   - Handle missing values
   - Fix inconsistencies
   - Validate ranges

3. TRANSFORM:
   - Standardize formats
   - Convert data types
   - Normalize units
   - Create derived fields

4. VALIDATE:
   - Re-run quality checks
   - Verify improvements
   - Document changes
   - Get stakeholder sign-off

5. DOCUMENT:
   - Data dictionary
   - Cleaning decisions
   - Transformation logic
   - Quality metrics

DELIVERABLES:

1. Data Quality Report:
   - Quality score per dimension
   - Issues identified (with examples)
   - Recommendations
   - Priority actions

2. Clean Dataset:
   - Cleaned data file
   - Cleaning log (what changed)
   - Rejected records (with reasons)
   - Data dictionary

3. Transformation Pipeline:
   - Automated cleaning script
   - Validation rules
   - Error handling
   - Monitoring

COLLABORATION:
- Alex (Technical Liaison): ETL pipeline implementation
- Sofia (Market Research): Survey data cleaning
- Lucas (Report Writer): Quality documentation

Ready for data quality assessment! 🧹
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "analysis_type": "Data Quality",
                "dimensions": ["Completeness", "Accuracy", "Consistency", "Uniqueness", "Timeliness", "Validity"],
                "deliverables": ["Quality report", "Clean dataset", "Transformation pipeline"],
                "quality_score": "0-100 weighted scoring"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "data_quality_report.pdf",
                "cleaned_dataset.csv",
                "cleaning_log.xlsx",
                "transformation_pipeline.py"
            ],
            next_steps="Provide dataset for quality assessment"
        )
    
    def _predictive_analytics(self, task: Task, context: list) -> TaskResult:
        """Predictive modeling and machine learning"""
        
        thoughts = f"""
🔮 PREDICTIVE ANALYTICS - Maya Patel

Request: {task.title}

PREDICTIVE MODELING FRAMEWORK:

🎯 Problem Type Classification:

1. REGRESSION (predicting continuous values):
   - Examples: Revenue forecast, price prediction, demand estimation
   - Output: Numeric value
   - Evaluation: R², RMSE, MAE

2. CLASSIFICATION (predicting categories):
   - Binary: Churn (yes/no), fraud (yes/no)
   - Multi-class: Customer segment (A/B/C), risk level (low/med/high)
   - Output: Category or probability
   - Evaluation: Accuracy, precision, recall, F1, AUC-ROC

3. TIME SERIES (forecasting over time):
   - Examples: Sales forecast, stock price, website traffic
   - Special consideration: Temporal dependencies
   - Evaluation: MAPE, RMSE, MAE

4. CLUSTERING (finding groups):
   - Examples: Customer segmentation, anomaly detection
   - Unsupervised learning
   - Evaluation: Silhouette score, Davies-Bouldin index

📊 Model Selection:

REGRESSION MODELS:
1. Linear Regression
   - Pro: Simple, interpretable, fast
   - Con: Assumes linearity, sensitive to outliers
   - Use: Clear linear relationships

2. Random Forest Regression
   - Pro: Handles non-linearity, robust to outliers
   - Con: Black box, slower
   - Use: Complex relationships, feature importance needed

3. XGBoost
   - Pro: High accuracy, handles missing data
   - Con: Requires tuning, computational cost
   - Use: Kaggle competitions, production systems

CLASSIFICATION MODELS:
1. Logistic Regression
   - Pro: Probabilistic output, interpretable
   - Con: Assumes linearity, limited complexity
   - Use: Binary classification, baseline model

2. Random Forest Classifier
   - Pro: High accuracy, feature importance
   - Con: Overfitting risk, memory intensive
   - Use: General purpose classification

3. Neural Networks
   - Pro: Handles complex patterns
   - Con: Requires large data, black box
   - Use: Large datasets, complex problems

TIME SERIES MODELS:
1. ARIMA
   - Pro: Classical, well-understood
   - Con: Requires stationarity, manual tuning
   - Use: Short-term forecasts, single series

2. Prophet (Facebook)
   - Pro: Handles seasonality well, robust to missing data
   - Con: Limited customization
   - Use: Business forecasting with seasonality

3. LSTM (Neural Network)
   - Pro: Captures long-term dependencies
   - Con: Requires large data, slow training
   - Use: Complex temporal patterns

🔧 Modeling Workflow:

1. DATA PREPARATION:
   
   Split Data:
   - Training (60-70%): Model learns
   - Validation (15-20%): Hyperparameter tuning
   - Test (15-20%): Final evaluation
   
   Time Series Special: Use time-based splits (no random shuffling!)
   
   Feature Engineering:
   - Create derived features
   - Encode categorical variables (one-hot, label encoding)
   - Scale numeric features (standardization, normalization)
   - Handle missing values

2. MODEL TRAINING:
   
   Baseline Model:
   - Always start with simple model
   - Establish performance benchmark
   
   Cross-Validation:
   - K-fold (typically k=5 or 10)
   - Reduces overfitting
   - More reliable performance estimate
   
   Hyperparameter Tuning:
   - Grid search: Exhaustive
   - Random search: Efficient
   - Bayesian optimization: Smart search

3. MODEL EVALUATION:
   
   REGRESSION METRICS:
   - R²: 0-1, higher better (variance explained)
   - RMSE: Same units as target, lower better
   - MAE: Mean absolute error, lower better
   - MAPE: % error, lower better
   
   CLASSIFICATION METRICS:
   - Accuracy: Overall correct %
   - Precision: Of predicted positives, % actually positive
   - Recall: Of actual positives, % correctly identified
   - F1: Harmonic mean of precision and recall
   - AUC-ROC: 0.5-1.0, higher better
   
   Confusion Matrix:
   |           | Predicted + | Predicted - |
   |-----------|-------------|-------------|
   | Actual +  | TP          | FN          |
   | Actual -  | FP          | TN          |
   
   - TP: True Positive
   - FP: False Positive (Type I error)
   - FN: False Negative (Type II error)
   - TN: True Negative

4. MODEL INTERPRETATION:
   
   Feature Importance:
   - Which features matter most?
   - SHAP values: Local and global explanations
   - Permutation importance
   
   Residual Analysis:
   - Plot predicted vs actual
   - Check for patterns in residuals
   - Identify outliers

5. MODEL DEPLOYMENT:
   
   Production Considerations:
   - Inference speed
   - Model size
   - Retraining frequency
   - Monitoring and alerting
   
   API Design:
   - Input: Features
   - Output: Prediction + confidence
   - Versioning: Model version tracking

🎯 Use Case Examples:

CUSTOMER CHURN PREDICTION:
- Problem: Binary classification
- Features: Usage metrics, demographics, support tickets
- Model: Random Forest or XGBoost
- Output: Churn probability (0-1)
- Business action: Retention offers for high-risk customers

SALES FORECASTING:
- Problem: Time series regression
- Features: Historical sales, seasonality, promotions, economic indicators
- Model: Prophet or ARIMA
- Output: Sales forecast + confidence interval
- Business action: Inventory planning, staffing

CUSTOMER SEGMENTATION:
- Problem: Clustering (unsupervised)
- Features: Purchase behavior, demographics, engagement
- Model: K-Means or Hierarchical clustering
- Output: Customer segments
- Business action: Targeted marketing campaigns

TOOLS AVAILABLE:
✓ {self.toolkit.predictive_model_recommendation.__name__} - Model selection
✓ {self.toolkit.time_series_decomposition.__name__} - Time series analysis

DELIVERABLES:

1. Model Report:
   - Problem definition
   - Data exploration findings
   - Model selection rationale
   - Performance metrics
   - Feature importance

2. Trained Model:
   - Model file (.pkl, .h5, .joblib)
   - Feature preprocessing pipeline
   - Prediction API/function
   - Model card (documentation)

3. Validation Results:
   - Performance on test set
   - Cross-validation scores
   - Confusion matrix / residual plots
   - Business impact estimation

4. Deployment Plan:
   - Infrastructure requirements
   - API specification
   - Monitoring strategy
   - Retraining schedule

COLLABORATION:
- Alex (Technical): Model deployment and API
- Marcus (Financial): Financial forecasting
- Sofia (Market Research): Demand forecasting
- Viktor (Orchestrator): Business priorities

Ready for predictive analytics! 🔮
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "analysis_type": "Predictive Analytics",
                "problem_types": ["Regression", "Classification", "Time Series", "Clustering"],
                "models": ["Linear Regression", "Random Forest", "XGBoost", "ARIMA", "Prophet", "Neural Networks"],
                "deliverables": ["Model report", "Trained model", "Validation results", "Deployment plan"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "model_report.pdf",
                "trained_model.pkl",
                "validation_results.pdf",
                "feature_importance.png",
                "deployment_plan.md"
            ],
            next_steps="Define prediction problem and provide training data"
        )
    
    def _correlation_analysis(self, task: Task, context: list) -> TaskResult:
        """Correlation and relationship analysis"""
        
        thoughts = f"""
🔗 CORRELATION ANALYSIS - Maya Patel

Request: {task.title}

CORRELATION & RELATIONSHIP FRAMEWORK:

📊 Correlation Types:

1. PEARSON CORRELATION (linear relationship):
   - Range: -1 to +1
   - +1: Perfect positive correlation
   - 0: No linear correlation
   - -1: Perfect negative correlation
   
   Interpretation:
   - |r| ≥ 0.7: Strong correlation
   - 0.4 ≤ |r| < 0.7: Moderate correlation
   - |r| < 0.4: Weak correlation
   
   Assumptions:
   - Linear relationship
   - No outliers (sensitive!)
   - Normal distribution (for significance testing)
   
   Example:
   - Height vs Weight: r = 0.85 (strong positive)
   - Price vs Demand: r = -0.72 (strong negative)

2. SPEARMAN CORRELATION (monotonic relationship):
   - Rank-based (non-parametric)
   - Use when: Non-linear but monotonic
   - Robust to outliers
   - Good for ordinal data
   
   Example:
   - Customer satisfaction (1-5) vs loyalty

3. KENDALL TAU (concordant pairs):
   - Another rank-based measure
   - More conservative than Spearman
   - Good for small samples

🎯 Correlation vs Causation:

CRITICAL: Correlation ≠ Causation!

Examples of Spurious Correlations:
- Ice cream sales correlate with drowning deaths
  → Both caused by summer weather (confounding variable)
- Number of firefighters correlates with fire damage
  → Both caused by fire size (common cause)

Establishing Causation Requires:
1. Correlation exists
2. Temporal precedence (cause before effect)
3. No plausible alternative explanations
4. Theoretical mechanism

Methods for Causal Inference:
- Randomized controlled trials (RCT)
- Natural experiments
- Instrumental variables
- Regression discontinuity
- Difference-in-differences

📊 Multivariate Relationships:

CORRELATION MATRIX:
- All pairwise correlations
- Visualized as heatmap
- Identify multicollinearity

Example Matrix:
|        | Price | Quality | Size | Sales |
|--------|-------|---------|------|-------|
| Price  | 1.00  | 0.65    | 0.82 | -0.45 |
| Quality| 0.65  | 1.00    | 0.54 | 0.73  |
| Size   | 0.82  | 0.54    | 1.00 | -0.22 |
| Sales  | -0.45 | 0.73    | -0.22| 1.00  |

Insights:
- Quality strongly predicts Sales (r=0.73)
- Price and Size highly correlated (r=0.82) → multicollinearity risk
- Price negatively affects Sales (r=-0.45)

REGRESSION ANALYSIS:

Simple Linear Regression:
Y = β₀ + β₁X + ε

- Y: Dependent variable (what we predict)
- X: Independent variable (predictor)
- β₀: Intercept
- β₁: Slope (effect size)
- ε: Error term

Multiple Linear Regression:
Y = β₀ + β₁X₁ + β₂X₂ + ... + βₙXₙ + ε

- Controls for multiple factors
- Isolates effect of each variable
- Risk: Multicollinearity

Interpretation:
- β₁ = 0.5: One unit increase in X → 0.5 unit increase in Y (holding others constant)
- R²: Proportion of variance explained (0-1)
  * 0.7: 70% of variation in Y explained by model

REGRESSION DIAGNOSTICS:

Assumptions to Check:
1. Linearity: Relationship is linear
2. Independence: Observations independent
3. Homoscedasticity: Constant variance of residuals
4. Normality: Residuals normally distributed

Diagnostic Plots:
- Residuals vs Fitted: Check linearity and homoscedasticity
- Q-Q Plot: Check normality
- Cook's Distance: Identify influential points

🔍 Advanced Relationships:

INTERACTION EFFECTS:
- Combined effect of two variables
- Example: Marketing × Product Quality on Sales
- May be synergistic (1+1=3) or antagonistic (1+1=1)

NON-LINEAR RELATIONSHIPS:
- Polynomial regression: Y = β₀ + β₁X + β₂X² + ...
- Logarithmic: log(Y) = β₀ + β₁X
- Exponential: Y = e^(β₀ + β₁X)

CATEGORICAL RELATIONSHIPS:
- ANOVA: Compare means across groups
- Chi-square: Test independence of categorical variables
- Cramér's V: Effect size for chi-square (0-1)

TOOLS AVAILABLE:
✓ {self.toolkit.correlation_analysis.__name__} - Pearson correlation + interpretation
✓ {self.toolkit.descriptive_statistics.__name__} - Univariate analysis

ANALYSIS DELIVERABLES:

1. Correlation Report:
   - Correlation matrix (table + heatmap)
   - Strength interpretation
   - Significance testing
   - Key relationships identified

2. Regression Analysis (if applicable):
   - Model coefficients
   - R² and adjusted R²
   - P-values for predictors
   - Diagnostic plots

3. Insights and Recommendations:
   - Strongest relationships
   - Causal hypotheses (with caveats)
   - Business implications
   - Recommended actions

COLLABORATION:
- Sofia (Market Research): Consumer behavior correlations
- Marcus (Financial): Financial metric relationships
- Viktor (Orchestrator): Strategic implications

Ready for correlation analysis! 🔗
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "analysis_type": "Correlation Analysis",
                "methods": ["Pearson", "Spearman", "Kendall", "Regression"],
                "deliverables": ["Correlation matrix", "Regression results", "Insights"],
                "caution": "Correlation ≠ Causation"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "correlation_report.pdf",
                "correlation_matrix_heatmap.png",
                "regression_analysis.pdf",
                "diagnostic_plots.png"
            ],
            next_steps="Provide dataset with variables to analyze"
        )
    
    def _general_data_analysis(self, task: Task, context: list) -> TaskResult:
        """General data analysis support"""
        
        thoughts = f"""
📊 DATA ANALYSIS - Maya Patel

Request: {task.title}

DATA ANALYSIS CAPABILITIES:

🎯 ANALYSIS TYPES:

1. Statistical Analysis:
   ✓ Descriptive statistics
   ✓ Hypothesis testing
   ✓ Confidence intervals
   ✓ Effect size analysis

2. Data Visualization:
   ✓ Charts (bar, line, scatter, etc.)
   ✓ Interactive dashboards
   ✓ Statistical plots
   ✓ Professional reports

3. Data Quality:
   ✓ Quality assessment (6 dimensions)
   ✓ Data cleaning
   ✓ Transformation pipelines
   ✓ Validation rules

4. Predictive Analytics:
   ✓ Regression models
   ✓ Classification models
   ✓ Time series forecasting
   ✓ Clustering/segmentation

5. Correlation & Relationships:
   ✓ Correlation analysis
   ✓ Regression analysis
   ✓ Causal inference support

🔧 TOOLS & TECHNOLOGIES:

Python Stack:
- pandas: Data manipulation
- numpy: Numerical computing
- scipy: Statistical functions
- matplotlib: Visualization
- seaborn: Statistical plots
- plotly: Interactive charts
- scikit-learn: Machine learning
- statsmodels: Statistical models

{chr(10).join([f'✓ {category}: {len(tools)} capabilities' for category, tools in self.tools.items() if category not in ['status', 'python_stack']])}

📊 TYPICAL WORKFLOW:

1. DATA UNDERSTANDING:
   - Profile data
   - Identify data types
   - Check quality
   - Explore distributions

2. DATA PREPARATION:
   - Clean missing values
   - Handle outliers
   - Transform variables
   - Create features

3. ANALYSIS:
   - Descriptive statistics
   - Visualizations
   - Statistical tests
   - Modeling (if needed)

4. INTERPRETATION:
   - Translate results to business context
   - Identify actionable insights
   - Quantify impact
   - Make recommendations

5. COMMUNICATION:
   - Executive summary
   - Detailed report
   - Visualizations
   - Dashboard (if needed)

🤝 TEAM COLLABORATION:

With Sofia (Market Research):
- Survey data analysis
- Consumer behavior insights
- Market segmentation

With Marcus (Financial):
- Financial metrics analysis
- Performance dashboards
- Forecasting models

With Elena (OSINT):
- Social media data analysis
- Trend analysis

With Alex (Technical Liaison):
- Data pipeline setup
- Database queries
- ETL processes

With Lucas (Report Writer):
- Statistical reports
- Data visualizations for reports
- Dashboard documentation

📈 DELIVERABLE FORMATS:

Reports:
- PDF: Professional, static
- HTML: Interactive, web-based
- Jupyter Notebook: Technical, reproducible

Visualizations:
- PNG/SVG: High-resolution charts
- Interactive dashboard: Web-based
- PowerPoint: Presentation format

Data:
- CSV/Excel: Cleaned datasets
- Database: Structured storage
- JSON: API-friendly format

Code:
- Python scripts: Automation
- Jupyter notebooks: Analysis documentation
- Git repository: Version control

Ready for data analysis! 📊
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "capabilities": ["Statistical", "Visualization", "Quality", "Predictive", "Correlation"],
                "tools": self.tools,
                "python_stack": ["pandas", "numpy", "scipy", "matplotlib", "seaborn", "sklearn"],
                "collaboration": ["Sofia", "Marcus", "Elena", "Alex", "Lucas"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["data_analysis_overview.pdf"],
            next_steps="Specify analysis type and provide data"
        )


# Quick test
if __name__ == "__main__":
    print("📊 Maya Patel - Data Analyst\n")
    
    agent = MayaAgent()
    
    print(f"Agent: {agent.name}")
    print(f"Role: {agent.role}")
    print(f"Specialization: {agent.specialization}")
    
    print(f"\nTools Available:")
    for category, tools in agent.tools.items():
        if category not in ["status", "python_stack"]:
            print(f"  {category}: {len(tools)} tools")
    
    print(f"\n{agent.tools.get('status', 'Ready!')}")
