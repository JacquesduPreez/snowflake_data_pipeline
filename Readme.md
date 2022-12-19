# Readme

```bash
terraform init
terraform plan
```

```bash
terraform apply
```

```bash
cd az_py_upload
mv example_env.sh env.sh
az ad sp create-for-rbac --name dataloader
```

get the `appId`, `password` and `tenant` and enter it in `env.sh`

```bash
export AZURE_CLIENT_ID="appId"
export AZURE_TENANT_ID="tenant"
export AZURE_CLIENT_SECRET="password"
```

then 

```bash
. env.sh
```

Install azure dependencies

```bash
pip install -r requirements.txt
```

now change the `az.py` file to correspond to your storage account and blob container and execute

```bash
python az.py
```

It should upload the example file to your storage container