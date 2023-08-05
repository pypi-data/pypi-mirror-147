from typing import Optional, Any, Callable, Dict, cast, List, Tuple
from typing_extensions import Protocol

from phidata.task import Task, TaskArgs
from phidata.utils.cli_console import print_info
from phidata.utils.log import logger


PythonTaskType = Callable[..., bool]


class PythonTaskArgs(TaskArgs):
    # To run a task we need to execute a function.
    # This python function is called the entrypoint
    # For example:
    #     def simple_python_function(**kwargs) -> bool:
    # The entrypoint() should accept **kwargs as the parameters
    # and return the run_status: True/False as a bool
    # The type for the entrypoint_function is Callable[..., bool].
    #   The entrypoint_function takes any number of/type of arguments
    #   as key=value pairs and returns True/False
    # https://stackoverflow.com/a/39624147
    # https://docs.python.org/3/library/typing.html#typing.Callable
    entrypoint: PythonTaskType
    # If True, scans the args/kwargs for SqlTable objects and populates the
    # SqlTable.db_engine value using the SqlTable.db_conn_id
    create_db_engine_from_conn_id: bool = False

    # Used for internal operations
    entrypoint_args: Optional[Tuple[Any, ...]] = None
    entrypoint_kwargs: Optional[Dict] = None


