tokenTool = context.onetimetoken_storage

token = tokenTool.setToken('anonymous')
portal = context.portal_url.getPortalObject()

return "%s/full-sponsorship?logincode=%s" % (portal.absolute_url(), token)
