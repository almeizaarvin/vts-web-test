FROM jenkins/jenkins:lts-jdk17

USER root

# Install docker client + docker-compose plugin
RUN apt-get update \
    && apt-get install -y docker.io docker-compose-plugin \
    && usermod -aG docker jenkins

# Allow access to /var/run/docker.sock
RUN chmod 666 /var/run/docker.sock || true

USER jenkins
