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
        withCredentials(bindings: [[$class: 'UsernamePasswordMultiBinding', credentialsId: 'DockerHub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]) {
          sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
        }

      }
    }

    stage('Deploy') {
      steps {
        script {
          def precision = sh(script: 'python3 test-lda.py', returnStdout: true).trim()
          if (precision.toInteger() > 62) {
            sh 'docker build -f Dockerfile . -t l0g1g06/mljenkins:latest'
            sh 'docker push l0g1g06/mljenkins:latest'
            discordSend description: "Link para o novo container para deploy:",
            footer: "https://hub.docker.com/repository/docker/l0g1g06/mljenkins/general",
            link: env.BUILD_URL,
            result: currentBuild.currentResult,
            title: JOB_NAME,
            webhookURL: "https://discord.com/api/webhooks/1207777679592394793/k0KTnD2qSX1N8-upTPvvNf3_RnDZ5fZdIhQtWSlU4zSvHrPFxmtP-SzjDeQbitGSRZes"
          } else {
            discordSend description: "Falha ao buildar:",
            footer: "O modelo tem uma precisão menor que a desejada",
            link: env.BUILD_URL,
            result: currentBuild.currentResult,
            title: JOB_NAME,
            webhookURL: "https://discord.com/api/webhooks/1207777679592394793/k0KTnD2qSX1N8-upTPvvNf3_RnDZ5fZdIhQtWSlU4zSvHrPFxmtP-SzjDeQbitGSRZes"
            sh 'python3 send-model-staging.py'
          }
        }

      }
    }

  }
}