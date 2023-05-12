from airflow import DAG
from airflow.models.variable import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonVirtualenvOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "soda_core",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

PROJECT_ROOT = "<this_project_full_path_root>"


def run_soda_scan(project_root, scan_name, checks_subpath = None):
    from soda.scan import Scan

    print("Running Soda Scan ...")
    config_file = f"{project_root}/soda/configuration.yml"
    checks_path = f"{project_root}/soda/checks"

    if checks_subpath:
        checks_path += f"/{checks_subpath}"

    data_source = "soda_demo"

    scan = Scan()
    scan.set_verbose()
    scan.add_configuration_yaml_file(config_file)
    scan.set_data_source_name(data_source)
    scan.add_sodacl_yaml_files(checks_path)
    scan.set_scan_definition_name(scan_name)

    result = scan.execute()
    print(scan.get_logs_text())

    if result != 0:
        raise ValueError('Soda Scan failed')

    return result


with DAG(
    "model_adventureworks_sales_category",
    default_args=default_args,
    description="A simple Soda Core scan DAG",
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
):
    ingest_raw_data = DummyOperator(task_id="ingest_raw_data")

    checks_ingest = PythonVirtualenvOperator(
        task_id="checks_ingest",
        python_callable=run_soda_scan,
        requirements=["soda-core-postgres", "soda-core-scientific"],
        system_site_packages=False,
        op_kwargs={
            "project_root": PROJECT_ROOT,
            "scan_name": "model_adventureworks_sales_category_ingest",
            "checks_subpath": "ingest/dim_product_category.yml"
        },
    )

    dbt_transform = BashOperator(
        task_id="dbt_transform",
        bash_command=f"dbt run --project-dir {PROJECT_ROOT}/dbt --select transform",
    )

    checks_transform = PythonVirtualenvOperator(
        task_id="checks_transform",
        python_callable=run_soda_scan,
        requirements=["soda-core-postgres", "soda-core-scientific"],
        system_site_packages=False,
        op_kwargs={
            "project_root": PROJECT_ROOT,
            "scan_name": "model_adventureworks_sales_category_transform",
            "checks_subpath": "transform"
        },
    )

    dbt_report = BashOperator(
        task_id="dbt_report",
        bash_command=f"dbt run --project-dir {PROJECT_ROOT}/dbt --select report",
    )

    checks_report = PythonVirtualenvOperator(
        task_id="checks_report",
        python_callable=run_soda_scan,
        requirements=["soda-core-postgres", "soda-core-scientific"],
        system_site_packages=False,
        op_kwargs={
            "project_root": PROJECT_ROOT,
            "scan_name": "model_adventureworks_sales_category_report",
            "checks_subpath": "report"
        },
    )

    publish_data = DummyOperator(task_id="publish_data")

    ingest_raw_data >> checks_ingest >> dbt_transform >> checks_transform >> dbt_report >> checks_report >> publish_data
