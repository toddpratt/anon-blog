pipeline {
    agent any
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("anon-blog:${env.BUILD_NUMBER}")
                }
            }
        }
        stage('Push Docker Image to Local Registry') {
            steps {
                script {
                    docker.withRegistry('https://registry.vengarl.com/') {
                        docker.image("anon-blog:${env.BUILD_NUMBER}").push()
                    }
                }
            }
        }
    }
}
