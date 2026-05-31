class EC2Deploy:
    def launch(self):
        cmd = "aws ec2 run-instances --image-id ami-xxxxx --instance-type t2.micro"
        return cmd
    
    def setup(self):
        return ["sudo yum install python3", "pip install -r requirements.txt"]
    
    def run(self):
        return "python -m uvicorn main:app"

if __name__ == "__main__":
    deploy = EC2Deploy()
    print(deploy.launch())
