# this file is used to create GKE cluster, that will run our application

data "google_client_config" "default" {}

provider "kubernetes" {
  host                   = "https://${module.gke.endpoint}"
  token                  = var.gcp-service-account
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}

module "gke" {
  source                     = "terraform-google-modules/kubernetes-engine/google"
  version                    = "27.0.0"
  project_id                 = var.project-id
  name                       = "visawheels-cluster"
  region                     = var.region
  network                    = "default"
  subnetwork                 = "default"
  ip_range_pods              = var.ip_range_pods
  ip_range_services          = var.ip_range_services
  http_load_balancing        = true
  network_policy             = false
  remove_default_node_pool = true 


node_pools = [
    {
      name                      = "my-node-pool"
      machine_type              = "e2-medium"
      node_locations            = "europe-west4-b,europe-west4-c"
      min_count                 = 1
      max_count                 = 2
      local_ssd_count           = 0
      spot                      = false
      disk_size_gb              = 40
      disk_type                 = "pd-standard"
      image_type                = "COS_CONTAINERD"
      enable_gcfs               = false
      enable_gvnic              = false
      auto_repair               = true
      auto_upgrade              = true
      service_account           = var.gcp-service-account
      preemptible               = false
      initial_node_count        = 1
    },
  ]
}
