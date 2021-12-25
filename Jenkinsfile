pipeline {
    agent any
    stages {
        stage('Cleanup') {
            steps {
                script {
                    sh 'docker-compose down'
                    try {
                      sh 'docker rm -f $(docker ps -a -q)'
                    } catch (err) {}
                    try {
                      sh 'docker volume rm $(docker volume ls -q)'
                    } catch (err) {}
                    try {
                      sh 'docker rmi $(docker images -q)'
                    } catch (err) {}
                }
            }
        }
        stage('Build') {
            steps {
                sh '''
                docker-compose -f docker-compose.prod.yml up -d --remove-orphans
                '''
            }
        }
        stage('Warmup') {
            steps {
                sh 'sleep 60'
            }
        }
    }
}
