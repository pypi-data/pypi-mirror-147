from typing import NamedTuple, Optional

from kfp.v2 import dsl
from kfp.v2.dsl import Artifact, Input, Metrics, Model, Output


@dsl.component(base_image="python:3.8-slim")
def AddServingConfigOp(
    model: Input[Model],
    configured_model: Output[Artifact],
    serving_config: dict,
):
    """
    Adds a serving configuration to a Model artifact.

    Args:
        model: the Model artifact to prepare for deployment
        configured_model: the output artifact handle for the configured model
        serving_config: the serving configuration to apply to the Model artifact
    """
    from copy import copy

    configured_model.uri = model.uri
    configured_model.metadata = copy(model.metadata)
    configured_model.metadata.update(serving_config)


@dsl.component(base_image="python:3.8-slim")
def AddModelToTritonRepoOp(
    model_artifact: Input[Model],
    model_config: Input[Artifact],
    model: Output[Model],
    model_repo: str,
    model_name: str,
    model_version: int,
    model_subdir: str = "",
):
    """
    Adds a model artifact to a triton model registry.

    Args:
        model_artifact: the model artifact to move to the triton model repository
        model_config: the triton config for the model
        model: the output artifact handle for the model in the triton repository
        model_repo: gcs path to the root of the target model repository
        model_name: the model name for the model artifact
        model_version: the version under which to save the model
        model_subdir: optional sub-directory of the model under the version
    """
    import shutil
    from pathlib import Path

    model_artifact_uri_fuse = model_artifact.uri.replace("gs://", "/gcs/")
    model_config_uri_fuse = model_config.uri.replace("gs://", "/gcs/")
    model_repo_fuse = model_repo.replace("gs://", "/gcs/")

    config_path = Path(model_config_uri_fuse)
    model_source = Path(model_artifact_uri_fuse)

    target_path = Path(model_repo_fuse, model_name)
    if config_path.exists():
        target_path.mkdir(parents=True, exist_ok=True)
        shutil.copy(config_path, target_path / "config.pbtxt")

    target_path = target_path / str(model_version)
    if target_path.exists():
        shutil.rmtree(target_path)

    target_path.mkdir(parents=True, exist_ok=True)
    target_path = target_path / model_subdir
    shutil.copytree(model_source, target_path, dirs_exist_ok=True)

    model.uri = model_repo
    model.metadata = model_artifact.metadata


@dsl.component(base_image="python:3.8-slim")
def UpdateWorkerPoolSpecsOp(
    worker_pool_specs: list,
    image_uri: Optional[str] = None,
    command: Optional[list] = None,
    args: Optional[dict] = None,
    hyperparams: Optional[dict] = None,
    env: Optional[dict] = None,
) -> list:
    """
    A kfp component for conveniently updating the ContainerSpecs for a list of WorkerPoolSpecs.

    Note:
        For details of WorkerPoolSpecs see Googles
        [documentation](https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec#WorkerPoolSpec).

    Args:
        worker_pool_specs: the provided list of WorkerPoolSpecs
        image_uri: imageUri to add to ContainerSpec in each WorkerPoolSpec
        command: the command to add to ContainerSpec in each WorkerPoolSpec
        args: the args to add ContainerSpec args in each WorkerPoolSpec
        hyperparams: additional args to add to ContainerSpec args in each WorkerPoolSpec
        env: environment variables to add in ContainerSpec env in each WorkerPoolSpec

    Returns:
        list of updated WorkerPoolSpecs
    """
    for spec in worker_pool_specs:
        if "container_spec" not in spec:
            spec["container_spec"] = {}

        if image_uri:
            spec["container_spec"]["image_uri"] = image_uri

        if command:
            spec["container_spec"]["command"] = command

        if args or hyperparams:
            if "args" not in spec["container_spec"]:
                spec["container_spec"]["args"] = []
            if args:
                for k, v in args.items():
                    spec["container_spec"]["args"].append(f"--{k.replace('_', '-')}={v}")
            if hyperparams:
                for k, v in hyperparams.items():
                    spec["container_spec"]["args"].append(f"--{k.replace('_', '-')}={v}")

        if env:
            if "env" not in spec["container_spec"]:
                spec["container_spec"]["env"] = []
            for k, v in env.items():
                spec["container_spec"]["env"].append(dict(name=k, value=v))

    return worker_pool_specs


