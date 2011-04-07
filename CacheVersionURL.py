#This software is released under GNU public license. See details in the URL:
#http://www.gnu.org/copyleft/gpl.html

#For Security control and init
from AccessControl import ClassSecurityInfo
import Globals
from Acquisition import aq_base
from OFS.SimpleItem import SimpleItem

from zLOG.EventLogger import log_write
import zLOG

def log(name, short="", longMessage="", error_level=zLOG.INFO, reraise=0):
    "Log an error to a file"
    log_write(name, error_level, str(short), str(longMessage), None)

def manage_addCacheVersionURL(self, name):
    "create a CacheVersionURL object"
    self._setObject(name, CacheVersionURL(name))
    return self.REQUEST.RESPONSE.redirect(self.absolute_url() + "/manage_workspace")

addForm = '''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head><title>CacheVersionURL</title>
    <style>
    p.error {
        background-color: #FFDDDD;
    }
    </style>
    </head><body>
    <div><form name="form" action="manage_addCacheVersionURL">
    <p>Name:<input type="text" name="name" value="" /></p>
    <p><input type="submit" name="manage_add" value="Create CacheVersionURL" /></p>
    </form></div>
    </body></html>
    '''
    
def manage_add_form(self):
    "Manage add form"
    return addForm
    
class CacheVersionURL(SimpleItem):
        "this object creates versioned urls and uses __bobo_traverse__ to find the real object"
        meta_type = "CacheVersionURL"
        security = ClassSecurityInfo()
        prefix = 'ver_'
        
        manage_options = ({'label': 'Edit', 'action': 'manage_workspace'},)
        
        security.declarePrivate('__init__')
        def __init__(self, name):
            "create a new cdoc"
            self.id = name       
        
        security.declarePublic('__bobo_traverse__')
        def __bobo_traverse__(self, REQUEST, name):
            "bobo method"
            #If we have an object with this name return it otherwise try a layout
            if name.startswith('ver_'):
                name = self.REQUEST.TraversalRequestNameStack.pop()
                self.REQUEST.RESPONSE.setHeader('Cache-Control', 'max-age=315360000')
                self.REQUEST.RESPONSE.setHeader('Expires', 'Thu, 01 Dec 2030 12:00:0')
            obj = getattr(self, name, None)
            if obj is not None:
                return obj
                        
        def index_html(self):
            "main view of docs"
            return ""
        
        def manage_workspace(self):
            "edit interface"
            temp = []
            temp.append(self.manage_page_header())
            temp.append(self.manage_tabs())
            temp.append('''<div>There is nothing to edit in this object</div>
            <div>To use this object call version_absolute_url or version_absolute_url_path with your object
            as an arguement</div>''')
            temp.append(self.manage_page_footer())
            return ''.join(temp)
            
        security.declarePublic('absolute_url')
        def version_absolute_url(self, obj, relative=0):
            """Return the absolute URL of the object"""
            version = '/%s%s' % (self.prefix, int(obj.bobobase_modification_time().timeTime()))
            local_url = self.absolute_url(relative)
            parent_url = local_url.replace('/'+self.id, '')
            obj_url = obj.absolute_url(relative)
            return local_url + version + obj_url.replace(parent_url, '')

        security.declarePublic('absolute_url_path')
        def version_absolute_url_path(self, obj):
            """Return the absolute URL of the object"""
            version = '/%s%s' % (self.prefix, int(obj.bobobase_modification_time().timeTime()))
            local_path = self.absolute_url_path()
            parent_path = local_path.replace('/'+self.id, '')
            obj_path = obj.absolute_url_path()
            log('path', (parent_path, local_path, obj_path))
            return local_path + version + obj_path.replace(parent_path, '')
            
            
Globals.InitializeClass(CacheVersionURL)