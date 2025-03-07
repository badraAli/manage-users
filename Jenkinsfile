pipeline {
    agent any

   
    stages {
        stage('Build') {
            steps {
                echo "Building the applicatoion version ${{ secrets.NEW_VERSION }} ....."
            }
        }
        stage('Test') {
            when {
                expression {
                    env.BRANCH_NAME == 'main'
                }
            }
            steps {
                echo "Testing the applicatoion ....."
            }
        }
        stage('Deploy') {
            steps {
                echo "Deploying the applicatoion ....."
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
