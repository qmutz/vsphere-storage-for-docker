##
## This module handles creating and managing a kv store for volumes
## (vmdks) created by the docker volume plugin on an ESX host. The
## module exposes a set of functions that allow creat/delete/get/set
## on the kv store. Currently uses side cars to keep KV pairs for
## a given volume.

import logging
import kvESX

# Default meta-data for a volume created by the plugin, keys can be
# added or removed during the life of a volume. The below list
# is whats included by default when a kv store is created.
#
# 1. status - the status of the volume, whether its attached or
#             not to a VM.
# 2. volOpts - the string of options with which the volume was
#              created.

# Create a kv store object for this volume identified by volPath
# Create the side car or open if it exists.
def init():
   kvESX.kvESXInit()
   return None


# Create a side car KV store for given volpath
def create(volPath, status, opts):
   volMeta = {'status': status,
              'volOpts': opts};

   res = kvESX.create(volPath, volMeta)

   if res != True:
      logging.debug ("KV store create failed.")
      return False

   return True

# Delete a kv store object for this volume identified by volPath
def delete(volPath):
   return kvESX.delete(volPath)

# Return the entire meta-data for the given volpath
def getAll(volPath):
   volMeta = kvESX.load(volPath)

   if volMeta:
      return volMeta
   else:
      return None

# Store the meta-data for a given vol-path
def setAll(volPath, volMeta):
   if volMeta:
       return kvESX.save(volPath, volMeta)

# Set a string value for a given key(index)
def set(volPath, key, val):
   volMeta = kvESX.load(volPath)

   if not volMeta:
      return False

   volMeta[key] = val

   return kvESX.save(volPath, volMeta)


# Get value for a given key (index), returns a string thats the value
# for the key
def get(volPath, key):
   volMeta = kvESX.load(volPath)

   if not volMeta:
      return None

   if volMeta.has_key(key):
      return volMeta[key]
   else:
      return None

# No-op for side car based KV pairs, once added KV pairs live till
# the side car is deleted.
def remove(volPath, key):
   volMeta = kvESX.load(volPath)

   if not volMeta:
      return False

   del volMeta[key]

   return kvESX.save(volPath, volMeta)