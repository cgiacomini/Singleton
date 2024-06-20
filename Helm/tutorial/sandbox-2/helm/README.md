 helm install demo-chart-0.1.0.tgz   --generate-name
kubectl -n default  port-forward nginx-deployment-57d84f57dc-xn8zb  8080:80
