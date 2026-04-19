pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "devops734/ai-log-analyzer"
        DOCKER_TAG = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Code GitHub se le raha hoon...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Docker image build ho rahi hai...'
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Docker Hub pe push ho rahi hai...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}"
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('Done') {
            steps {
                echo "Build ${DOCKER_TAG} successfully pushed to Docker Hub!"
            }
        }
    }

    post {
        success {
            echo 'Pipeline successful!'
        }
        failure {
            echo 'Pipeline failed — check logs!'
        }
    }
}