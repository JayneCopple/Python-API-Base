pipeline {
    agent any
    environment {
        //GCR_CREDENTIALS_ID = 'jayne-srv-storage-admin@lbg-mea-17.iam.gserviceaccount.com'
        GCR_CREDENTIALS_ID = 'jayne-srv-storage-admin'
        IMAGE_NAME = 'jayne-python-api'
        BUILD_VERSION = 'v2'
        GCR_URL = 'eu.gcr.io/lbg-mea-17'
        PROJECT_ID = 'lbg-mea-17'
        CLUSTER_NAME = 'jayne-kube-cluster'
        LOCATION = 'europe-west2-c'
        //CREDENTIALS_ID = 'jayne-jenkins-k8s-srv@lbg-mea-17.iam.gserviceaccount.com'
        CREDENTIALS_ID = 'jayne-jenkins-k8s-srv'
        }
    stages {
        stage('Build') {
            steps {
                script {
                // Authenticate with Google Cloud
                withCredentials([file(credentialsId: /$GCR_CREDENTIALS_ID, variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    echo $GCR_CREDENTIALS_ID
                    echo $GOOGLE_APPLICATION_CREDENTIALS
                sh 'gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS'
                }

                // Configure Docker to use gcloud as a credential helper
                sh 'gcloud auth configure-docker --quiet'

                // Build the Docker image
                sh "docker build -t ${GCR_URL}/${IMAGE_NAME}:${BUILD_VERSION} ."
                }
            }
        }
        stage('Push') {
            steps {
                // Push the Docker image to GCR
                sh "docker push ${GCR_URL}/${IMAGE_NAME}:${BUILD_VERSION}"
            }
        }
        stage('Deploy to GKE cluster') {
            steps {
                 script {
                 // Deploy to GKE using Jenkins Kubernetes Engine Plugin

                    step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'kubernetes/deployment.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])   
                 }
            }
        }

    }
    post {
        always {
                sh '''
                echo "done"
                '''
        }
    }
}