resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
  }
}

resource "helm_release" "kube_prometheus_stack" {
  name       = "my-k8s-prom-stack"
  namespace  = "monitoring"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  version    = "45.5.0"
  create_namespace = true

  depends_on = [
    kubernetes_namespace.monitoring
  ]

  set {
    name  = "prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues"
    value = "false"
  }

  set {
    name  = "grafana.sidecar.datasources.enabled"
    value = "true"
  }

    set {
    name  = "server.service.type"
    value = "ClusterIP"
  }
}


resource "helm_release" "metrics_server" {
  name       = "metrics-server"
  namespace  = "kube-system"
  repository = "https://kubernetes-sigs.github.io/metrics-server/" 
  chart      = "metrics-server"
  version    = "3.10.0"  
}

resource "kubernetes_ingress_v1" "prometheus_ingress" {
  metadata {
    name = "prometheus-ingress"
    namespace = "monitoring"
    # annotations = {
    #   "nginx.ingress.kubernetes.io/backend-protocol" = "HTTPS"
    # }

  }

  spec {
    ingress_class_name = "nginx"
    rule {
      host = "erangrafana.duckdns.org"
      http {
        path {
          backend {
            service {
              name = "my-k8s-prom-stack-grafana"
              port {
                number = 3000
              }
            }
          }
          path = "/"
        }
      }
    }
  }
}
