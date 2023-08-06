from M.MCore import MCore

""" 
    -> This is a "Static" Instance of the Database for all to use.
"""

DEFAULT_HOST_INSTANCE = None

if not DEFAULT_HOST_INSTANCE:
    DEFAULT_HOST_INSTANCE = MCore().constructor()

def GET_COLLECTION(collection_name):
    if DEFAULT_HOST_INSTANCE:
        return DEFAULT_HOST_INSTANCE.get_collection(collection_name)
    return MCore.Collection(collection_name)

def SET_COLLECTION(collection_name):
    if DEFAULT_HOST_INSTANCE:
        return DEFAULT_HOST_INSTANCE.set_ccollection(collection_name)
    return MCore.SetCollection(collection_name)

# def GET_MCOLLECTION(collection_name):
#     return MCollection().construct_mcollection(collection_or_name=collection_name)
