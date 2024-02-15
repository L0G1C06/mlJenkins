pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        git(url: 'https://github.com/L0G1C06/mlJenkins', branch: 'feat-model')
      }
    }
    stage('Build') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Train') {
      steps {
        sh 'python3 train-lda.py'
      }
    }
    stage('Docker Login') {
      steps {
        withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'DockerHub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]) {
            sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
        }
      }
    }
    stage('Deploy') {
      steps {
        script {
          def precision = sh(script: 'python3 test-lda.py', returnStdout: true).trim()
          if (precision.toFloat() > 62) {
            sh 'docker build -f Dockerfile . -t l0g1g06/mljenkins:latest'
            sh 'docker push l0g1g06/mljenkins:latest'
            discordSend(message: 'Link do container para deploy: https://hub.docker.com/repository/docker/l0g1g06/mljenkins/general')
          } else {
            discordSend(message: 'O modelo tem uma precisão menor que 62%')
          }
        }
      }
    }

  }
}

def discordSend(def message){
  discordSend message: "${message}",
              webhookURL: 'https://discord.com/api/webhooks/1207777679592394793/k0KTnD2qSX1N8-upTPvvNf3_RnDZ5fZdIhQtWSlU4zSvHrPFxmtP-SzjDeQbitGSRZes'
}