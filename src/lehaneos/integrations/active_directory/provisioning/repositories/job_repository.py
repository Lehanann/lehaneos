from pathlib import Path
from lehaneos.integrations.active_directory.provisioning.repositories.yaml_repository import (
    YamlRepository,
)
from lehaneos.integrations.active_directory.provisioning.schemas.job import Job

class JobRepository(YamlRepository):
    """
    Repository responsible for accessing job configuration data.
    """

    PATH_FILE = Path(__file__).parent.parent / "config" / "job.yaml"

    def get_job(self, job_name: str) -> Job | None:
        """
        Retrieve a job definition by its identifier.

        Args:
            job_name: Job identifier defined in the job configuration file.

        Returns:
            The matching Job instance if found, otherwise None.
        """
        data = self._load()
        if data is None:
            return None

        job = data["jobs"].get(job_name)

        if job is None:
            return None

        return Job.model_validate(job)

    def list_jobs(self) -> list[Job]:
        """
        Retrieve all jobs defined in the job configuration file.

        Returns:
            A list containing all configured jobs.
            Returns an empty list if the configuration loaded.
        """
        data = self._load()

        if data is None:
            return []

        return [Job.model_validate(job) for job in data["jobs"].values()]

    def list_jobs_with_key(self) -> dict[str, Job]:
        data = self._load()

        if data is None:
            return {}

        return {
            key: Job.model_validate(job)
            for key, job in data["jobs"].items()
        }
