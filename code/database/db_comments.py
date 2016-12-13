# coding: utf8
# models/db_comments.py

# Make sure to handle / page
# Dont forget to change EDIT_ME
if request.get_vars['page_id']=='/':
    request.get_vars['page_id'] = 'EDIT_ME/JE_Coding/default/index'

db.define_table('comment_post',
    Field('body','text',label=T('Your comment')),
    Field('atURL', 'text', writable=False, readable=False, label=T('At URL'), 
    default=request.get_vars['page_id']), auth.signature)
