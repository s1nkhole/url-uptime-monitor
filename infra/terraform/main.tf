# Простое описание одного облачного сервера (Yandex Cloud), на котором
# можно поднять проект через docker compose. Без разбивки на модули —
# для одного VM это было бы избыточно.

terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.130"
    }
  }
}

provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
  zone      = "ru-central1-a"
}

variable "yc_token" {
  description = "OAuth-токен Yandex Cloud, передавать через TF_VAR_yc_token"
  type        = string
  sensitive   = true
}

variable "yc_cloud_id" {
  type = string
}

variable "yc_folder_id" {
  type = string
}

resource "yandex_compute_instance" "vm" {
  name        = "url-uptime-monitor-vm"
  platform_id = "standard-v3"
  zone        = "ru-central1-a"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd8vqhkkq5deui9jkm2h" # Ubuntu 22.04 LTS, актуальный id уточнять через yc cli
      size     = 20
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_ed25519.pub")}"
  }
}

resource "yandex_vpc_network" "network" {
  name = "url-uptime-monitor-network"
}

resource "yandex_vpc_subnet" "subnet" {
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["10.10.0.0/24"]
}

output "public_ip" {
  value = yandex_compute_instance.vm.network_interface[0].nat_ip_address
}