@dsl.component(
    base_image="python:3.8-slim",
    packages_to_install=[
        "google-cloud-pipeline-components==0.2.6",
        "google-cloud-aiplatform==1.9.0",
    ],
)
def GetCustomJobResultsOp(
    project: str,
    location: str,
    job_resource: str,
    job_id_subdir: False,
    model: Output[Model],
    checkpoints: Output[Artifact],
    metrics: Output[Metrics],
):
    """
    A kfp component function for extracting custom training job results.

    Note:
        This component assumes that you used the `CustomTrainingJobOp` of Google Cloud's
        `google_cloud_pipeline_components` package. This outputs a job_resource, which is used
        here to extract the results of the job and output respective Artifacts.
        The `CustomTrainingJobOp` in particular requires a `base_output_directory`, to which
        all the job outputs are saved.

        The following assumptions are made of the script executed in CustomTrainingJob:

        - the trained model artifacts is saved to `base_output_directory/job_id/model/`
        - the model metadata is written to `base_output_directory/job_id/model/metadata.json`
        - the training checkpoints are saved to `base_output_directory/job_id/checkpoints/`
        - the model metrics are written to `base_output_directory/job_id/metrics/metrics.json`

    Args:
        project: the project in which the training job was run
        location: the region in which the training job was run
        job_resource: job resource output of `CustomTrainingJobOp`
        job_id_subdir: boolean flag to indicate whether outputs are written to <job_id> subdirectory
        model: the model output artifact
        checkpoints: the checkpoints artifact
        metrics: the metrics artifact
    """
    import json
    from pathlib import Path

    import google.cloud.aiplatform as aip
    from google.protobuf.json_format import Parse
    from google_cloud_pipeline_components.proto.gcp_resources_pb2 import GcpResources

    aip.init(project=project, location=location)

    training_gcp_resources = Parse(job_resource, GcpResources())
    custom_job_id = training_gcp_resources.resources[0].resource_uri
    split_idx = custom_job_id.find("project")
    custom_job_name = custom_job_id[split_idx:]
    job = aip.CustomJob.get(custom_job_name)

    job_resource = job.gca_resource
    job_base_dir = job_resource.job_spec.base_output_directory.output_uri_prefix
    if job_id_subdir:
        job_base_dir = f"{job_base_dir}/{job.name}"

    job_base_dir_fuse = Path(job_base_dir.replace("gs://", "/gcs/"))
    model_uri_fuse = job_base_dir_fuse / "model"
    checkpoints_uri_fuse = job_base_dir_fuse / "checkpoints"
    metrics_uri_fuse = job_base_dir_fuse / "metrics"

    if (model_uri_fuse / "metadata.json").exists():
        with open(model_uri_fuse / "metadata.json") as fh:
            model_metadata = json.load(fh)
        model.metadata = model_metadata

    if (metrics_uri_fuse / "metrics.json").exists():
        with open(metrics_uri_fuse / "metrics.json") as fh:
            metrics_dict = json.load(fh)

        for k, v in metrics_dict.items():
            metrics.log_metric(k, v)

    model.uri = str(model_uri_fuse).replace("/gcs/", "gs://")
    checkpoints.uri = str(checkpoints_uri_fuse).replace("/gcs/", "gs://")
    metrics.uri = str(metrics_uri_fuse).replace("/gcs/", "gs://")


@dsl.component(
    base_image="python:3.8-slim",
    packages_to_install=[
        "google-cloud-pipeline-components==0.2.6",
        "google-cloud-aiplatform==1.9.0",
    ],
)
def GetHyperparameterTuningJobResultsOp(
    project: str,
    location: str,
    job_resource: str,
    study_spec_metrics: list,
    trials: Output[Artifact],
) -> NamedTuple("outputs", [("best_params", dict)]):  # noqa: F821
    """
    Extracts the results of a Vertex AI HyperparameterTuningJob

    Args:
        project: the GCP project id in which the job was run
        location: the GCP location in which the job was run
        job_resource: the HyperparameterTuningJob resource
        study_spec_metrics: the StudySpec
        trials: the trials output artifact handle

    Returns:
        a NamedTuple containing the best parameters
    """
    import google.cloud.aiplatform as aip
    from google.cloud.aiplatform_v1.types import study
    from google.protobuf.json_format import Parse
    from google_cloud_pipeline_components.proto.gcp_resources_pb2 import GcpResources

    aip.init(project=project, location=location)

    gcp_resources_proto = Parse(job_resource, GcpResources())
    tuning_job_id = gcp_resources_proto.resources[0].resource_uri
    split_idx = tuning_job_id.find("project")
    tuning_job_name = tuning_job_id[split_idx:]

    job = aip.HyperparameterTuningJob.get(tuning_job_name)
    job_resource = job.gca_resource
    job_base_dir = f"{job_resource.trial_job_spec.base_output_directory.output_uri_prefix}/" f"{job.name}"

    trials.uri = job_base_dir

    if len(study_spec_metrics) > 1:
        raise RuntimeError("Unable to determine best parameters for multi-objective hyperparameter tuning.")

    metric = study_spec_metrics[0]["metric_id"]
    goal = study_spec_metrics[0]["goal"]
    if goal == study.StudySpec.MetricSpec.GoalType.MAXIMIZE:
        best_fn = max
        goal_name = "maximize"
    elif goal == study.StudySpec.MetricSpec.GoalType.MINIMIZE:
        best_fn = min
        goal_name = "minimize"
    best_trial = best_fn(job_resource.trials, key=lambda trial: trial.final_measurement.metrics[0].value)

    trials.metadata = dict(
        metric=metric,
        goal=goal_name,
        num_trials=len(job_resource.trials),
        best_metric_value=best_trial.final_measurement.metrics[0].value,
    )

    from collections import namedtuple

    output = namedtuple("outputs", ["best_params"])
    return output(best_params={p.parameter_id: p.value for p in best_trial.parameters})


__all__ = [
    "AddServingConfigOp",
    "AddModelToTritonRepoOp",
    "UpdateWorkerPoolSpecsOp",
    "GetCustomJobResultsOp",
    "GetHyperparameterTuningJobResultsOp",
]
