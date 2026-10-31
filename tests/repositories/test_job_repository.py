from lehaneos.integrations.active_directory.provisioning.repositories.job_repository import JobRepository

def test_get_job():
    job_repo = JobRepository()

    job = job_repo.get_job("system_administrator")

    assert job is not None
    assert job.title == "Administrateur systèmes"
    assert job.organization_unit =="admins"
    assert "GRP_ADM_LEHANEOS" in job.groups
    assert "GRP_DEPT_IT" in job.groups


