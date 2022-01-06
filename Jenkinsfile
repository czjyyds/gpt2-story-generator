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
                }
            }
        }
        stage('Copy Files') {
            steps {
                sh '''
                rm ${WORKSPACE}/src/config.ini
                cp ${LOCAL_STORAGE_PATH}/config/config.ini ${WORKSPACE}/src/
                rm -r ${WORKSPACE}/src/generation/model/
                cp -r ${LOCAL_STORAGE_PATH}/generation/model ${WORKSPACE}/src/generation/
                rm -r ${WORKSPACE}/src/video_search/model/
                cp -r ${LOCAL_STORAGE_PATH}/video_search/model ${WORKSPACE}/src/video_search/
                rm -r ${WORKSPACE}/etc/cert/
                cp -r ${LOCAL_STORAGE_PATH}/cert ${WORKSPACE}/etc/
                '''
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
