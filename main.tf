terraform {
    required_providers {
      docker = {
        source = "kreuzwerker/docker"
        version = "~> 3.0.1"
      }
    }
}

provider "docker" {}

resource "docker_image" "mljenkins-inference"{
    name = "l0g1g06/mljenkins-inference:1.2"
    keep_locally = false 
}

resource "docker_container" "mljenkins-inference"{
    image = docker_image.mljenkins-inference.image_id
    name = "api-inference"

    ports {
        internal = 8001
        external = 8001
    }
}

resource "docker_image" "mljenkins-staging"{
    name = "l0g1g06/mljenkins-staging:latest"
    keep_locally = false 
}

resource "docker_container" "mljenkins-staging"{
    image = docker_image.mljenkins-staging.image_id
    name = "model-staging"

    ports {
      internal = 8000
      external = 8000
    }
}