# variables for main file
# using .tfvars file, for sensitive data (where default value not exists)

variable "project-id" {
    description = "The project ID in gcp"
    type = string
}

variable "gcp-service-account" {
    description = "The service account to use for gcp"
    type = string
}

variable "region" {
    description = "The region to use for gcp"
    type = string
    default = "europe-west4"
}

variable "node_locations" {
    description = "The node locations to use for gcp"
    type = string
    default = "{europe-west4-b,europe-west4-c}"
  
}

variable "gke-version" {
    description = "The version of gke to install, check for latest version"
    type = string
    default = "27.0.0"

}

# The following ranges have to be set on gcp
variable "ip_range_pods" {
    description = "The ip range for pods, need to have that set on gcp"
    type = string
    default = "europe-west4-pods"
}

variable "ip_range_services" {
    description = "The ip range for services, need to have that set on gcp"
    type = string
    default = "europe-west4-services"
}

