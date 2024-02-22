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

    stage('Deploy App') {
      steps {
        script {
          def precision = sh(script: 'python3 test-lda.py', returnStdout: true).trim()
          def modelHash = sh(script: 'head -n 1 model_hashes.txt', returnStdout: true).trim()
          if (precision.toInteger() > 62) {
            sh 'docker build -f Dockerfile . -t l0g1g06/mljenkins-inference:latest'
            sh 'docker push l0g1g06/mljenkins-inference:latest'
            sh 'tofu init'
            sh 'tofu plan'
            def userInput = input(id: 'confirm', message: 'Apply Terraform?', parameters: [ [$class: 'BooleanParameterDefinition', defaultValue: false, description: 'Apply terraform', name: 'confirm'] ])
            sh 'tofu apply -auto-approve'
            discordSend description: "Link Live App:",
                    footer: "http://0.0.0.0:8001/docs",
                    link: env.BUILD_URL,
                    result: currentBuild.currentResult,
                    title: modelHash,
                    webhookURL: "https://discord.com/api/webhooks/1207777679592394793/k0KTnD2qSX1N8-upTPvvNf3_RnDZ5fZdIhQtWSlU4zSvHrPFxmtP-SzjDeQbitGSRZes",
          } else {
            discordSend description: "Falha ao buildar:",
                    footer: "O modelo tem uma precisão menor que a desejada. Link download modelo: http://0.0.0.0:8000/download/model",
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