terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
    project = var.project
    region = var.region
}

# Data Lake Bucket
resource "google_storage_bucket" "data_lake_bucket" {
  name          = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region

  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  force_destroy = false
}

# Data Warehouse
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}

#network resource
resource "google_compute_network" "tbf_network" {
  name = "terraform-network"
  auto_create_subnetworks = "true"
}


#VM firewall
resource "google_compute_firewall" "ssh-rule" {
  name = "demo-ssh"
  network = google_compute_network.tbf_network.self_link
  allow {
    protocol = "tcp"
    ports = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  
}


# VM instance
resource "google_compute_instance" "vm_instance" {
  name          = "terraform-instance"
  project       = var.project
  machine_type  = "e2-standard-4"
  zone          = var.zone

  boot_disk {
    initialize_params {
      image = var.vm_image
    }
  }

  network_interface {
    # network = "default"
    network = google_compute_network.tbf_network.self_link
    access_config {
      // Ephemeral public IP
    }
  }

  # metadata_startup_script = "${file("./docker_installation.sh")}"

  # provisioner "local-exec" {
  #   command = "gcloud compute config-ssh"
  # }

  # provisioner "local-exec" {
  #   command = <<EOT
  #   gcloud compute config-ssh
  #   gcloud compute scp ~/.google/credentials/google_credentials.json airflow-instance:~ --zone=us-central1-a
  #   EOT
  # }

}

output "ip" {
  value = "${google_compute_instance.vm_instance.network_interface.0.access_config.0.nat_ip}"
}


/*
resource "google_project_service" "workflows" {
  service            = "workflows.googleapis.com"
  disable_on_destroy = false
}

#Dataproc cluster
resource "google_dataproc_cluster" "tbf-terraform-cluster" {
  name     = "tbf-terraform-cluster"
  region   = "us-central1"
}
*/