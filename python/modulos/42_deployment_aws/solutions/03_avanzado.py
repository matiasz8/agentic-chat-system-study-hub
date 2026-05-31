class TerraformDeploy:
    def config(self):
        return """
        resource "aws_ecs_cluster" "main" {
            name = "ask-sage-cluster"
        }
        resource "aws_ecs_service" "main" {
            desired_count = 3
        }
        """
    
    def steps(self):
        return ["terraform init", "terraform plan", "terraform apply"]

if __name__ == "__main__":
    deploy = TerraformDeploy()
    print(deploy.config())
