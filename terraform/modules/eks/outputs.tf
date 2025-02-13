// change all names to movies

output "eks_endpoint" {
    value = aws_eks_cluster.tf-movies.endpoint
}

output "cluster_ca" {
  value = aws_eks_cluster.tf-movies.certificate_authority[0].data
}

output "cluster_name" {
  value = aws_eks_cluster.tf-movies.name
}