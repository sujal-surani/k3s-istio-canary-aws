output "k3s-public_ip" {
  value = aws_instance.k3s_server.public_ip
}

output "k3s-instance_id" {
  value = aws_instance.k3s_server.id
}