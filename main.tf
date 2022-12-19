terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.30.0"
    }
  }
}
provider "azurerm" {
  features {}
  skip_provider_registration = true
}


resource "azurerm_resource_group" "lab" {
  name     = var.resource_group_name
  location = var.azure_region
}

resource "azurerm_storage_account" "lab" {
  name                     = var.azurerm_storage_account_name
  resource_group_name      = azurerm_resource_group.lab.name
  location                 = azurerm_resource_group.lab.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "lab" {
  name                  = var.azurerm_storage_container_name
  storage_account_name  = azurerm_storage_account.lab.name
  container_access_type = "private"
}

data "azurerm_client_config" "current" {
}


resource "azurerm_role_assignment" "lab" {
  scope                = azurerm_storage_account.lab.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}
