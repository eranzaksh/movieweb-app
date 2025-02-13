output "release_name" {
  description = "The name of the Prometheus Helm release"
  value       = helm_release.kube_prometheus_stack.name
}

output "namespace" {
  description = "The namespace where Prometheus is installed"
  value       = kubernetes_namespace.monitoring.metadata[0].name
}