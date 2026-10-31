# Node Isolation Using Taints and Labels in Kubernetes

## Project Overview

This lab demonstrates how to achieve **Node Isolation** in a Kubernetes cluster using **Taints** and **Labels**. By combining both mechanisms, we ensure that:

1. **Taint (`NoSchedule`)**: Repels unauthorized pods from being scheduled on the target worker node unless they have a matching toleration.
2. **Label**: Attracts and identifies the specific node for targeted pod scheduling via `nodeSelector` or `nodeAffinity`.

> **Environment:** Killercoda Kubernetes Playground

---

## Lab Tasks

- [x] Apply a taint to a worker node with key `workload`, value `ivolveApp`, and effect `NoSchedule`.
- [x] Label the same worker node with `project=ivolve`.
- [x] Verify that both the taint and label have been applied successfully.

---

## Step-by-Step Implementation

### Step 1: Identify the Worker Node

First, list all nodes in the cluster to find the target node name:

```bash
kubectl get nodes
```

> **Screenshot:**
>
> ![List Nodes](screenshots/1.png)

---

### Step 2: Apply Taint to the Node

Apply a taint with key `workload`, value `ivolveApp`, and effect `NoSchedule`:

```bash
kubectl taint nodes controlplane workload=ivolveApp:NoSchedule
```

> **Screenshot:**
>
> ![Apply Taint](screenshots/2.png)

---

### Step 3: Apply Label to the Same Node

Assign the label `project=ivolve` to the node:

```bash
kubectl label nodes controlplane project=ivolve
```

> **Screenshot:**
>
> ![Apply Label](screenshots/3.png)

---

### Step 4: Verification

#### 1. Verify the Taint

Inspect the node details and check the **Taints** section:

```bash
kubectl describe node controlplane | grep -i taints
```

*Expected Output:*

```text
Taints:             workload=ivolveApp:NoSchedule
```

#### 2. Verify the Label

List the nodes with their labels to verify `project=ivolve`:

```bash
kubectl get nodes --show-labels
```

Or view the specific node's labels:

```bash
kubectl get node controlplane --show-labels
```

> **Screenshot:**
>
> ![Verify](screenshots/4.png)
