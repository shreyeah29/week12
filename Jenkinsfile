pipeline {
    agent any
   
    stages {

        stage('Run Selenium Tests with pytest') {
            steps {
                echo "Running Selenium Tests using pytest"

                // Install Python dependencies
                sh 'pip install -r requirements.txt'

                // Start Flask app in background
                sh 'start /B python app.py'

                // Wait for the app to start
                sh 'ping 127.0.0.1 -n 5 > nul'

                // Run pytest
                sh 'pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image"
                sh "docker build -t seleniumdemoapp:v1 ."
            }
        }

        stage('Docker Login') {
            steps {
                echo "Logging into Docker Hub"
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Pushing Docker Image to Docker Hub"
                sh "docker tag seleniumdemoapp:v1 shreyeah29/week7-myapp:tagname:seleniumtest"
                sh "docker push shreyeah29/week7-myapp:seleniumtest"
            }
        }

        stage('Deploy to Kubernetes') { 
            steps { 
                echo "Deploying to Kubernetes"
                sh 'kubectl apply -f deployment.yaml --validate=false' 
                sh 'kubectl apply -f service.yaml' 
            } 
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}