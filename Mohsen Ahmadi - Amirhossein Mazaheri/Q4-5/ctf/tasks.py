import docker
from celery import shared_task
from .models import Team, Challenge, ActiveContainer, ChallengeHistory
from django.utils import timezone

client = docker.from_env()


@shared_task
def start_challenge_container(team_id, challenge_id):
    team = Team.objects.get(id=team_id)
    challenge = Challenge.objects.get(id=challenge_id)

    existing = ActiveContainer.objects.filter(team=team, challenge=challenge).first()
    if existing:
        return {
            "message": "Container already running",
            "container_id": existing.container_id,
            "url": existing.access_url
        }

    container = client.containers.run(
        image=challenge.docker_image,
        detach=True,
        ports={f"{challenge.internal_port}/tcp": None}
    )
    container.reload()
    host_port = container.attrs['NetworkSettings']['Ports'][f"{challenge.internal_port}/tcp"][0]['HostPort']
    url = f"http://localhost:{host_port}"

    ActiveContainer.objects.create(
        team=team,
        challenge=challenge,
        container_id=container.id,
        host_port=host_port,
        access_url=url
    )

    ChallengeHistory.objects.create(
        team=team,
        challenge=challenge,
        container_id=container.id,
        started_at=timezone.now(),
        stopped_at=None
    )

    return {"container_id": container.id, "url": url}

@shared_task
def stop_challenge_container(team_id, challenge_id):
    active = ActiveContainer.objects.get(team_id=team_id, challenge_id=challenge_id)
    container = client.containers.get(active.container_id)
    container.stop()
    container.remove()

    history = ChallengeHistory.objects.get(container_id=active.container_id)
    history.stopped_at = timezone.now()
    history.save()

    active.delete()
    return {"status": "stopped"}
