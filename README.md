# Kubernetes-HPA-Probes

## Description
This project investigates the capabilities of Horizontal Pod Autoscaler (HPA) and Liveness Probe features in Kubernetes by simulating the behavior of a Weaviate vector store using a simple Flask application.

**weaviate folder**: This folder contains files for the Weaviate simulator. Since Kubernetes does not care about what is actually running inside each instance, and for easier manipulation of CPU/memory usage or putting the instance in an unhealthy state, a simple Flask app was created instead of using Weaviate itself. The code is simple and includes comments for clarity. You can also find its Dockerfile to build your specific one. The Docker image is publicly available on the following registry: `hajizadeh2079/weaviate`.

**kubernetes folder**: This folder contains files for Kubernetes configuration. The main configs are well-commented, allowing for easy modification to observe changes in the simulation process.

## Requirements

Install Docker ([Installation Guide](https://docs.docker.com/engine/install/ubuntu/)), kubectl ([Installation Guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)), and minikube ([Installation Guide](https://minikube.sigs.k8s.io/docs/start/)).

## Simulation Process

1. **Start your Kubernetes cluster**:
   ```bash
   minikube start --addons=metrics-server
   ```

2. **Create required Kubernetes manifest**:
   ```bash
   kubectl apply -f weaviate.yaml
   kubectl apply -f hpa.yaml
   ```

3. **Bind Kubernetes service to localhost** (to be accessible via curl):
   ```bash
   kubectl port-forward service/weaviate 5000:5000
   ```

4. **Before proceeding**, it is useful to familiarize yourself with the following commands:
   - `watch "kubectl get pod"`
   - `watch "kubectl top pod"`
   - `watch "kubectl describe hpa weaviate-hpa"`
   - `kubectl describe pod {pod_name}`

### Liveness Probe

To simulate an unhealthy situation, use the following command to put the instance in an unhealthy state:
```bash
curl http://localhost:5000/set_health_false
```
Using `kubectl describe pod {pod_name}`, observe that the liveness check of Kubernetes is failing, and Kubernetes detects that the instance is unhealthy. Eventually, Kubernetes will restart the instance. Using `watch "kubectl get pod"`, you can see that the instance has been restarted.

*Note*: In addition to liveness probe, there are two other probes in Kubernetes, readiness and startup. For more details, see [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

### Autoscaling

To simulate CPU/memory usage increase, use one of the following commands (you can use `watch "kubectl top pod"` to monitor CPU and memory usage of instances):
```bash
curl -m 0 http://localhost:5000/increase_memory
curl -m 0 http://localhost:5000/increase_cpu
```
Using `watch "kubectl describe hpa weaviate-hpa"`, you can see that HPA detects that CPU/memory usage is above the threshold and scales up the number of instances. When the usage is far below the threshold, HPA scales down the number of instances. HPA will wait for 5 minutes before scaling down the number of instances. Using `watch "kubectl get pod"`, you can see the creation/deletion of instances in the whole process.

*Some Notes*:
- Both scale down and up speed are configurable in Kubernetes, using scaling policies. For more details, see [Scaling Policies](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#scaling-policies).
- In addition to built-in metrics, custom metrics can be used for scaling up and down, see [Documentation](https://caiolombello.medium.com/kubernetes-hpa-custom-metrics-for-effective-cpu-memory-scaling-23526bba9b4). These metrics depend a lot on the application itself. Unfortunately, Weaviate does not provide any metrics regarding network usage, it just provides metrics regarding user requests, see [Weaviate documentation](https://weaviate.io/developers/weaviate/configuration/monitoring#obtainable-metrics). Of course, sidecars (or any other similar mechanism) can be used to get the required metrics by them. For example, see [Istio documentation](https://istio.io/latest/docs/reference/config/metrics/#metrics).
- For more details on Kubernetes HPA, see [Kubernetes documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
