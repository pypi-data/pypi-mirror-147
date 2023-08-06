import json

from ..HTTP import Requests
from datetime import datetime


class hubspot:

  expires_at = None
  access_token = None
  auth_refreshed = False
  headers = {"Content-Type": "application/json", "Accept": "application/json"}
  auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
  base_url = "https://api.hubapi.com/"

  def __init__(
      self,
      access_token=None,
      expires_at=0,
      client_id=None,
      client_secret=None,
      refresh_token=None
  ):
    self.headers['Authorization'] = f"Bearer {access_token}"
    self.expires_at = expires_at
    self.access_token = access_token
    self.refresh_token = refresh_token
    self.auth_refreshed = False
    if client_id is None:
      raise Exception("Client ID must be provided")
    if client_secret is None:
      raise Exception("Client secret must be provided")

    if datetime.now().timestamp() > expires_at:
      self.authenticate(client_id, client_secret, refresh_token)
      self.auth_refreshed = True

  def authenticate(self, client_id, client_secret, refresh_token):
    post_url = f"{self.base_url}oauth/v1/token"
    auth_body = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    result = Requests.post(post_url, self.auth_headers, auth_body)
    auth_result = result['content']
    self.access_token = auth_result['access_token']
    self.headers['Authorization'] = f"Bearer {auth_result['access_token']}"
    self.expires_at = datetime.now().timestamp() + int(auth_result['expires_in'])

  # Contains utilities for interacting with the HubSpot API
  def get_token_details(self):
    post_url = f"{self.base_url}oauth/v1/refresh-tokens/{self.refresh_token}"
    return Requests.get(post_url, self.headers)

  def revoke_token(self):
    post_url = f"{self.base_url}oauth/v1/refresh-tokens/{self.refresh_token}"
    return Requests.delete(post_url, self.auth_headers)

  def custom_request(self, method=None, endpoint=None, **kwargs):
    endpoint = endpoint.lstrip('/')
    post_url = f"{self.base_url}{endpoint}"
    return getattr(Requests, method)(post_url, self.headers, **kwargs)

  def search_records_by_property_value(self, object_type, property_name, property_value, property_names=None, after=None, sorts=[]):
    filters = [
        {
            'propertyName': property_name,
            'operator': 'EQ',
            'value': property_value
        }
    ]
    return self.search_records(object_type, property_names, filters, after, sorts)

  def search_records_by_property_known(self, object_type, property_name, property_names, after=None, sorts=[]):
    filters = [
        {
            'propertyName': property_name,
            'operator': 'HAS_PROPERTY'
        }
    ]
    return self.search_records(object_type, property_names, filters, after, sorts)

  def search_records_by_property_less_than(self, object_type, property_name, property_value, property_names, after=None, sorts=[]):
    filters = [
        {
            'propertyName': property_name,
            'operator': 'LT',
            'value': property_value
        }
    ]
    return self.search_records(object_type, property_names, filters, after, sorts)

  def search_records_by_property_greater_than(self, object_type, property_name, property_value, property_names, after=None, sorts=[]):
    filters = [
        {
            'propertyName': property_name,
            'operator': 'GT',
            'value': property_value
        }
    ]
    return self.search_records(object_type, property_names, filters, after, sorts)

  def search_records_by_property_values(self, object_type, property_name, property_values, property_names, after=None, sorts=[]):
    filters = [
        {
            'propertyName': property_name,
            'operator': 'IN',
            'values': property_values
        }
    ]
    return self.search_records(object_type, property_names, filters, after, sorts)

  def search_records(self, object_type, property_names, filters, after=None, sorts=[]):
    post_url = f"{self.base_url}crm/v3/objects/{object_type}/search"
    post_body = {
        'filterGroups': [
            {
                'filters': filters
            }
        ],
        'sorts': sorts,
        'properties': property_names,
        'limit': 100
    }
    if after:
      post_body['after'] = after
    result = Requests.post(post_url, self.headers, json.dumps(post_body))
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to search {object_type}. Result: {result}")
    return result

  def create_record(self, object_type, properties):
    post_url = f"{self.base_url}crm/v3/objects/{object_type}"
    post_body = {
        'properties': properties
    }
    result = Requests.post(post_url, self.headers, json.dumps(post_body))
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to create {object_type}. Result: {result}")
    return result

  def update_record(self, object_id, object_type, properties):
    post_url = f"{self.base_url}crm/v3/objects/{object_type}/{object_id}?"
    post_body = {
        'properties': properties
    }
    result = Requests.patch(post_url, self.headers, json.dumps(post_body))
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to update {object_type}. Result: {result}")
    return result

  def read_records_batch(self, object_type, properties, inputs, id_property=None):
    post_url = f"{self.base_url}crm/v3/objects/{object_type}/batch/read"
    post_body = {
        'properties': properties,
        'inputs': inputs
    }
    if id_property is not None:
      post_body['idProperty'] = id_property
    result = Requests.post(post_url, self.headers, json.dumps(post_body))
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to read {object_type}. Result: {result}")
    return result

  def get_record(self, object_type, object_id, property_names=None, associations=None):
    post_url = f"{self.base_url}crm/v3/objects/{object_type}/{object_id}?archived=false"
    if property_names:
      post_url = f"{post_url}&properties={'%2C'.join(property_names)}"

    if associations:
      post_url = f"{post_url}&associations={'%2C'.join(associations)}"
    result = Requests.get(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to retrieve {object_type}. Result: {result}")
    return result

  def get_records(self, object_type, object_id, property_names=None, associations=None, after=None):
    post_url = f"{self.base_url}crm/v3/objects/{object_type}/{object_id}?archived=false"
    if property_names:
      post_url = f"{post_url}&properties={'%2C'.join(property_names)}"
    if after is not None:
      post_url = f"{post_url}&after={after}"
    if associations:
      post_url = f"{post_url}&associations={'%2C'.join(associations)}"
    result = Requests.get(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to retrieve {object_type}. Result: {result}")
    return result

  def create_records_batch(self, object_type, records):
    post_url = f"{self.base_url}crm/v3/objects/{object_type}/batch/create"
    post_body = {
        'inputs': records
    }
    result = Requests.post(post_url, self.headers, json.dumps(post_body))
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to create {object_type}. Result: {result}")
    return result

  def update_records_batch(self, object_type, records):
    post_url = f"{self.base_url}crm/v3/objects/{object_type}/batch/update"
    post_body = {
        'inputs': records
    }
    result = Requests.post(post_url, self.headers, json.dumps(post_body))
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to update {object_type}. Result: {result}")
    return result

  def delete_record(self, object_type, object_id):
    post_url = f"{self.base_url}crm/v3/objects/{object_type}/{object_id}"
    result = Requests.delete(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to delete {object_type}. Result: {result}")
    return result

  def get_properties(self, object_type):
    post_url = f"{self.base_url}crm/v3/properties/{object_type}?archived=false"
    result = Requests.get(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to get properties. Result: {result}")
    return result

  def get_property(self, object_type, property_name):
    post_url = f"{self.base_url}crm/v3/properties/{object_type}/{property_name}?archived=false"
    result = Requests.get(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to get property. Result: {result}")
    return result

  def update_property(self, object_type, property_name, data):
    post_url = f"{self.base_url}crm/v3/properties/{object_type}/{property_name}"
    acceptable_keys = [
        'groupName',
        'hidden',
        'displayOrder',
        'options',
        'label',
        'type',
        'fieldType',
        'formField'
    ]
    data = {k: v for k, v in data.items() if k in acceptable_keys}
    result = Requests.patch(post_url, self.headers, payload=json.dumps(data))
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to update property. Result: {result}")
    return result

  def unsubscribe_from_all(self, contact_email):
    post_url = f"{self.base_url}email/public/v1/subscriptions/{contact_email}"
    post_body = {
        'unsubscribeFromAll': True
    }
    result = Requests.put(post_url, self.headers, json.dumps(post_body))
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to unsubscribe contact. Result: {result}")
    return result

  def get_owner(self, owner_id):
    post_url = f"{self.base_url}crm/v3/owners/{owner_id}"
    result = Requests.get(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to retrieve owner. Result: {result}")
    return result

  def search_owners(self, email=None, limit=100, after=None):
    post_url = f"{self.base_url}crm/v3/owners?limit={limit}"
    if email is not None:
      post_url = f"{post_url}&email={email}"
    if after is not None:
      post_url = f"{post_url}&after={after}"
    result = Requests.get(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to search owners. Result: {result}")
    return result

  def get_associations(self, from_object_type, to_object_type, from_object_id):
    post_url = f"{self.base_url}crm/v3/associations/{from_object_type}/{to_object_type}/batch/read"
    post_body = {
        'inputs': [
            {
                'id': from_object_id
            }
        ]
    }
    result = Requests.post(post_url, self.headers, json.dumps(post_body))
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to retrieve associations. Result: {result}")
    return result

  def set_parent_company(self, company_id, parent_company_id):
    post_url = f"{self.base_url}crm/v3/objects/companies/{company_id}/associations/company/{parent_company_id}/CHILD_TO_PARENT_COMPANY"
    result = Requests.put(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to set parent company. Result: {result}")
    return result

  def set_child_company(self, company_id, child_company_id):
    post_url = f"{self.base_url}crm/v3/objects/companies/{company_id}/associations/company/{child_company_id}/PARENT_TO_CHILD_COMPANY"
    result = Requests.put(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to set child company. Result: {result}")
    return result

  def set_company_for_contact(self, contact_id, company_id):
    post_url = f"{self.base_url}crm/v3/objects/contacts/{contact_id}/associations/company/{company_id}/CONTACT_TO_COMPANY"
    result = Requests.put(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to set company for contact. Result: {result}")
    return result

  def set_company_for_deal(self, deal_id, company_id):
    post_url = f"{self.base_url}crm/v3/objects/deals/{deal_id}/associations/company/{company_id}/DEAL_TO_COMPANY"
    result = Requests.put(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to set company for deal. Result: {result}")
    return result

  def delete_company_from_deal(self, deal_id, company_id):
    post_url = f"{self.base_url}crm/v3/objects/deals/{deal_id}/associations/company/{company_id}/DEAL_TO_COMPANY"
    result = Requests.delete(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to delete company from deal. Result: {result}")
    return result

  def set_contact_for_deal(self, deal_id, contact_id):
    post_url = f"{self.base_url}crm/v3/objects/deals/{deal_id}/associations/contact/{contact_id}/DEAL_TO_CONTACT"
    result = Requests.put(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to set contact for deal. Result: {result}")
    return result

  def set_deal_for_line_item(self, line_item_id, deal_id):
    post_url = f"{self.base_url}crm/v3/objects/line_items/{line_item_id}/associations/deals/{deal_id}/LINE_ITEM_TO_DEAL"
    result = Requests.put(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to set deal for line item. Result: {result}")
    return result

  def set_contact_for_meeting(self, meeting_id, contact_id):
    post_url = f"{self.base_url}crm/v3/objects/meetings/{meeting_id}/associations/contacts/{contact_id}/MEETING_EVENT_TO_CONTACT"
    result = Requests.put(post_url, self.headers)
    if not Requests.Utils.is_success(result['status_code']):
      raise Exception(f"Failed to set contact for meeting. Result: {result}")
    return result
