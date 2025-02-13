resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
  }
}

resource "helm_release" "argocd" {
  name       = "argocd"
  namespace  = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "3.35.4"



  set {
    name  = "server.service.type"
    value = "ClusterIP"
  }

}
# If i want to change the service name
# data "kubernetes_service" "argocd_server" {
#   metadata {
#     name      = "argocd-server"
#     namespace = kubernetes_namespace.argocd.metadata[0].name
#   }
# }
resource "kubernetes_ingress_v1" "argocd_ingress" {
  metadata {
    name = "argocd-ingress"
    namespace = "argocd"
    annotations = {
      "nginx.ingress.kubernetes.io/backend-protocol" = "HTTPS"
    }

  }

  spec {
    ingress_class_name = "nginx"
    rule {
      host = "eranargocd.duckdns.org"
      http {
        path {
          backend {
            service {
              name = "argocd-server"
              port {
                number = 443
              }
            }
          }
          path = "/"
        }
      }
    }
  }
}