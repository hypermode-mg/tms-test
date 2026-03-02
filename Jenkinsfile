pipeline {
    agent any

    parameters {
        booleanParam(name: 'ROLLBACK_ONLY', defaultValue: false, description: 'Включить режим только отката')
    }

    environment {
        IMAGE_NAME = 'report-service'
        CONTAINER_NAME = 'report-service'
        HOST_PORT = '8081'
        CONTAINER_PORT = '5000'
        HEALTH_CHECK_URL = "http://localhost:${env.HOST_PORT}/health"
        VERSION_FILE = 'last_successful_build.txt'
    }

    stages {
        stage('Rollback (if ROLLBACK_ONLY)') {
            when { expression { params.ROLLBACK_ONLY } }
            steps {
                script {
                    echo 'Запуск режима отката (ROLLBACK_ONLY = true)'
                    rollbackToPreviousVersion()
                }
            }
        }

        stage('Test') {
            when { expression { !params.ROLLBACK_ONLY } }
            steps {
                echo 'Запуск тестов...'
                sh '''
                    python -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    pytest
                '''
            }
        }

        stage('Build') {
            when { expression { !params.ROLLBACK_ONLY } }
            steps {
                echo "Сборка Docker-образа: ${env.IMAGE_NAME}:${BUILD_NUMBER}"
                sh '''
                    docker build -t ${env.IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Deploy') {
            when { expression { !params.ROLLBACK_ONLY } }
            steps {
                echo 'Деплой новой версии...'
                script {
                    try {
                        // Сохраняем текущую версию как предыдущую перед деплоем
                        sh '''
                            if docker ps --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
                                docker stop ${CONTAINER_NAME}
                                docker rm ${CONTAINER_NAME}
                            fi
                        '''

                        // Запускаем новый контейнер
                        sh '''
                            docker run -d \
                                -p ${HOST_PORT}:${CONTAINER_PORT} \
                                --name ${CONTAINER_NAME} \
                                ${IMAGE_NAME}:${BUILD_NUMBER}
                        '''
                    } catch (Exception e) {
                        echo "Ошибка при деплое: ${e.message}"
                        rollbackToPreviousVersion()
                        error("Деплой завершился ошибкой, выполнен откат")
                    }
                }
            }
        }

        stage('Health-check') {
            when { expression { !params.ROLLBACK_ONLY } }
            steps {
                script {
                    try {
                        echo "Проверка работоспособности: ${env.HEALTH_CHECK_URL}"
                        sh "curl -f ${env.HEALTH_CHECK_URL}"
                        echo 'Health-check пройден успешно'

                        // Сохраняем успешную версию в файл
                        saveSuccessfulVersion("${BUILD_NUMBER}")
                    } catch (Exception e) {
                        echo "Health-check не пройден: ${e.message}"
                        echo 'Запуск автоматического отката...'
                        rollbackToPreviousVersion()
                        error("Health-check провалился, выполнен автоматический откат")
                    }
                }
            }
        }
    }

    post {
        failure {
            script {
                if (!params.ROLLBACK_ONLY) {
                    echo 'Pipeline завершился с ошибкой'
                }
            }
        }
        success {
            echo 'Pipeline успешно завершён'
        }
    }
}

def saveSuccessfulVersion(version) {
    echo "Сохранение успешной версии ${version} в ${env.VERSION_FILE}"
    sh '''
        echo "${version}" > ${env.VERSION_FILE}
        echo "Последняя успешная сборка: ${version} ($(date))" >> ${env.VERSION_FILE}
    '''
    archiveArtifacts artifacts: "${env.VERSION_FILE}", onlyIfSuccessful: false
}

def rollbackToPreviousVersion() {
    echo 'Выполнение отката на предыдущую версию...'
    script {
        def previousVersion = readFile(env.VERSION_FILE).trim()

        if (!previousVersion) {
            error "Файл ${env.VERSION_FILE} не найден или пуст. Невозможно выполнить откат."
        }

        echo "Обнаружена предыдущая успешная версия: ${previousVersion}"

        sh '''
            # Останавливаем текущий контейнер, если существует
            if docker ps --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
                docker stop ${CONTAINER_NAME}
                docker rm ${CONTAINER_NAME}
            fi

            # Запускаем предыдущую версию
            if docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "${IMAGE_NAME}:${previousVersion}"; then
                docker run -d \
                    -p ${HOST_PORT}:${CONTAINER_PORT} \
            --name ${CONTAINER_NAME} \
            ${IMAGE_NAME}:${previousVersion}
                echo "Откат выполнен на версию ${IMAGE_NAME}:${previousVersion}"
            else
                echo "Образ ${IMAGE_NAME}:${previousVersion} не найден, невозможно выполнить откат"
                exit 1
            fi
        '''
    }
}
