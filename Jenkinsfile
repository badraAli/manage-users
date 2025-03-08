pipeline {
    agent any

   
    stages {

        stage('Build') {
            steps {
                echo "Building the applicatoion version ${NEW_VERSION} ....."
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo "Testing the application ....."
                sh '. venv/bin/activate && pytest tests/'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building the docker image ....."
                sh 'docker build -t manage-users-image:1.0 .'
            }
        }

        stage('Deploy Docker Image to AWS ECR') {
            steps {
                echo "Coniguring AWS CLI ....."
                sh 'aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"'
                sh 'aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"'

                echo "Logging into AWS ECR ....."
                sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 891377325592.dkr.ecr.us-east-1.amazonaws.com'

                echo "Tagging the docker image ....."
                sh 'docker tag manage-users-image:1.0 891377325592.dkr.ecr.us-east-1.amazonaws.com/manage-users-image:1.0'

                echo "Pushing the docker image to AWS ECR ....."
                sh 'docker push 891377325592.dkr.ecr.us-east-1.amazonaws.com/manage-users-image:1.0'
            }
        }
    }
    post {
        always {
            echo "This will always run"
        }
        success {
            echo "This will run only if the pipeline is successful"
        }
        failure {
            echo "This will run only if the pipeline is failed " 
        }
    }
}
