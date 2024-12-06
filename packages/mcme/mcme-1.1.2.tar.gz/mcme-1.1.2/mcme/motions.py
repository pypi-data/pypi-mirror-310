
import os
import tempfile

import click
from .helpers import Uploader
from .avatars import from_smpl
import requests
import openapi_client as client
from .logger import log
from openapi_client import PostgresqlBuildState as BuildState


class Motion():
    """Temporary motion"""
    def __init__(self,  prompt: str, api_instance: client.SearchMotionsApi) -> None:
        """Finding motion and downloading motion .smpl file as a temporary file"""
        motion_options = client.ServicesSearchMotionsOptions(
        num_motions=1,
        text=prompt)
        try:
            # Search for motion using prompt
            api_response = api_instance.submit_search_motions(motion_options)
        except Exception as e:
            raise click.ClickException("Exception when calling SearchMotionsApi->submit_search_motions: %s\n" % e) from e
        if api_response.data is None or api_response.data.attributes is None:
            raise click.ClickException("Searching for motion response came back empty")
        log.info(f"Creating motion from text finished with state {BuildState(api_response.data.attributes.state).name}")
        if api_response.included is None or \
            len(api_response.included) == 0 or \
            api_response.included[0] is None or \
            api_response.included[0].attributes is None or \
            api_response.included[0].attributes.url is None:
                raise click.ClickException("No motion found.")
        
        # Temporarily downloading motion .smpl file
        motion_download_url = api_response.included[0].attributes.url.path
        with tempfile.NamedTemporaryFile(delete=False, suffix='.smpl') as file:
            self.file = file.name
            try:
                stream = requests.get(motion_download_url, stream=True, timeout=60)
                stream.raise_for_status()
            except requests.exceptions.HTTPError as err:
                raise click.ClickException(str(err)) from err
            for chunk in stream.iter_content(chunk_size=1024 * 1024):
                file.write(chunk)
    
    def create_avatar(self, api_instance: client.AvatarsApi, uploader: Uploader, timeout: int) -> str:
        """"Creates avatar asset from motion .smpl file"""
        asset_id = from_smpl(self.file, api_instance, uploader, timeout)
        return asset_id

    def cleanup(self):
        """"Deleting temporary .smpl file containing the downloaded motion"""
        os.remove(self.file)
