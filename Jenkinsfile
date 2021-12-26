pipeline {
    agent any
    stages {
        stage('Cleanup') {
            steps {
                discordSend description: "Build ${BUILD_DISPLAY_NAME} started", result: "SUCCESS", unstable: false, title: "${JOB_NAME}", webhookURL: "${WEBHOOK_URL}"
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
                    sh "rm ${WORKSPACE}/src/config.ini"
                    sh "cp ${CONFIG_FILE_PATH} ${WORKSPACE}/src/"
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
    post {
        always {
            discordSend description: "Build ${BUILD_DISPLAY_NAME} ${currentBuild.currentResult.toLowerCase()} after ${currentBuild.durationString.minus(' and counting')}", result: "${currentBuild.currentResult}", unstable: false, title: "${JOB_NAME}", webhookURL: "${WEBHOOK_URL}"
        }
    }
}
