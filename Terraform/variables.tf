locals {
  data_lake_bucket = "tbf-analysis-terraform"
}

variable "project" {
  description = "Your GCP Project ID"
  type        = string
  default     = "trans-border-freights-394419"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "zones in your region for GCP ex(a,b,c) "
  type        = string
  default     = "us-central1-a"
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  type        = string
  default     = "STANDARD"
}

# variable "vm_image" {
#   description = "Base image for your Virtual Machine."
#   type = string
#   default = "ubuntu-os-cloud/ubuntu-2004-lts"
# }

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "tbf_with_metadata2"
}


####### Dataproc variables
variable "dataproc_master_machine_type" {
  type        = string
  description = "dataproc master node machine tyoe"
  default     = "e2-standard-4"
}

variable "dataproc_worker_machine_type" {
  type        = string
  description = "dataproc worker nodes machine type"
  default     = "e2-standard-4"
}

variable "dataproc_workers_count" {
  type        = number
  description = "count of worker nodes in cluster"
  default     = 2
}
variable "dataproc_master_bootdisk" {
  type        = number
  description = "primary disk attached to master node, specified in GB"
  default     = 100
}

variable "dataproc_worker_bootdisk" {
  type        = number
  description = "primary disk attached to master node, specified in GB"
  default     = 50
}

variable "worker_local_ssd" {
  type        = number
  description = "primary disk attached to master node, specified in GB"
  default     = 50
}

variable "preemptible_worker" {
  type        = number
  description = "number of preemptible nodes to create"
  default     = 1
}

variable "dataproc_software_image_version" {
  type        = string
  description = "Image version of OS to for the dataproc cluster machine"
  default     = "2.1.21-ubuntu20"

}

variable "google_service_acct_email" {
  type        = string
  description = "Email of service account to be used for dataproc operation"
  default     = "terraform@trans-border-freights-394419.iam.gserviceaccount.com"

}

variable "pip_packages" {
  type        = string
  description = "A space separated list of pip packages to be installed"
  default     = "xlrd"
}

variable "pip_initialization_script" {
  type        = string
  description = "Location of script in GS used to install pip packages (https://github.com/GoogleCloudPlatform/dataproc-initialization-actions)"
  default     = "gs://tbf-analysis-accessory/scripts/dataproc-pip-installation.sh"
}