from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import docker
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def deploy_container(request):
    docker_image = request.data.get('docker_image')
    ports = request.data.get('ports')

    logger.info(f"Received request to deploy container with image {docker_image} and ports {ports}")

    if not docker_image or not ports:
        return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        client.images.pull(docker_image)
        port_bindings = {int(port): int(port) for port in ports}
        container = client.containers.run(
            docker_image,
            detach=True,
            ports=port_bindings
        )

        logger.info(f"Container {container.id} deployed successfully")

        return Response({"message": "Container deployed successfully", "container_id": container.id}, status=status.HTTP_200_OK)
    except docker.errors.DockerException as e:
        logger.error(f"Error deploying container: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_container_logs(request, container_id):
    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        container = client.containers.get(container_id)
        logs = container.logs().decode('utf-8')
        
        logger.info(f"Retrieved logs for container {container_id}")
        
        return Response({"logs": logs}, status=status.HTTP_200_OK)
    except docker.errors.DockerException as e:
        logger.error(f"Error retrieving logs for container {container_id}: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    