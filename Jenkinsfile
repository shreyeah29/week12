pipeline {
    agent any

    stages {

        stage('Run Selenium Tests with pytest') {
            steps {
                echo "🐍 Running Selenium Tests using pytest"

                // Create a virtual environment safely
                sh '''
                    apt-get update -y
                    apt-get install -y python3 python3-venv python3-pip
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --break-system-packages -r requirements.txt
                    python app.py &
                    sleep 5
                    pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker Image"
                sh 'docker build -t seleniumdemoapp:v1 .'
            }
        }

        stage('Docker Login') {
            steps {
                echo "🔑 Logging into Docker Hub"
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "⬆️ Pushing Docker Image to Docker Hub"
                sh '''
                    docker tag seleniumdemoapp:v1 shreyeah29/week7-myapp:seleniumtest
                    docker push shreyeah29/week7-myapp:seleniumtest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "🚀 Deploying to Kubernetes"
                sh '''
                    kubectl apply -f deployment.yaml --validate=false
                    kubectl apply -f service.yaml
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check the logs.'
        }
    }
}
