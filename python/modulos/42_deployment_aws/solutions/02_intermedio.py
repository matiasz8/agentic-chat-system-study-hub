class DockerDeploy:
    def build(self):
        return "docker build -t ask-sage:latest ."
    
    def push(self, registry):
        return f"docker push {registry}/ask-sage:latest"
    
    def steps(self):
        return [self.build(), "docker login ...", self.push("ecr-registry")]

if __name__ == "__main__":
    deploy = DockerDeploy()
    for step in deploy.steps():
        print(step)
