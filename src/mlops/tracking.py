import mlflow
import os

MLFLOW_TRACKING_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "mlruns")

def init_mlflow(experiment_name="research_platform_eval"):
    db_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "mlflow.db"))
    mlflow.set_tracking_uri(f"sqlite:///{db_path}")
    mlflow.set_experiment(experiment_name)

def log_question_run(question_index, metrics_dict):
    with mlflow.start_run(run_name=f"question_{question_index}", nested=True):
        mlflow.log_param("question", metrics_dict.get("question", ""))
        for key, value in metrics_dict.items():
            if key != "question" and isinstance(value, (int, float)):
                mlflow.log_metric(key, value)

def log_summary(avg_recall, avg_faithfulness, success_rate, model_name, results_file_path):
    mlflow.log_param("model_name", model_name)
    mlflow.log_metric("avg_recall_at_5", avg_recall)
    mlflow.log_metric("avg_faithfulness", avg_faithfulness)
    mlflow.log_metric("success_rate", success_rate)
    mlflow.log_artifact(results_file_path)

