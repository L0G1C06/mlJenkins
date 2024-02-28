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
    name = "l0g1g06/mljenkins-inference:latest"
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