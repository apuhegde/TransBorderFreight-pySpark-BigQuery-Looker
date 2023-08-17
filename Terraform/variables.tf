locals {
  data_lake_bucket = "tbf-analysis-terraform"
}

variable "project" {
  description = "Your GCP Project ID"
  type = string
  default = "trans-border-freights-394419"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  type = string
  default = "us-central1"
}

variable "zone" {
  description = "zones in your region for GCP ex(a,b,c) "
  type = string
  default = "us-central1-a"
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  type = string
  default = "STANDARD"
}

variable "vm_image" {
  description = "Base image for your Virtual Machine."
  type = string
  default = "ubuntu-os-cloud/ubuntu-2004-lts"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "tbf_with_metadata2"
}


