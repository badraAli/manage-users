pipeline {
    agent any

    parameters {
        choice(name: 'VERSION', choices: ['1.0', '1.1', '1.2', '1.3', '1.4', '1.5'], description: 'Select the version of the application to deploy')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests after build?')
    }
   
    stages {
        stage('Build') {
            steps {
                echo "Building the applicatoion version ${VERSION} ....."
                sh "python3 -m venv venv"
                sh ". venv/bin/activate && pip install -r requirements.txt"
            }
        }

        stage('Test') {
            when {
                expression {
                    params.RUN_TESTS == true
                }
            } 
            steps {
                echo "Testing the application ....."
                sh ". venv/bin/activate && pytest tests/"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building the docker image ....."
                sh "docker buildx build --provenance false -t manage-users-image:${VERSION} . --load"
            }
        }

        stage('Deploy Docker Image to AWS ECR') {
            steps {

                echo "Logging into AWS ECR ....."
                sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 891377325592.dkr.ecr.us-east-1.amazonaws.com"

                echo "Tagging the docker image ....."
                sh "docker tag manage-users-image:${VERSION} 891377325592.dkr.ecr.us-east-1.amazonaws.com/manage-users-image:${VERSION}"

                echo "Pushing the docker image to AWS ECR ....."
                sh "docker push 891377325592.dkr.ecr.us-east-1.amazonaws.com/manage-users-image:${VERSION}"
            }
        }
    }
    post {
        success {
            echo "This will run only if the pipeline is successful"
        }
        failure {
            echo "This will run only if the pipeline is failed " 
        }
    }
}
