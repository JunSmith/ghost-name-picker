from google.appengine.ext import db
import models
import ghost_vault

def catch():
    ghosts_result = db.Query(models.Ghost)
    if(ghosts_result.get() == None):
        for ghost in ghost_vault.get():
            ghost_entity = models.Ghost(name =  ghost.keys()[0], description = ghost.values()[0])
            ghost_entity.put()
