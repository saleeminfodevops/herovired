# 1. Download and extract the latest eksctl binary to the /tmp directory
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

# 2. Move the binary to /usr/local/bin so the system can locate the command
sudo mv /tmp/eksctl /usr/local/bin

# 3. Verify the installation
eksctl version
