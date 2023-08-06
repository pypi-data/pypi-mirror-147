"""
Generic update contents for documents with a field containing content regions.

In some cases a fixed layout is preferable to the more flexible flow layout,
or you may wish to allow users to update more than one field within a document
via the in-page editor. This generic view is designed to provide a basis for
such cases (it's also possible to combine both flow and region based update
views).

Image syncing is only supported against the `content_regions_field`, assets
are stored within the regions field under the special `__assets__` key.

: `content_regions_field`
    The field within the document that contains the content flows (defaults to
    'flows').

"""

import json
import re

from bs4 import BeautifulSoup
import flask
from manhattan.chains import Chain, ChainMgr
from manhattan.content.snippets import Region
from manhattan.content.views import factories
from manhattan.manage.views import utils as manage_utils
from manhattan.manage.views import factories as manage_factories
from mongoframes import Q
from .utils import sync_image_fixtures, sync_images, sync_picture_fixtures

__all__ = ['update_contents_chains']


# Define the chains
update_contents_chains = ChainMgr()

update_contents_chains['post'] = Chain([
    'config',
    'authenticate',
    'get_document',
    'get_contents',
    'get_regions',
    'sync_imagery',
    'update_document',
    'render_json'
])


# Define the links

update_contents_chains.set_link(
    manage_factories.config(content_regions_field='regions')
)
update_contents_chains.set_link(manage_factories.authenticate())
update_contents_chains.set_link(manage_factories.get_document())
update_contents_chains.set_link(factories.get_contents())

@update_contents_chains.link
def get_regions(state):
    """
    Get copies of the regions within the document we'll be updating.

    This link adds the `regions` key to the state, which contains a dictionary
    of existing regions contents.
    """

    # Get the document we're add the snippet to
    document = state[state.manage_config.var_name]

    # Ensure there's a table to get/set contents against
    assert state.content_regions_field, 'No `content_regions_field` configured'
    regions = document.get(state.content_regions_field) or {}
    setattr(document, state.content_regions_field, regions)
    state.regions = regions.copy()

    # Ensure there's a base region and assets table for each of the content
    # updates.
    for region_name, content in state.contents.items():
        assets = {}
        if region_name in state.regions:
            assets = state.regions.get('assets', {})
        state.regions[region_name] = Region(
            assets=assets,
            content=content
        )

@update_contents_chains.link
def sync_imagery(state):
    """
    Temporary and permenant images inserted into the contents must be
    synchronized, by which we mean that temporary assets are converted to
    permenant assets and the content variation of the image is resized to
    match the width/height.
    """

    # Get the document we're add the snippet to
    document = state[state.manage_config.var_name]

    asset_mgr = flask.current_app.asset_mgr
    config = flask.current_app.config
    variation_name = config.get('CONTENT_VARIATION_NAME', 'image')

    # Update the images
    for region, content in state.contents.items():

        # Parse the content of the region
        soup = BeautifulSoup(content, 'lxml')

        # Find any element within the content that relates to an asset
        sync_images(state.regions[region], soup)
        sync_image_fixtures(state.regions[region], soup)
        sync_picture_fixtures(state.regions[region], soup)

        # Save the content of the region back to the snippet
        soup.html.unwrap()
        soup.body.unwrap()
        state.regions[region].content = str(soup)

@update_contents_chains.link
def update_document(state):
    """Update documents contents"""

    # Get the document we're updating the contents of
    document = state[state.manage_config.var_name]

    # Update the document
    document.logged_update(
        state.manage_user,
        {state.content_regions_field: state.regions}
    )

@update_contents_chains.link
def render_json(state):
    """Render a JSON response for the successful saving of content"""
    return manage_utils.json_success()
