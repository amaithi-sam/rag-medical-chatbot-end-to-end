# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# 1. Install prerequisites
# We install lsb-release to dynamically get the OS codename (e.g., bookworm/bullseye)
RUN apt-get update -y && \
    apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 2. Add Docker's official GPG key (Modern Method)
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 3. Set up the repository dynamically
# This automatically detects your CPU architecture (amd64 vs arm64) and OS version
RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Install Docker Engine and CLI
RUN apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# 5. Add Jenkins user to the Docker group
RUN usermod -aG docker jenkins

# Switch back to the Jenkins user
USER jenkins