import hashlib, os, re

COLLECTION_FLAG = '.plexcollection'

def Start():
  pass
  
def ValidatePrefs():
  pass

class CollectionAgent(Agent.Movies):
  name = 'Collection Agent (Movies)'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.none', 'com.plexapp.agents.imdb', 'com.plexapp.agents.themoviedb', 'com.plexapp.agents.youtube', 'com.plexapp.agents.staticmedia']

  def search(self, results, media, lang, manual=False):
    if media.primary_agent == 'com.plexapp.agents.none':
      results.Append(MetadataSearchResult(id = media.id, score = 100))
    else:
      results.Append(MetadataSearchResult(id = media.primary_metadata.id, score = 100))

  def update(self, metadata, media, lang):
    part = media.items[0].parts[0]
    path = os.path.dirname(part.file)
    (root_file, ext) = os.path.splitext(os.path.basename(part.file))
    
    if os.path.isfile(os.path.join(path, COLLECTION_FLAG)):
      collection = os.path.basename(path)
      if Prefs['clear_collections']:
        metadata.collections.clear()
      metadata.collections.add(collection)
      Log('[COLLECTION] Collection set to %s for %s' % (collection, root_file))
    else:
      if Prefs['reset_collections']:
        metadata.collections.clear()
        Log('[COLLECTION] Collection reset for %s' % (root_file))
