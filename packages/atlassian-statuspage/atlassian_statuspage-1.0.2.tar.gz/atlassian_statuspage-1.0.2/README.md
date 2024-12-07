# statuspage

- API version: 1.0.0
- Package version: v1.0.0

For more information, please visit [https://developer.statuspage.io](https://developer.statuspage.io)

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+ssh://spkishore007@github.com/statuspage.git
```

Then import the package:
```python
import statuspage 
```

### Setuptools

Install via Pip
( for dev, enable venv)
```sh
pip install -e .
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import statuspage
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import statuspage
from statuspage.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = statuspage.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = statuspage.ComponentGroupsApi(statuspage.ApiClient(configuration))
page_id = 'page_id_example' # str | Page identifier
id = 'id_example' # str | Component group identifier

```

## Documentation for API Endpoints

All URIs are relative to *https://api.statuspage.io/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ComponentGroupsApi* | [**delete_pages_page_id_component_groups_id**](docs/ComponentGroupsApi.md#delete_pages_page_id_component_groups_id) | **DELETE** /pages/{page_id}/component-groups/{id} | Delete a component group
*ComponentGroupsApi* | [**get_pages_page_id_component_groups**](docs/ComponentGroupsApi.md#get_pages_page_id_component_groups) | **GET** /pages/{page_id}/component-groups | Get a list of component groups
*ComponentGroupsApi* | [**get_pages_page_id_component_groups_id**](docs/ComponentGroupsApi.md#get_pages_page_id_component_groups_id) | **GET** /pages/{page_id}/component-groups/{id} | Get a component group
*ComponentGroupsApi* | [**get_pages_page_id_component_groups_id_uptime**](docs/ComponentGroupsApi.md#get_pages_page_id_component_groups_id_uptime) | **GET** /pages/{page_id}/component-groups/{id}/uptime | Get uptime data for a component group
*ComponentGroupsApi* | [**patch_pages_page_id_component_groups_id**](docs/ComponentGroupsApi.md#patch_pages_page_id_component_groups_id) | **PATCH** /pages/{page_id}/component-groups/{id} | Update a component group
*ComponentGroupsApi* | [**post_pages_page_id_component_groups**](docs/ComponentGroupsApi.md#post_pages_page_id_component_groups) | **POST** /pages/{page_id}/component-groups | Create a component group
*ComponentGroupsApi* | [**put_pages_page_id_component_groups_id**](docs/ComponentGroupsApi.md#put_pages_page_id_component_groups_id) | **PUT** /pages/{page_id}/component-groups/{id} | Update a component group
*ComponentsApi* | [**delete_pages_page_id_components_component_id**](docs/ComponentsApi.md#delete_pages_page_id_components_component_id) | **DELETE** /pages/{page_id}/components/{component_id} | Delete a component
*ComponentsApi* | [**delete_pages_page_id_components_component_id_page_access_groups**](docs/ComponentsApi.md#delete_pages_page_id_components_component_id_page_access_groups) | **DELETE** /pages/{page_id}/components/{component_id}/page_access_groups | Remove page access groups from a component
*ComponentsApi* | [**delete_pages_page_id_components_component_id_page_access_users**](docs/ComponentsApi.md#delete_pages_page_id_components_component_id_page_access_users) | **DELETE** /pages/{page_id}/components/{component_id}/page_access_users | Remove page access users from component
*ComponentsApi* | [**get_pages_page_id_components**](docs/ComponentsApi.md#get_pages_page_id_components) | **GET** /pages/{page_id}/components | Get a list of components
*ComponentsApi* | [**get_pages_page_id_components_component_id**](docs/ComponentsApi.md#get_pages_page_id_components_component_id) | **GET** /pages/{page_id}/components/{component_id} | Get a component
*ComponentsApi* | [**get_pages_page_id_components_component_id_uptime**](docs/ComponentsApi.md#get_pages_page_id_components_component_id_uptime) | **GET** /pages/{page_id}/components/{component_id}/uptime | Get uptime data for a component
*ComponentsApi* | [**patch_pages_page_id_components_component_id**](docs/ComponentsApi.md#patch_pages_page_id_components_component_id) | **PATCH** /pages/{page_id}/components/{component_id} | Update a component
*ComponentsApi* | [**post_pages_page_id_components**](docs/ComponentsApi.md#post_pages_page_id_components) | **POST** /pages/{page_id}/components | Create a component
*ComponentsApi* | [**post_pages_page_id_components_component_id_page_access_groups**](docs/ComponentsApi.md#post_pages_page_id_components_component_id_page_access_groups) | **POST** /pages/{page_id}/components/{component_id}/page_access_groups | Add page access groups to a component
*ComponentsApi* | [**post_pages_page_id_components_component_id_page_access_users**](docs/ComponentsApi.md#post_pages_page_id_components_component_id_page_access_users) | **POST** /pages/{page_id}/components/{component_id}/page_access_users | Add page access users to a component
*ComponentsApi* | [**put_pages_page_id_components_component_id**](docs/ComponentsApi.md#put_pages_page_id_components_component_id) | **PUT** /pages/{page_id}/components/{component_id} | Update a component
*IncidentPostmortemApi* | [**delete_pages_page_id_incidents_incident_id_postmortem**](docs/IncidentPostmortemApi.md#delete_pages_page_id_incidents_incident_id_postmortem) | **DELETE** /pages/{page_id}/incidents/{incident_id}/postmortem | Delete Postmortem
*IncidentPostmortemApi* | [**get_pages_page_id_incidents_incident_id_postmortem**](docs/IncidentPostmortemApi.md#get_pages_page_id_incidents_incident_id_postmortem) | **GET** /pages/{page_id}/incidents/{incident_id}/postmortem | Get Postmortem
*IncidentPostmortemApi* | [**put_pages_page_id_incidents_incident_id_postmortem**](docs/IncidentPostmortemApi.md#put_pages_page_id_incidents_incident_id_postmortem) | **PUT** /pages/{page_id}/incidents/{incident_id}/postmortem | Create Postmortem
*IncidentPostmortemApi* | [**put_pages_page_id_incidents_incident_id_postmortem_publish**](docs/IncidentPostmortemApi.md#put_pages_page_id_incidents_incident_id_postmortem_publish) | **PUT** /pages/{page_id}/incidents/{incident_id}/postmortem/publish | Publish Postmortem
*IncidentPostmortemApi* | [**put_pages_page_id_incidents_incident_id_postmortem_revert**](docs/IncidentPostmortemApi.md#put_pages_page_id_incidents_incident_id_postmortem_revert) | **PUT** /pages/{page_id}/incidents/{incident_id}/postmortem/revert | Revert Postmortem
*IncidentSubscribersApi* | [**delete_pages_page_id_incidents_incident_id_subscribers_subscriber_id**](docs/IncidentSubscribersApi.md#delete_pages_page_id_incidents_incident_id_subscribers_subscriber_id) | **DELETE** /pages/{page_id}/incidents/{incident_id}/subscribers/{subscriber_id} | Unsubscribe an incident subscriber
*IncidentSubscribersApi* | [**get_pages_page_id_incidents_incident_id_subscribers**](docs/IncidentSubscribersApi.md#get_pages_page_id_incidents_incident_id_subscribers) | **GET** /pages/{page_id}/incidents/{incident_id}/subscribers | Get a list of incident subscribers
*IncidentSubscribersApi* | [**get_pages_page_id_incidents_incident_id_subscribers_subscriber_id**](docs/IncidentSubscribersApi.md#get_pages_page_id_incidents_incident_id_subscribers_subscriber_id) | **GET** /pages/{page_id}/incidents/{incident_id}/subscribers/{subscriber_id} | Get an incident subscriber
*IncidentSubscribersApi* | [**post_pages_page_id_incidents_incident_id_subscribers**](docs/IncidentSubscribersApi.md#post_pages_page_id_incidents_incident_id_subscribers) | **POST** /pages/{page_id}/incidents/{incident_id}/subscribers | Create an incident subscriber
*IncidentSubscribersApi* | [**post_pages_page_id_incidents_incident_id_subscribers_subscriber_id_resend_confirmation**](docs/IncidentSubscribersApi.md#post_pages_page_id_incidents_incident_id_subscribers_subscriber_id_resend_confirmation) | **POST** /pages/{page_id}/incidents/{incident_id}/subscribers/{subscriber_id}/resend_confirmation | Resend confirmation to an incident subscriber
*IncidentUpdatesApi* | [**patch_pages_page_id_incidents_incident_id_incident_updates_incident_update_id**](docs/IncidentUpdatesApi.md#patch_pages_page_id_incidents_incident_id_incident_updates_incident_update_id) | **PATCH** /pages/{page_id}/incidents/{incident_id}/incident_updates/{incident_update_id} | Update a previous incident update
*IncidentUpdatesApi* | [**put_pages_page_id_incidents_incident_id_incident_updates_incident_update_id**](docs/IncidentUpdatesApi.md#put_pages_page_id_incidents_incident_id_incident_updates_incident_update_id) | **PUT** /pages/{page_id}/incidents/{incident_id}/incident_updates/{incident_update_id} | Update a previous incident update
*IncidentsApi* | [**delete_pages_page_id_incidents_incident_id**](docs/IncidentsApi.md#delete_pages_page_id_incidents_incident_id) | **DELETE** /pages/{page_id}/incidents/{incident_id} | Delete an incident
*IncidentsApi* | [**get_pages_page_id_incidents**](docs/IncidentsApi.md#get_pages_page_id_incidents) | **GET** /pages/{page_id}/incidents | Get a list of incidents
*IncidentsApi* | [**get_pages_page_id_incidents_active_maintenance**](docs/IncidentsApi.md#get_pages_page_id_incidents_active_maintenance) | **GET** /pages/{page_id}/incidents/active_maintenance | Get a list of active maintenances
*IncidentsApi* | [**get_pages_page_id_incidents_incident_id**](docs/IncidentsApi.md#get_pages_page_id_incidents_incident_id) | **GET** /pages/{page_id}/incidents/{incident_id} | Get an incident
*IncidentsApi* | [**get_pages_page_id_incidents_scheduled**](docs/IncidentsApi.md#get_pages_page_id_incidents_scheduled) | **GET** /pages/{page_id}/incidents/scheduled | Get a list of scheduled incidents
*IncidentsApi* | [**get_pages_page_id_incidents_unresolved**](docs/IncidentsApi.md#get_pages_page_id_incidents_unresolved) | **GET** /pages/{page_id}/incidents/unresolved | Get a list of unresolved incidents
*IncidentsApi* | [**get_pages_page_id_incidents_upcoming**](docs/IncidentsApi.md#get_pages_page_id_incidents_upcoming) | **GET** /pages/{page_id}/incidents/upcoming | Get a list of upcoming incidents
*IncidentsApi* | [**patch_pages_page_id_incidents_incident_id**](docs/IncidentsApi.md#patch_pages_page_id_incidents_incident_id) | **PATCH** /pages/{page_id}/incidents/{incident_id} | Update an incident
*IncidentsApi* | [**post_pages_page_id_incidents**](docs/IncidentsApi.md#post_pages_page_id_incidents) | **POST** /pages/{page_id}/incidents | Create an incident
*IncidentsApi* | [**put_pages_page_id_incidents_incident_id**](docs/IncidentsApi.md#put_pages_page_id_incidents_incident_id) | **PUT** /pages/{page_id}/incidents/{incident_id} | Update an incident
*MetricProvidersApi* | [**delete_pages_page_id_metrics_providers_metrics_provider_id**](docs/MetricProvidersApi.md#delete_pages_page_id_metrics_providers_metrics_provider_id) | **DELETE** /pages/{page_id}/metrics_providers/{metrics_provider_id} | Delete a metric provider
*MetricProvidersApi* | [**get_pages_page_id_metrics_providers**](docs/MetricProvidersApi.md#get_pages_page_id_metrics_providers) | **GET** /pages/{page_id}/metrics_providers | Get a list of metric providers
*MetricProvidersApi* | [**get_pages_page_id_metrics_providers_metrics_provider_id**](docs/MetricProvidersApi.md#get_pages_page_id_metrics_providers_metrics_provider_id) | **GET** /pages/{page_id}/metrics_providers/{metrics_provider_id} | Get a metric provider
*MetricProvidersApi* | [**get_pages_page_id_metrics_providers_metrics_provider_id_metrics**](docs/MetricProvidersApi.md#get_pages_page_id_metrics_providers_metrics_provider_id_metrics) | **GET** /pages/{page_id}/metrics_providers/{metrics_provider_id}/metrics | List metrics for a metric provider
*MetricProvidersApi* | [**patch_pages_page_id_metrics_providers_metrics_provider_id**](docs/MetricProvidersApi.md#patch_pages_page_id_metrics_providers_metrics_provider_id) | **PATCH** /pages/{page_id}/metrics_providers/{metrics_provider_id} | Update a metric provider
*MetricProvidersApi* | [**post_pages_page_id_metrics_providers**](docs/MetricProvidersApi.md#post_pages_page_id_metrics_providers) | **POST** /pages/{page_id}/metrics_providers | Create a metric provider
*MetricProvidersApi* | [**post_pages_page_id_metrics_providers_metrics_provider_id_metrics**](docs/MetricProvidersApi.md#post_pages_page_id_metrics_providers_metrics_provider_id_metrics) | **POST** /pages/{page_id}/metrics_providers/{metrics_provider_id}/metrics | Create a metric for a metric provider
*MetricProvidersApi* | [**put_pages_page_id_metrics_providers_metrics_provider_id**](docs/MetricProvidersApi.md#put_pages_page_id_metrics_providers_metrics_provider_id) | **PUT** /pages/{page_id}/metrics_providers/{metrics_provider_id} | Update a metric provider
*MetricsApi* | [**delete_pages_page_id_metrics_metric_id**](docs/MetricsApi.md#delete_pages_page_id_metrics_metric_id) | **DELETE** /pages/{page_id}/metrics/{metric_id} | Delete a metric
*MetricsApi* | [**delete_pages_page_id_metrics_metric_id_data**](docs/MetricsApi.md#delete_pages_page_id_metrics_metric_id_data) | **DELETE** /pages/{page_id}/metrics/{metric_id}/data | Reset data for a metric
*MetricsApi* | [**get_pages_page_id_metrics**](docs/MetricsApi.md#get_pages_page_id_metrics) | **GET** /pages/{page_id}/metrics | Get a list of metrics
*MetricsApi* | [**get_pages_page_id_metrics_metric_id**](docs/MetricsApi.md#get_pages_page_id_metrics_metric_id) | **GET** /pages/{page_id}/metrics/{metric_id} | Get a metric
*MetricsApi* | [**get_pages_page_id_metrics_providers_metrics_provider_id_metrics**](docs/MetricsApi.md#get_pages_page_id_metrics_providers_metrics_provider_id_metrics) | **GET** /pages/{page_id}/metrics_providers/{metrics_provider_id}/metrics | List metrics for a metric provider
*MetricsApi* | [**patch_pages_page_id_metrics_metric_id**](docs/MetricsApi.md#patch_pages_page_id_metrics_metric_id) | **PATCH** /pages/{page_id}/metrics/{metric_id} | Update a metric
*MetricsApi* | [**post_pages_page_id_metrics_data**](docs/MetricsApi.md#post_pages_page_id_metrics_data) | **POST** /pages/{page_id}/metrics/data | Add data points to metrics
*MetricsApi* | [**post_pages_page_id_metrics_metric_id_data**](docs/MetricsApi.md#post_pages_page_id_metrics_metric_id_data) | **POST** /pages/{page_id}/metrics/{metric_id}/data | Add data to a metric
*MetricsApi* | [**post_pages_page_id_metrics_providers_metrics_provider_id_metrics**](docs/MetricsApi.md#post_pages_page_id_metrics_providers_metrics_provider_id_metrics) | **POST** /pages/{page_id}/metrics_providers/{metrics_provider_id}/metrics | Create a metric for a metric provider
*MetricsApi* | [**put_pages_page_id_metrics_metric_id**](docs/MetricsApi.md#put_pages_page_id_metrics_metric_id) | **PUT** /pages/{page_id}/metrics/{metric_id} | Update a metric
*PageAccessGroupComponentsApi* | [**delete_pages_page_id_page_access_groups_page_access_group_id_components**](docs/PageAccessGroupComponentsApi.md#delete_pages_page_id_page_access_groups_page_access_group_id_components) | **DELETE** /pages/{page_id}/page_access_groups/{page_access_group_id}/components | Delete components for a page access group
*PageAccessGroupComponentsApi* | [**delete_pages_page_id_page_access_groups_page_access_group_id_components_component_id**](docs/PageAccessGroupComponentsApi.md#delete_pages_page_id_page_access_groups_page_access_group_id_components_component_id) | **DELETE** /pages/{page_id}/page_access_groups/{page_access_group_id}/components/{component_id} | Remove a component from a page access group
*PageAccessGroupComponentsApi* | [**get_pages_page_id_page_access_groups_page_access_group_id_components**](docs/PageAccessGroupComponentsApi.md#get_pages_page_id_page_access_groups_page_access_group_id_components) | **GET** /pages/{page_id}/page_access_groups/{page_access_group_id}/components | List components for a page access group
*PageAccessGroupComponentsApi* | [**patch_pages_page_id_page_access_groups_page_access_group_id_components**](docs/PageAccessGroupComponentsApi.md#patch_pages_page_id_page_access_groups_page_access_group_id_components) | **PATCH** /pages/{page_id}/page_access_groups/{page_access_group_id}/components | Add components to page access group
*PageAccessGroupComponentsApi* | [**post_pages_page_id_page_access_groups_page_access_group_id_components**](docs/PageAccessGroupComponentsApi.md#post_pages_page_id_page_access_groups_page_access_group_id_components) | **POST** /pages/{page_id}/page_access_groups/{page_access_group_id}/components | Replace components for a page access group
*PageAccessGroupComponentsApi* | [**put_pages_page_id_page_access_groups_page_access_group_id_components**](docs/PageAccessGroupComponentsApi.md#put_pages_page_id_page_access_groups_page_access_group_id_components) | **PUT** /pages/{page_id}/page_access_groups/{page_access_group_id}/components | Add components to page access group
*PageAccessGroupsApi* | [**delete_pages_page_id_page_access_groups_page_access_group_id**](docs/PageAccessGroupsApi.md#delete_pages_page_id_page_access_groups_page_access_group_id) | **DELETE** /pages/{page_id}/page_access_groups/{page_access_group_id} | Remove a page access group
*PageAccessGroupsApi* | [**get_pages_page_id_page_access_groups**](docs/PageAccessGroupsApi.md#get_pages_page_id_page_access_groups) | **GET** /pages/{page_id}/page_access_groups | Get a list of page access groups
*PageAccessGroupsApi* | [**get_pages_page_id_page_access_groups_page_access_group_id**](docs/PageAccessGroupsApi.md#get_pages_page_id_page_access_groups_page_access_group_id) | **GET** /pages/{page_id}/page_access_groups/{page_access_group_id} | Get a page access group
*PageAccessGroupsApi* | [**patch_pages_page_id_page_access_groups_page_access_group_id**](docs/PageAccessGroupsApi.md#patch_pages_page_id_page_access_groups_page_access_group_id) | **PATCH** /pages/{page_id}/page_access_groups/{page_access_group_id} | Update a page access group
*PageAccessGroupsApi* | [**post_pages_page_id_page_access_groups**](docs/PageAccessGroupsApi.md#post_pages_page_id_page_access_groups) | **POST** /pages/{page_id}/page_access_groups | Create a page access group
*PageAccessGroupsApi* | [**put_pages_page_id_page_access_groups_page_access_group_id**](docs/PageAccessGroupsApi.md#put_pages_page_id_page_access_groups_page_access_group_id) | **PUT** /pages/{page_id}/page_access_groups/{page_access_group_id} | Update a page access group
*PageAccessUserComponentsApi* | [**delete_pages_page_id_page_access_users_page_access_user_id_components**](docs/PageAccessUserComponentsApi.md#delete_pages_page_id_page_access_users_page_access_user_id_components) | **DELETE** /pages/{page_id}/page_access_users/{page_access_user_id}/components | Remove components for page access user
*PageAccessUserComponentsApi* | [**delete_pages_page_id_page_access_users_page_access_user_id_components_component_id**](docs/PageAccessUserComponentsApi.md#delete_pages_page_id_page_access_users_page_access_user_id_components_component_id) | **DELETE** /pages/{page_id}/page_access_users/{page_access_user_id}/components/{component_id} | Remove component for page access user
*PageAccessUserComponentsApi* | [**get_pages_page_id_page_access_users_page_access_user_id_components**](docs/PageAccessUserComponentsApi.md#get_pages_page_id_page_access_users_page_access_user_id_components) | **GET** /pages/{page_id}/page_access_users/{page_access_user_id}/components | Get components for page access user
*PageAccessUserComponentsApi* | [**patch_pages_page_id_page_access_users_page_access_user_id_components**](docs/PageAccessUserComponentsApi.md#patch_pages_page_id_page_access_users_page_access_user_id_components) | **PATCH** /pages/{page_id}/page_access_users/{page_access_user_id}/components | Add components for page access user
*PageAccessUserComponentsApi* | [**post_pages_page_id_page_access_users_page_access_user_id_components**](docs/PageAccessUserComponentsApi.md#post_pages_page_id_page_access_users_page_access_user_id_components) | **POST** /pages/{page_id}/page_access_users/{page_access_user_id}/components | Replace components for page access user
*PageAccessUserComponentsApi* | [**put_pages_page_id_page_access_users_page_access_user_id_components**](docs/PageAccessUserComponentsApi.md#put_pages_page_id_page_access_users_page_access_user_id_components) | **PUT** /pages/{page_id}/page_access_users/{page_access_user_id}/components | Add components for page access user
*PageAccessUserMetricsApi* | [**delete_pages_page_id_page_access_users_page_access_user_id_metrics**](docs/PageAccessUserMetricsApi.md#delete_pages_page_id_page_access_users_page_access_user_id_metrics) | **DELETE** /pages/{page_id}/page_access_users/{page_access_user_id}/metrics | Delete metrics for page access user
*PageAccessUserMetricsApi* | [**delete_pages_page_id_page_access_users_page_access_user_id_metrics_metric_id**](docs/PageAccessUserMetricsApi.md#delete_pages_page_id_page_access_users_page_access_user_id_metrics_metric_id) | **DELETE** /pages/{page_id}/page_access_users/{page_access_user_id}/metrics/{metric_id} | Delete metric for page access user
*PageAccessUserMetricsApi* | [**get_pages_page_id_page_access_users_page_access_user_id_metrics**](docs/PageAccessUserMetricsApi.md#get_pages_page_id_page_access_users_page_access_user_id_metrics) | **GET** /pages/{page_id}/page_access_users/{page_access_user_id}/metrics | Get metrics for page access user
*PageAccessUserMetricsApi* | [**patch_pages_page_id_page_access_users_page_access_user_id_metrics**](docs/PageAccessUserMetricsApi.md#patch_pages_page_id_page_access_users_page_access_user_id_metrics) | **PATCH** /pages/{page_id}/page_access_users/{page_access_user_id}/metrics | Add metrics for page access user
*PageAccessUserMetricsApi* | [**post_pages_page_id_page_access_users_page_access_user_id_metrics**](docs/PageAccessUserMetricsApi.md#post_pages_page_id_page_access_users_page_access_user_id_metrics) | **POST** /pages/{page_id}/page_access_users/{page_access_user_id}/metrics | Replace metrics for page access user
*PageAccessUserMetricsApi* | [**put_pages_page_id_page_access_users_page_access_user_id_metrics**](docs/PageAccessUserMetricsApi.md#put_pages_page_id_page_access_users_page_access_user_id_metrics) | **PUT** /pages/{page_id}/page_access_users/{page_access_user_id}/metrics | Add metrics for page access user
*PageAccessUsersApi* | [**delete_pages_page_id_page_access_users_page_access_user_id**](docs/PageAccessUsersApi.md#delete_pages_page_id_page_access_users_page_access_user_id) | **DELETE** /pages/{page_id}/page_access_users/{page_access_user_id} | Delete page access user
*PageAccessUsersApi* | [**get_pages_page_id_page_access_users**](docs/PageAccessUsersApi.md#get_pages_page_id_page_access_users) | **GET** /pages/{page_id}/page_access_users | Get a list of page access users
*PageAccessUsersApi* | [**get_pages_page_id_page_access_users_page_access_user_id**](docs/PageAccessUsersApi.md#get_pages_page_id_page_access_users_page_access_user_id) | **GET** /pages/{page_id}/page_access_users/{page_access_user_id} | Get page access user
*PageAccessUsersApi* | [**patch_pages_page_id_page_access_users_page_access_user_id**](docs/PageAccessUsersApi.md#patch_pages_page_id_page_access_users_page_access_user_id) | **PATCH** /pages/{page_id}/page_access_users/{page_access_user_id} | Update page access user
*PageAccessUsersApi* | [**post_pages_page_id_page_access_users**](docs/PageAccessUsersApi.md#post_pages_page_id_page_access_users) | **POST** /pages/{page_id}/page_access_users | Add a page access user
*PageAccessUsersApi* | [**put_pages_page_id_page_access_users_page_access_user_id**](docs/PageAccessUsersApi.md#put_pages_page_id_page_access_users_page_access_user_id) | **PUT** /pages/{page_id}/page_access_users/{page_access_user_id} | Update page access user
*PagesApi* | [**get_pages**](docs/PagesApi.md#get_pages) | **GET** /pages | Get a list of pages
*PagesApi* | [**get_pages_page_id**](docs/PagesApi.md#get_pages_page_id) | **GET** /pages/{page_id} | Get a page
*PagesApi* | [**patch_pages_page_id**](docs/PagesApi.md#patch_pages_page_id) | **PATCH** /pages/{page_id} | Update a page
*PagesApi* | [**put_pages_page_id**](docs/PagesApi.md#put_pages_page_id) | **PUT** /pages/{page_id} | Update a page
*PermissionsApi* | [**get_organizations_organization_id_permissions_user_id**](docs/PermissionsApi.md#get_organizations_organization_id_permissions_user_id) | **GET** /organizations/{organization_id}/permissions/{user_id} | Get a user&#x27;s permissions
*PermissionsApi* | [**put_organizations_organization_id_permissions_user_id**](docs/PermissionsApi.md#put_organizations_organization_id_permissions_user_id) | **PUT** /organizations/{organization_id}/permissions/{user_id} | Update a user&#x27;s role permissions
*StatusEmbedConfigApi* | [**get_pages_page_id_status_embed_config**](docs/StatusEmbedConfigApi.md#get_pages_page_id_status_embed_config) | **GET** /pages/{page_id}/status_embed_config | Get status embed config settings
*StatusEmbedConfigApi* | [**patch_pages_page_id_status_embed_config**](docs/StatusEmbedConfigApi.md#patch_pages_page_id_status_embed_config) | **PATCH** /pages/{page_id}/status_embed_config | Update status embed config settings
*StatusEmbedConfigApi* | [**put_pages_page_id_status_embed_config**](docs/StatusEmbedConfigApi.md#put_pages_page_id_status_embed_config) | **PUT** /pages/{page_id}/status_embed_config | Update status embed config settings
*SubscribersApi* | [**delete_pages_page_id_subscribers_subscriber_id**](docs/SubscribersApi.md#delete_pages_page_id_subscribers_subscriber_id) | **DELETE** /pages/{page_id}/subscribers/{subscriber_id} | Unsubscribe a subscriber
*SubscribersApi* | [**get_pages_page_id_subscribers**](docs/SubscribersApi.md#get_pages_page_id_subscribers) | **GET** /pages/{page_id}/subscribers | Get a list of subscribers
*SubscribersApi* | [**get_pages_page_id_subscribers_count**](docs/SubscribersApi.md#get_pages_page_id_subscribers_count) | **GET** /pages/{page_id}/subscribers/count | Get a count of subscribers by type
*SubscribersApi* | [**get_pages_page_id_subscribers_histogram_by_state**](docs/SubscribersApi.md#get_pages_page_id_subscribers_histogram_by_state) | **GET** /pages/{page_id}/subscribers/histogram_by_state | Get a histogram of subscribers by type and then state
*SubscribersApi* | [**get_pages_page_id_subscribers_subscriber_id**](docs/SubscribersApi.md#get_pages_page_id_subscribers_subscriber_id) | **GET** /pages/{page_id}/subscribers/{subscriber_id} | Get a subscriber
*SubscribersApi* | [**get_pages_page_id_subscribers_unsubscribed**](docs/SubscribersApi.md#get_pages_page_id_subscribers_unsubscribed) | **GET** /pages/{page_id}/subscribers/unsubscribed | Get a list of unsubscribed subscribers
*SubscribersApi* | [**patch_pages_page_id_subscribers_subscriber_id**](docs/SubscribersApi.md#patch_pages_page_id_subscribers_subscriber_id) | **PATCH** /pages/{page_id}/subscribers/{subscriber_id} | Update a subscriber
*SubscribersApi* | [**post_pages_page_id_subscribers**](docs/SubscribersApi.md#post_pages_page_id_subscribers) | **POST** /pages/{page_id}/subscribers | Create a subscriber
*SubscribersApi* | [**post_pages_page_id_subscribers_reactivate**](docs/SubscribersApi.md#post_pages_page_id_subscribers_reactivate) | **POST** /pages/{page_id}/subscribers/reactivate | Reactivate a list of subscribers
*SubscribersApi* | [**post_pages_page_id_subscribers_resend_confirmation**](docs/SubscribersApi.md#post_pages_page_id_subscribers_resend_confirmation) | **POST** /pages/{page_id}/subscribers/resend_confirmation | Resend confirmations to a list of subscribers
*SubscribersApi* | [**post_pages_page_id_subscribers_subscriber_id_resend_confirmation**](docs/SubscribersApi.md#post_pages_page_id_subscribers_subscriber_id_resend_confirmation) | **POST** /pages/{page_id}/subscribers/{subscriber_id}/resend_confirmation | Resend confirmation to a subscriber
*SubscribersApi* | [**post_pages_page_id_subscribers_unsubscribe**](docs/SubscribersApi.md#post_pages_page_id_subscribers_unsubscribe) | **POST** /pages/{page_id}/subscribers/unsubscribe | Unsubscribe a list of subscribers
*TemplatesApi* | [**get_pages_page_id_incident_templates**](docs/TemplatesApi.md#get_pages_page_id_incident_templates) | **GET** /pages/{page_id}/incident_templates | Get a list of templates
*TemplatesApi* | [**post_pages_page_id_incident_templates**](docs/TemplatesApi.md#post_pages_page_id_incident_templates) | **POST** /pages/{page_id}/incident_templates | Create a template
*UsersApi* | [**delete_organizations_organization_id_users_user_id**](docs/UsersApi.md#delete_organizations_organization_id_users_user_id) | **DELETE** /organizations/{organization_id}/users/{user_id} | Delete a user
*UsersApi* | [**get_organizations_organization_id_permissions_user_id**](docs/UsersApi.md#get_organizations_organization_id_permissions_user_id) | **GET** /organizations/{organization_id}/permissions/{user_id} | Get a user&#x27;s permissions
*UsersApi* | [**get_organizations_organization_id_users**](docs/UsersApi.md#get_organizations_organization_id_users) | **GET** /organizations/{organization_id}/users | Get a list of users
*UsersApi* | [**post_organizations_organization_id_users**](docs/UsersApi.md#post_organizations_organization_id_users) | **POST** /organizations/{organization_id}/users | Create a user

## Documentation For Models

 - [Component](docs/Component.md)
 - [ComponentGroupUptime](docs/ComponentGroupUptime.md)
 - [ComponentGroupUptimeRelatedEvents](docs/ComponentGroupUptimeRelatedEvents.md)
 - [ComponentIdPageAccessUsersBody](docs/ComponentIdPageAccessUsersBody.md)
 - [ComponentUptime](docs/ComponentUptime.md)
 - [ComponentUptimeRelatedEvents](docs/ComponentUptimeRelatedEvents.md)
 - [DeletePagesPageIdPageAccessGroupsPageAccessGroupIdComponents](docs/DeletePagesPageIdPageAccessGroupsPageAccessGroupIdComponents.md)
 - [DeletePagesPageIdPageAccessUsersPageAccessUserIdComponents](docs/DeletePagesPageIdPageAccessUsersPageAccessUserIdComponents.md)
 - [DeletePagesPageIdPageAccessUsersPageAccessUserIdMetrics](docs/DeletePagesPageIdPageAccessUsersPageAccessUserIdMetrics.md)
 - [ErrorEntity](docs/ErrorEntity.md)
 - [GroupComponent](docs/GroupComponent.md)
 - [Incident](docs/Incident.md)
 - [IncidentTemplate](docs/IncidentTemplate.md)
 - [IncidentUpdate](docs/IncidentUpdate.md)
 - [Metric](docs/Metric.md)
 - [MetricAddResponse](docs/MetricAddResponse.md)
 - [MetricAddResponseMetricId](docs/MetricAddResponseMetricId.md)
 - [MetricsProvider](docs/MetricsProvider.md)
 - [Page](docs/Page.md)
 - [PageAccessGroup](docs/PageAccessGroup.md)
 - [PageAccessUser](docs/PageAccessUser.md)
 - [PatchPages](docs/PatchPages.md)
 - [PatchPagesPage](docs/PatchPagesPage.md)
 - [PatchPagesPageIdComponentGroups](docs/PatchPagesPageIdComponentGroups.md)
 - [PatchPagesPageIdComponents](docs/PatchPagesPageIdComponents.md)
 - [PatchPagesPageIdIncidents](docs/PatchPagesPageIdIncidents.md)
 - [PatchPagesPageIdIncidentsIncident](docs/PatchPagesPageIdIncidentsIncident.md)
 - [PatchPagesPageIdIncidentsIncidentComponents](docs/PatchPagesPageIdIncidentsIncidentComponents.md)
 - [PatchPagesPageIdIncidentsIncidentIdIncidentUpdates](docs/PatchPagesPageIdIncidentsIncidentIdIncidentUpdates.md)
 - [PatchPagesPageIdIncidentsIncidentIdIncidentUpdatesIncidentUpdate](docs/PatchPagesPageIdIncidentsIncidentIdIncidentUpdatesIncidentUpdate.md)
 - [PatchPagesPageIdMetrics](docs/PatchPagesPageIdMetrics.md)
 - [PatchPagesPageIdMetricsMetric](docs/PatchPagesPageIdMetricsMetric.md)
 - [PatchPagesPageIdMetricsProviders](docs/PatchPagesPageIdMetricsProviders.md)
 - [PatchPagesPageIdMetricsProvidersMetricsProvider](docs/PatchPagesPageIdMetricsProvidersMetricsProvider.md)
 - [PatchPagesPageIdPageAccessGroups](docs/PatchPagesPageIdPageAccessGroups.md)
 - [PatchPagesPageIdPageAccessGroupsPageAccessGroupIdComponents](docs/PatchPagesPageIdPageAccessGroupsPageAccessGroupIdComponents.md)
 - [PatchPagesPageIdPageAccessUsersPageAccessUserIdComponents](docs/PatchPagesPageIdPageAccessUsersPageAccessUserIdComponents.md)
 - [PatchPagesPageIdPageAccessUsersPageAccessUserIdMetrics](docs/PatchPagesPageIdPageAccessUsersPageAccessUserIdMetrics.md)
 - [PatchPagesPageIdStatusEmbedConfig](docs/PatchPagesPageIdStatusEmbedConfig.md)
 - [PatchPagesPageIdStatusEmbedConfigStatusEmbedConfig](docs/PatchPagesPageIdStatusEmbedConfigStatusEmbedConfig.md)
 - [PatchPagesPageIdSubscribers](docs/PatchPagesPageIdSubscribers.md)
 - [Permissions](docs/Permissions.md)
 - [PermissionsData](docs/PermissionsData.md)
 - [PermissionsDataPages](docs/PermissionsDataPages.md)
 - [PostOrganizationsOrganizationIdUsers](docs/PostOrganizationsOrganizationIdUsers.md)
 - [PostOrganizationsOrganizationIdUsersUser](docs/PostOrganizationsOrganizationIdUsersUser.md)
 - [PostPagesPageIdComponentGroups](docs/PostPagesPageIdComponentGroups.md)
 - [PostPagesPageIdComponentGroupsComponentGroup](docs/PostPagesPageIdComponentGroupsComponentGroup.md)
 - [PostPagesPageIdComponents](docs/PostPagesPageIdComponents.md)
 - [PostPagesPageIdComponentsComponent](docs/PostPagesPageIdComponentsComponent.md)
 - [PostPagesPageIdIncidentTemplates](docs/PostPagesPageIdIncidentTemplates.md)
 - [PostPagesPageIdIncidentTemplatesTemplate](docs/PostPagesPageIdIncidentTemplatesTemplate.md)
 - [PostPagesPageIdIncidents](docs/PostPagesPageIdIncidents.md)
 - [PostPagesPageIdIncidentsIncident](docs/PostPagesPageIdIncidentsIncident.md)
 - [PostPagesPageIdIncidentsIncidentComponents](docs/PostPagesPageIdIncidentsIncidentComponents.md)
 - [PostPagesPageIdIncidentsIncidentIdSubscribers](docs/PostPagesPageIdIncidentsIncidentIdSubscribers.md)
 - [PostPagesPageIdIncidentsIncidentIdSubscribersSubscriber](docs/PostPagesPageIdIncidentsIncidentIdSubscribersSubscriber.md)
 - [PostPagesPageIdMetricsData](docs/PostPagesPageIdMetricsData.md)
 - [PostPagesPageIdMetricsMetricIdData](docs/PostPagesPageIdMetricsMetricIdData.md)
 - [PostPagesPageIdMetricsMetricIdDataData](docs/PostPagesPageIdMetricsMetricIdDataData.md)
 - [PostPagesPageIdMetricsProviders](docs/PostPagesPageIdMetricsProviders.md)
 - [PostPagesPageIdMetricsProvidersMetricsProvider](docs/PostPagesPageIdMetricsProvidersMetricsProvider.md)
 - [PostPagesPageIdMetricsProvidersMetricsProviderIdMetrics](docs/PostPagesPageIdMetricsProvidersMetricsProviderIdMetrics.md)
 - [PostPagesPageIdMetricsProvidersMetricsProviderIdMetricsMetric](docs/PostPagesPageIdMetricsProvidersMetricsProviderIdMetricsMetric.md)
 - [PostPagesPageIdPageAccessGroups](docs/PostPagesPageIdPageAccessGroups.md)
 - [PostPagesPageIdPageAccessGroupsPageAccessGroup](docs/PostPagesPageIdPageAccessGroupsPageAccessGroup.md)
 - [PostPagesPageIdPageAccessGroupsPageAccessGroupIdComponents](docs/PostPagesPageIdPageAccessGroupsPageAccessGroupIdComponents.md)
 - [PostPagesPageIdPageAccessUsers](docs/PostPagesPageIdPageAccessUsers.md)
 - [PostPagesPageIdPageAccessUsersPageAccessUser](docs/PostPagesPageIdPageAccessUsersPageAccessUser.md)
 - [PostPagesPageIdPageAccessUsersPageAccessUserIdComponents](docs/PostPagesPageIdPageAccessUsersPageAccessUserIdComponents.md)
 - [PostPagesPageIdPageAccessUsersPageAccessUserIdMetrics](docs/PostPagesPageIdPageAccessUsersPageAccessUserIdMetrics.md)
 - [PostPagesPageIdSubscribers](docs/PostPagesPageIdSubscribers.md)
 - [PostPagesPageIdSubscribersReactivate](docs/PostPagesPageIdSubscribersReactivate.md)
 - [PostPagesPageIdSubscribersResendConfirmation](docs/PostPagesPageIdSubscribersResendConfirmation.md)
 - [PostPagesPageIdSubscribersSubscriber](docs/PostPagesPageIdSubscribersSubscriber.md)
 - [PostPagesPageIdSubscribersUnsubscribe](docs/PostPagesPageIdSubscribersUnsubscribe.md)
 - [Postmortem](docs/Postmortem.md)
 - [PutOrganizationsOrganizationIdPermissions](docs/PutOrganizationsOrganizationIdPermissions.md)
 - [PutOrganizationsOrganizationIdPermissionsPages](docs/PutOrganizationsOrganizationIdPermissionsPages.md)
 - [PutOrganizationsOrganizationIdPermissionsPagesPageId](docs/PutOrganizationsOrganizationIdPermissionsPagesPageId.md)
 - [PutPages](docs/PutPages.md)
 - [PutPagesPageIdComponentGroups](docs/PutPagesPageIdComponentGroups.md)
 - [PutPagesPageIdComponents](docs/PutPagesPageIdComponents.md)
 - [PutPagesPageIdIncidents](docs/PutPagesPageIdIncidents.md)
 - [PutPagesPageIdIncidentsIncidentIdIncidentUpdates](docs/PutPagesPageIdIncidentsIncidentIdIncidentUpdates.md)
 - [PutPagesPageIdIncidentsIncidentIdPostmortem](docs/PutPagesPageIdIncidentsIncidentIdPostmortem.md)
 - [PutPagesPageIdIncidentsIncidentIdPostmortemPostmortem](docs/PutPagesPageIdIncidentsIncidentIdPostmortemPostmortem.md)
 - [PutPagesPageIdIncidentsIncidentIdPostmortemPublish](docs/PutPagesPageIdIncidentsIncidentIdPostmortemPublish.md)
 - [PutPagesPageIdIncidentsIncidentIdPostmortemPublishPostmortem](docs/PutPagesPageIdIncidentsIncidentIdPostmortemPublishPostmortem.md)
 - [PutPagesPageIdMetrics](docs/PutPagesPageIdMetrics.md)
 - [PutPagesPageIdMetricsProviders](docs/PutPagesPageIdMetricsProviders.md)
 - [PutPagesPageIdPageAccessGroups](docs/PutPagesPageIdPageAccessGroups.md)
 - [PutPagesPageIdPageAccessGroupsPageAccessGroupIdComponents](docs/PutPagesPageIdPageAccessGroupsPageAccessGroupIdComponents.md)
 - [PutPagesPageIdPageAccessUsersPageAccessUserIdComponents](docs/PutPagesPageIdPageAccessUsersPageAccessUserIdComponents.md)
 - [PutPagesPageIdPageAccessUsersPageAccessUserIdMetrics](docs/PutPagesPageIdPageAccessUsersPageAccessUserIdMetrics.md)
 - [PutPagesPageIdStatusEmbedConfig](docs/PutPagesPageIdStatusEmbedConfig.md)
 - [SingleMetricAddResponse](docs/SingleMetricAddResponse.md)
 - [StatusEmbedConfig](docs/StatusEmbedConfig.md)
 - [Subscriber](docs/Subscriber.md)
 - [SubscriberCountByState](docs/SubscriberCountByState.md)
 - [SubscriberCountByType](docs/SubscriberCountByType.md)
 - [SubscriberCountByTypeAndState](docs/SubscriberCountByTypeAndState.md)
 - [User](docs/User.md)

## Documentation For Authorization


## api_key

- **Type**: API key
- **API key parameter name**: Authorization
- **Location**: HTTP header


## Author
spkishore007@guidewire.com

