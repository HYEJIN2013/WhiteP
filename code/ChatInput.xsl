<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 

 <xsl:template match="ChatInput">
  <div id="{@id}">
   <xsl:call-template name="ChatInput" />
  </div>
 </xsl:template>

 <xsl:template match="ChatInput.update">
  <replaceInner id="{@id}">
   <xsl:call-template name="ChatInput" />
  </replaceInner>
 </xsl:template>
 
 <xsl:template name="ChatInput">
  <input type="text" id="{@id}_newmsg" />
  <input id="{@id}_button" type="button" 
         class="button"
         value="Add (or press enter)" />
 </xsl:template>

</xsl:stylesheet>