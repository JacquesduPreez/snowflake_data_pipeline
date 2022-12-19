variable "azure_region" {
  description = "Azure region for all resources."
  type        = string
  default     = "eastus2"
}

variable "resource_group_name" {
  type = string
}

variable "azurerm_storage_account_name" {
  type = string
}

variable "azurerm_storage_container_name" {
  type = string
}
