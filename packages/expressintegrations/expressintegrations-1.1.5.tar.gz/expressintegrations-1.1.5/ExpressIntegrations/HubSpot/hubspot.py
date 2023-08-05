from ..HTTP.Requests import *
from datetime import datetime

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
AUTH_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
BASE_URL = "https://api.hubapi.com/"


class hubspot:
  import json
  from . import associations
  from . import companies
  from . import contacts
  from . import deals
  from . import owners
  from . import products
  from . import lineitems

  expires_at = None
  access_token = None
  auth_refreshed = False

  def __init__(
      self,
      access_token=None,
      expires_at=0,
      client_id=None,
      client_secret=None,
      refresh_token=None
  ):
    HEADERS['Authorization'] = f"Bearer {access_token}"
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
    post_url = f"{BASE_URL}oauth/v1/token"
    auth_body = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    result = post(post_url, AUTH_HEADERS, auth_body)
    auth_result = result['content']
    self.access_token = auth_result['access_token']
    HEADERS['Authorization'] = f"Bearer {auth_result['access_token']}"
    self.expires_at = datetime.now().timestamp() + int(auth_result['expires_in'])

  # Contains utilities for interacting with the HubSpot API
  def get_token_details(self):
    post_url = f"{BASE_URL}oauth/v1/refresh-tokens/{self.refresh_token}"
    return get(post_url, HEADERS)

  def revoke_token(self):
    post_url = f"{BASE_URL}oauth/v1/refresh-tokens/{self.refresh_token}"
    return delete(post_url, AUTH_HEADERS)
