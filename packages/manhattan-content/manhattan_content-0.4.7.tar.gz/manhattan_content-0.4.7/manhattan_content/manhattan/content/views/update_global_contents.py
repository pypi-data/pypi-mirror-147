"""
Generic update global contents asset chain.

This view updates contents with the `GlobalRegion` collection.
"""

import json
import re

from bs4 import BeautifulSoup
import cssutils
import flask
from manhattan.chains import Chain, ChainMgr
from manhattan.content.snippets import GlobalRegion
from manhattan.content.views import factories
from manhattan.manage.views import utils as manage_utils
from manhattan.manage.views import factories as manage_factories
from mongoframes import Q
from .utils import sync_image_fixtures, sync_images, sync_picture_fixtures

__all__ = ['update_global_contents_chains']


# Define the chains
update_global_contents_chains = ChainMgr()

update_global_contents_chains['post'] = Chain([
    'config',
    'authenticate',
    'get_contents',
    'get_global_regions',
    'sync_imagery',
    'update_contents',
    'render_json'
])


# Define the links

update_global_contents_chains.set_link(manage_factories.config())
update_global_contents_chains.set_link(manage_factories.authenticate())
update_global_contents_chains.set_link(factories.get_contents())

@update_global_contents_chains.link
def get_global_regions(state):
    """
    Get the global regions that will be update based on the contents.

    This link adds the `global_regions` key to the state, which contains a
    dictionary of global regions to apply the update to, e.g
    `{region_name: instance}`.

    NOTE: If the contents contains a region name that doesn't exist a new
    region will be created.
    """

    # Build the table of global regions
    global_regions = {}
    for region_name, content in state.contents.items():

        # Attempt to find the named global region
        global_region = GlobalRegion.one(Q.name == region_name)

        # If there's no existing region with that name then add one
        if not global_region:
            global_region = GlobalRegion(name=region_name)
            global_region.logged_insert(state.manage_user)

        global_regions[region_name] = global_region

    # Add the global regions to the state
    state.global_regions = global_regions

@update_global_contents_chains.link
def sync_imagery(state):
    """
    Temporary and permenant images inserted into the contents must be
    synchronized, by which we mean that temporary assets are converted to
    permenant assets and the content variation of the image is resized to
    match the width/height.
    """

    asset_mgr = flask.current_app.asset_mgr
    config = flask.current_app.config
    variation_name = config.get('CONTENT_VARIATION_NAME', 'image')

    # Update the images
    for region, content in state.contents.items():

        # Parse the content of the region
        soup = BeautifulSoup(content, 'lxml')

        # Find any element within the content that relates to an asset
        sync_images(state.global_regions[region], soup)
        sync_image_fixtures(state.global_regions[region], soup)
        sync_picture_fixtures(state.global_regions[region], soup)

        # Save the content of the region back to the snippet
        soup.html.unwrap()
        soup.body.unwrap()
        state.global_regions[region].content = str(soup)

@update_global_contents_chains.link
def update_contents(state):
    """Update the contents of global regions within the contents"""
    for region_name, content in state.contents.items():
        state.global_regions[region_name].logged_update(
            state.manage_user,
            {
                'content': state.global_regions[region_name].content,
                'assets': state.global_regions[region_name].assets
            }
        )

@update_global_contents_chains.link
def render_json(state):
    """Render a JSON response for the successful saving of content"""
    return manage_utils.json_success()
