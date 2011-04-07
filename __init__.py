#This software is released under GNU public license. See details in the URL:
#http://www.gnu.org/copyleft/gpl.html

import CacheVersionURL

def initialize(context):
    "Initialize the CacheVersionURL object."
    addForm = CacheVersionURL.addForm
    
    context.registerClass(
       CacheVersionURL.CacheVersionURL,
       permission='Add CacheVersionURL',
       constructors=(
        CacheVersionURL.manage_add_form,
        CacheVersionURL.manage_addCacheVersionURL,
        )
    )
