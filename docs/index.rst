.. watsongraph documentation master file, created by
   sphinx-quickstart on Tue Jan 19 17:56:01 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to watsongraph's documentation!
=======================================

Contents:

.. toctree::
   :maxdepth: 2

.. module:: conceptmodel

.. autoclass:: ConceptModel
    :members: __init__, concepts, edges, remove, neighborhood, set_property, map_property, concepts_by_property, set_view_counts, get_view_count, concepts_by_view_count, add, merge_with, copy, augment, abridge, explode, expand, add_edges, add_edge, explode_edges, to_json, load_from_json

.. module:: item

.. autoclass:: Item
   :members: __init__, concepts, relevancies, to_json, load_from_json, save, load

.. module:: user

.. autoclass:: User
    :members: __init__, concepts, interests, interest_in, get_best_item, express_interest, express_disinterest, input_interest, input_interests, save_user, load_user, update_user_credentials, delete_user


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

