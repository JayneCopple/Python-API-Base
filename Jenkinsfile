pipeline {
    agent any
    environment {
        GCR_CREDENTIALS_ID = 'jayne-srv-storage-admin'
        IMAGE_NAME = 'jayne-python-api'
        GCR_URL = 'eu.gcr.io/lbg-mea-17'
        }
    stages {
        stage('Build and Deploy stage') {
            steps {
                script {
                // Authenticate with Google Cloud
                withCredentials([file(credentialsId: GCR_CREDENTIALS_ID, variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                sh 'gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS'
                }

                // Configure Docker to use gcloud as a credential helper
                sh 'gcloud auth configure-docker --quiet'

                // Build the Docker image
                sh "docker build -t ${GCR_URL}/${IMAGE_NAME}:${BUILD_NUMBER} ."
           }
        }
        stage('Push') {
            steps {
                // Push the Docker image to GCR
                sh "docker push ${GCR_URL}/${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }
    }
    post {
        always {
                sh '''
                
                '''
        }
    }
}
}
