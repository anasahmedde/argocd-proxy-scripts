# argocd-proxy-multicluster

ArgoCD proxy to abstract multicluster operations.


```
# Create and activate virtual env.
python3 -m venv venv
source venv/bin/activate

# Install zappa and dependencies.
pip install zappa
pip install -r requirements.txt

# For deploying ArgoCD proxy for first time.
zappa deploy prod 

# For updating ArgoCD proxy after first deployment.
zappa update prod 
```
