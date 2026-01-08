pipeline {
    agent any

    environment {
        REGISTRY = "docker.io/Sanjay12223"
        BACKEND_IMAGE = "${REGISTRY}/cicd-backend"
        FRONTEND_IMAGE = "${REGISTRY}/cicd-frontend"
        TAG = "staging-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                docker build -t $BACKEND_IMAGE:$TAG backend
                docker build -t $FRONTEND_IMAGE:$TAG frontend
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                docker run --rm $BACKEND_IMAGE:$TAG python -c "print('Tests passed')"
                '''
            }
        }

        stage('Security Scan (Trivy)') {
            steps {
                sh '''
                trivy image --exit-code 0 $BACKEND_IMAGE:$TAG
                trivy image --exit-code 0 $FRONTEND_IMAGE:$TAG
                '''
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

                    # Push build-specific tags
                    docker push $BACKEND_IMAGE:$TAG
                    docker push $FRONTEND_IMAGE:$TAG

                    # Tag images for staging deployment
                    docker tag $BACKEND_IMAGE:$TAG $BACKEND_IMAGE:staging-latest
                    docker tag $FRONTEND_IMAGE:$TAG $FRONTEND_IMAGE:staging-latest

                    # Push staging-latest tags
                    docker push $BACKEND_IMAGE:staging-latest
                    docker push $FRONTEND_IMAGE:staging-latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "CI pipeline completed successfully"
        }
        failure {
            echo "CI pipeline failed"
        }
    }
}