class PythonTask(Task):
    """A PythonTask executes a python function"""

    def __init__(
        self,
        name: Optional[str] = None,
        entrypoint: Optional[Callable[..., bool]] = None,
        task_id: Optional[str] = None,
        dag_id: Optional[str] = None,
        create_db_engine_from_conn_id: bool = False,
        entrypoint_args: Optional[Tuple[Any, ...]] = None,
        entrypoint_kwargs: Optional[Dict] = None,
        version: Optional[str] = None,
        enabled: bool = True,
    ) -> None:
        super().__init__()
        self.args: Optional[PythonTaskArgs] = None
        if name is not None and entrypoint is not None:
            try:
                self.args = PythonTaskArgs(
                    name=name,
                    entrypoint=entrypoint,
                    task_id=task_id,
                    dag_id=dag_id,
                    create_db_engine_from_conn_id=create_db_engine_from_conn_id,
                    entrypoint_args=entrypoint_args,
                    entrypoint_kwargs=entrypoint_kwargs,
                    version=version,
                    enabled=enabled,
                )
            except Exception as e:
                logger.error(f"Args for {self.__class__.__name__} are not valid")
                raise

    @property
    def entrypoint(self) -> Optional[Callable[..., bool]]:
        return self.args.entrypoint if self.args else None

    ######################################################
    ## Run PythonTask
    ######################################################

    def run_in_local_env(self) -> bool:
        """
        Runs a PythonTask in the local environment where phi wf is called from.

        Returns:
            run_status (bool): True if the run was successful
        """
        # PythonTask not yet initialized
        if self.args is None:
            logger.error("PythonTask not initialized")
            return False

        # Important: Validate that PathContext is available
        # This is passed down by the workflow
        if self.path_context is None:
            logger.error("PathContext not available")
            return False

        dry_run: bool = self.run_context.dry_run if self.run_context else False
        if dry_run:
            logger.info("Dry run, returning True")
            return True

        run_status: bool = False
        entrypoint = self.entrypoint
        try:
            if self.args is not None and entrypoint is not None:
                run_status = entrypoint(**self.args.dict())
        except Exception as e:
            logger.error("Could not run PythonTask")
            logger.error(e)
        return run_status

    def run_in_docker_container(
        self, active_container: Any, docker_env: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Runs a PythonTask in a docker container.

        Args:
            active_container: The container to run the workflow in
            docker_env:

        Returns:
            run_status (bool): True if the run was successful

        Notes:
            * This function runs in the local environment where phi wf is called from.
            But executes an `airflow` commands in the docker container to run the workflow
            * For the airflow tasks to be available, they need to be added to the workflow DAG
            using add_airflow_tasks_to_dag()
        """
        # PythonTask not yet initialized
        if self.args is None:
            logger.error("PythonTask not initialized")
            return False

        from pathlib import Path

        from docker.errors import APIError
        from docker.models.containers import Container

        from phidata.infra.docker.utils.container import execute_command

        if active_container is None or not isinstance(active_container, Container):
            logger.error("Invalid Container object")
            return False
        container: Container = active_container

        task_id = self.task_id
        dag_id = self.dag_id
        if task_id is None:
            logger.error("task_id unavailable")
            return False
        if dag_id is None:
            logger.error("dag_id unavailable")
            return False

        run_date: str = self.args.run_date
        dry_run: bool = self.run_context.dry_run if self.run_context else False
        airflow_cmd_dry_run_str: str = " -n" if dry_run else ""

        workflow_file_path: Optional[Path] = (
            self.path_context.workflow_file if self.path_context else None
        )
        airflow_cmd_subdir_str: str = (
            f" -S {str(workflow_file_path.parent)}" if workflow_file_path else ""
        )

        # logger.debug("task_id: {}".format(task_id))
        # logger.debug("dag_id: {}".format(dag_id))
        # logger.debug("run_date: {}".format(run_date))
        # logger.debug("dry_run: {}".format(dry_run))

        run_status: bool = False

        test_wf_cmd = f"airflow tasks test {dag_id} {task_id} {run_date}{airflow_cmd_subdir_str}{airflow_cmd_dry_run_str}"
        dry_run_cmd = f"python {workflow_file_path}"
        command_to_run = dry_run_cmd if dry_run else test_wf_cmd
        try:
            print_info(
                "Running command: {}\nContainer: {}".format(
                    command_to_run, container.name
                )
            )
            run_status = execute_command(
                cmd=command_to_run,
                container=container,
                docker_env=docker_env,
            )
        except APIError as e:
            logger.exception(e)
            raise

        return run_status

    def run_in_k8s_container(
        self,
        pod: Any,
        k8s_api_client: Any,
        container_name: Optional[str] = None,
        k8s_env: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Runs a PythonTask in a k8s container.

        Args:
            pod: The pod to run the workflow in
            k8s_api_client: K8sApiClient
            container_name: The container to run the workflow in
            k8s_env:

        Returns:
            run_status (bool): True if the run was successful

        Notes:
            * This function runs in the local environment where phi wf is called from.
            But executes an `airflow` commands in the k8s container to run the workflow
            * For the airflow tasks to be available, they need to be added to the workflow DAG
            using add_airflow_tasks_to_dag()
        """
        # PythonTask not yet initialized
        if self.args is None:
            logger.error("PythonTask not initialized")
            return False

        from pathlib import Path

        from phidata.infra.k8s.resource.core.v1.pod import Pod
        from phidata.infra.k8s.api_client import K8sApiClient

        from phidata.infra.k8s.utils.pod import execute_command

        if pod is None or not isinstance(pod, Pod):
            logger.error("Invalid Pod")
            return False
        if k8s_api_client is None or not isinstance(k8s_api_client, K8sApiClient):
            logger.error("Invalid K8sApiClient")
            return False

        task_id = self.task_id
        dag_id = self.dag_id
        if task_id is None:
            logger.error("task_id unavailable")
            return False
        if dag_id is None:
            logger.error("dag_id unavailable")
            return False

        run_date: str = self.args.run_date
        dry_run: Optional[bool] = self.run_context.dry_run if self.run_context else None
        airflow_cmd_dry_run_str: str = " -n" if dry_run else ""

        workflow_file_path: Optional[Path] = (
            self.path_context.workflow_file if self.path_context else None
        )
        airflow_cmd_subdir_str: str = (
            f"-S {str(workflow_file_path.parent)}" if workflow_file_path else ""
        )

        # logger.debug("task_id: {}".format(task_id))
        # logger.debug("dag_id: {}".format(dag_id))
        # logger.debug("run_date: {}".format(run_date))
        # logger.debug("dry_run: {}".format(dry_run))

        run_status: bool = False

        test_wf_cmd = ["airflow", "tasks", "test", dag_id, task_id, run_date]
        dry_run_cmd = ["python", workflow_file_path]
        command_to_run = dry_run_cmd if dry_run else test_wf_cmd
        try:
            print_info("Running command: {}\nContainer: {}".format(command_to_run, pod))
            run_status = execute_command(
                cmd=test_wf_cmd,
                pod=pod,
                k8s_api_client=k8s_api_client,
                container_name=container_name,
                k8s_env=k8s_env,
            )
        except Exception as e:
            logger.error(e)
            raise

        return run_status

    ######################################################
    ## Airflow functions
    ######################################################

    def add_airflow_task(self, dag: Any) -> Any:
        """
        This function adds the PythonTask to a dag.
        Args:
            dag:

        Returns:
            PythonOperator
        """
        # PythonTask not yet initialized
        # logger.info(f"args: {self.args}")
        # logger.info(f"dag: {dag}")
        if self.args is None:
            return False

        # Important: Validate that PathContext is available
        # logger.info(f"path_context: {self.path_context}")
        if self.path_context is None:
            return False

        from airflow.models.dag import DAG
        from airflow.operators.python import PythonOperator

        if dag is None or not isinstance(dag, DAG):
            logger.error("Invalid DAG")
            return False

        # Get the task_id for the airflow task
        task_id = self.task_id
        logger.info(f"Creating airflow task: {task_id}")

        # Create db_engines if selected
        if self.args.create_db_engine_from_conn_id:
            self.create_db_engines()

        # Function to run
        entrypoint = (
            self.args.entrypoint
            if self.args and self.args.entrypoint is not None
            else simple_python_function
        )
        entrypoint = cast(PythonTaskType, entrypoint)
        # Airflow task
        airflow_task = PythonOperator(
            task_id=task_id,
            dag=dag,
            python_callable=entrypoint,
            op_kwargs=self.args.dict(),
        )
        logger.debug(f"Airflow task created: {task_id}")
        return airflow_task

    def create_db_engines(self):
        if self.args is None:
            return False

        from phidata.asset.table.sql import SqlTable, SqlType

        def create_db_engine_using_conn_id(t: SqlTable):
            # logger.info(f"Creating DbEngine for: {t.name}")
            if t.sql_type == SqlType.POSTGRES:
                from airflow.providers.postgres.hooks.postgres import PostgresHook

                pg_hook = PostgresHook(postgres_conn_id=t.db_conn_id)
                t.db_engine = pg_hook.get_sqlalchemy_engine()

        logger.debug("Creating DbEngines for SqlTables")
        # logger.info(f"args: {self.args}")
        for field_key, field_value in self.args.__dict__.items():
            if isinstance(field_value, SqlTable):
                create_db_engine_using_conn_id(field_value)

        if self.args.entrypoint_kwargs is not None and isinstance(
            self.args.entrypoint_kwargs, dict
        ):
            for kwargs_key, kwargs_value in self.args.entrypoint_kwargs.items():
                if isinstance(kwargs_value, SqlTable):
                    create_db_engine_using_conn_id(kwargs_value)


def simple_python_function(**kwargs) -> bool:
    logger.error("Invalid entrypoint function")
    logger.error("KWargs: {}".format(kwargs))
    return True


class PythonTaskDecoratorType(Protocol):
    def __call__(
        self,
        *args,
        name: Optional[str] = None,
        task_id: Optional[str] = None,
        dag_id: Optional[str] = None,
        create_db_engine_from_conn_id: bool = True,
        version: Optional[str] = None,
        enabled: bool = True,
        **kwargs,
    ) -> PythonTask:
        ...
