"""
Generic update contents chain for content flows.

: `content_flows_field`
    The field within the document that contains the content flows (defaults to
    'flows').

"""

import logging
from copy import deepcopy
import json
import re

from bs4 import BeautifulSoup
import cssutils
import flask
from manhattan.assets import Asset
from manhattan.assets.transforms.base import BaseTransform
from manhattan.assets.transforms.images import Fit, Output
from manhattan.chains import Chain, ChainMgr
from manhattan.content.snippets import Snippet
from manhattan.content.views import factories
from manhattan.manage.views import utils as manage_utils
from manhattan.manage.views import factories as manage_factories
from .utils import sync_image_fixtures, sync_images, sync_picture_fixtures

cssutils.log.setLevel(logging.CRITICAL)


__all__ = ['update_flow_contents_chains']


# Define the chains
update_flow_contents_chains = ChainMgr()

update_flow_contents_chains['post'] = Chain([
    'config',
    'authenticate',
    'get_document',
    'get_flows',
    'get_contents',
    'sync_imagery',
    'update_contents',
    'update_flows',
    'render_json'
])


# Define the links

update_flow_contents_chains.set_link(
    manage_factories.config(content_flows_field='flows')
)
update_flow_contents_chains.set_link(manage_factories.authenticate())
update_flow_contents_chains.set_link(manage_factories.get_document())
update_flow_contents_chains.set_link(factories.get_contents())

@update_flow_contents_chains.link
def get_flows(state):
    """
    Get the flows that we're applying updates to.

    This link adds `flows` and `original_flows` keys to the state containing the
    flows that are to be updated.
    """

    # Get the document we're add the snippet to
    document = state[state.manage_config.var_name]

    # Get the flows we'll be updating
    state.flows = deepcopy(document.get(state.content_flows_field) or {})
    state.original_flows = deepcopy(state.flows)

    # Ensure all snippets in all flows are `Snippet` instances
    for flow_id, flow in state.flows.items():
        for i, snippet in enumerate(flow):
            if not isinstance(snippet, Snippet):
                flow[i] = Snippet(snippet)

@update_flow_contents_chains.link
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

    # Build a lookup table of all snippets with the page flows
    snippet_lookup = {}
    for flow_id, flow in state.flows.items():
        for snippet in flow:
            snippet_lookup[snippet.id] = snippet

    # Update the images
    for snippet_id, contents in state.contents.items():
        for region, content in contents.items():

            # Parse the content of the region
            soup = BeautifulSoup(content, 'lxml')

            # Find any element within the content that relates to an asset
            sync_images(snippet_lookup[snippet_id], soup)
            sync_image_fixtures(snippet_lookup[snippet_id], soup)
            sync_picture_fixtures(snippet_lookup[snippet_id], soup)

            # Save the content of the region back to the snippet
            soup.html.unwrap()
            soup.body.unwrap()
            contents[region] = str(soup)

@update_flow_contents_chains.link
def update_contents(state):
    """Update the contents of snippets with the flows"""

    # Apply the changes
    for flow_id, flow in state.flows.items():
        for snippet in flow:
            if snippet.id not in state.contents:
                continue

            if snippet.scope == 'local':
                # Apply changes to this snippet
                snippet.local_contents.update(state.contents[snippet.id])

            elif snippet.scope == 'global':
                # Apply changes to the global snippet this snippet references
                global_snippet = snippet.global_snippet

                # Update the contents
                global_contents = global_snippet.contents.copy()
                global_contents.update(state.contents[snippet.id])

                # Update the global snippet
                global_snippet.logged_update(
                    state.manage_user,
                    {'contents': global_contents}
                )

                # Clear global snippet cache from the snippet
                snippet._global_snippet_cache = None

@update_flow_contents_chains.link
def update_flows(state):
    """Perform a logged or straight update of flows within the document"""

    # Get the document we're add the snippet to
    document = state[state.manage_config.var_name]

    # Check to see if the frame class supports `logged_update`s
    if hasattr(state.manage_config.frame_cls, 'logged_update'):

        # Logged update
        document.logged_update(
            state.manage_user,
            {state.content_flows_field: state.flows}
        )

    else:
        # Straight update (no logging)
        setattr(document, state.content_flows_field, state.flows)
        document.update(state.content_flows_field)

@update_flow_contents_chains.link
def render_json(state):
    """Render a JSON response for the successful saving of content"""
    return manage_utils.json_success()

