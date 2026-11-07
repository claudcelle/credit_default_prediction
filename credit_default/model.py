"""Importable preprocessing and the selected XGBoost configuration."""

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder
from xgboost import XGBClassifier

RANDOM_STATE = 42
TEST_SIZE = 0.2
TARGET = "default_payment_next_month"
DECISION_THRESHOLD = 0.5

CATEGORICAL_COLUMNS = ["sex", "education", "marriage"]
REPAYMENT_COLUMNS = ["pay_0", "pay_2", "pay_3", "pay_4", "pay_5", "pay_6"]
NUMERICAL_COLUMNS = [
    "limit_bal", "age",
    *[f"bill_amt{i}" for i in range(1, 7)],
    *[f"pay_amt{i}" for i in range(1, 7)],
] + REPAYMENT_COLUMNS


def group_education_codes(X):
    """Preserve the original input while grouping undocumented education codes."""
    X = X.copy()
    X["education"] = X["education"].replace({5: 0, 6: 0})
    return X


def build_final_pipeline():
    """Return an unfitted copy of the configuration selected in training.ipynb."""
    preprocessing = ColumnTransformer([
        ("categorical", OneHotEncoder(
            handle_unknown="ignore", sparse_output=False,
        ), CATEGORICAL_COLUMNS),
        ("numerical", "passthrough", NUMERICAL_COLUMNS),
    ], remainder="drop")

    return Pipeline([
        ("education_recoding", FunctionTransformer(
            group_education_codes, feature_names_out="one-to-one",
        )),
        ("preprocessing", preprocessing),
        ("model", XGBClassifier(
            objective="binary:logistic",
            eval_metric="auc",
            tree_method="hist",
            n_estimators=100,
            max_depth=6,
            learning_rate=0.05,
            min_child_weight=5,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=RANDOM_STATE,
            n_jobs=2,
        )),
    ])
