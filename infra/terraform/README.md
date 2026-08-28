# Terraform

Один файл `main.tf`, который описывает VM в Yandex Cloud, куда можно
залить проект и поднять `docker compose up`.

## Использование

```bash
export TF_VAR_yc_token="<oauth-токен>"
export TF_VAR_yc_cloud_id="<cloud-id>"
export TF_VAR_yc_folder_id="<folder-id>"

terraform init
terraform plan
```

`terraform apply` создаёт реальный сервер (платно), поэтому постоянно
запущенным его не держал — важно, что `plan` проходит без ошибок.
