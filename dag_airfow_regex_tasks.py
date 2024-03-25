import os
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
from docker.types import Mount  # Импортируем необходимый класс


project_dir = os.getenv('AIRFLOW_REGEX_TASKS_DIR', '/home/sergio/Code/github_projects/airflow')

# Путь к директории для вывода данных
host_data_dir = os.path.join(project_dir, 'output_data')

default_args = {
    'owner': 'sergio',
    'start_date': datetime(2023, 1, 1),
}

dag = DAG(
    'airflow_regex_tasks',
    default_args=default_args,
    description='Run Python scripts in Docker containers',
    schedule_interval=None,
)

def create_docker_task(task_id, script_name):
    # Создаем определение тома с использованием класса Mount
    volume_mapping = Mount(source=host_data_dir, target='/app/output_data', type='bind')
    return DockerOperator(
        task_id=task_id,
        image='sergeipanov01/airflow_regex_tasks:mar19',
        command=f'python /app/{script_name}',
        auto_remove=True,
        mounts=[volume_mapping],
        user=f"{os.getuid()}:{os.getgid()}",
        dag=dag,
    )

# Инициализация задач
filter_ct_prefix = create_docker_task('filter_ct_prefix', '01_filter_ct_prefix.py')
extract_numeric_serials = create_docker_task('extract_numeric_serials', '02_extract_numeric_serials.py')
combine_serials_position = create_docker_task('combine_serials_position', '03_combined_serials_pos.py')
match_serials = create_docker_task('match_serials', '04_matched_serials.py')

# Устанавливаем последовательность выполнения задач
filter_ct_prefix >> extract_numeric_serials >> combine_serials_position >> match_serials