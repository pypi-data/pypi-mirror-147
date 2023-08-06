from setuptools import setup, find_packages

setup(
    name="airflow-census",
    license="MIT",
    version="0.0.0",
    description="""
    This project is created to provide a simple way to
    ingest data from the Census API.
    https://files.consumerfinance.gov/ccdb/complaints.csv.zip

    Project provide prebuilt airflow DAG pipleine designed using TFX.
    
    how to use this library

    ```
    from census_consumer_complaint_orchestrator.airflow_orchestrator import get_airflow_dag_pipeline
    dag = get_airflow_dag_pipeline()
    ```


    """,
    author="Avnish Yadav",
    packages=find_packages(),
    install_requires=['tfx==1.6.1', 'apache-beam[interactive]', 'apache-airflow']
)
