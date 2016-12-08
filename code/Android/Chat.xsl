<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 

 <xsl:template match="Chat">
  <div id="{@id}">
   <xsl:call-template name="Chat" />
  </div>
 </xsl:template>

 <xsl:template match="Chat.update">
  <xsl:if test="@changed='true'">
   <replaceInner id="{@id}">
    <xsl:call-template name="Chat" />
   </replaceInner>
  </xsl:if>
 </xsl:template>
 
 <xsl:template name="Chat">
  <ul>
   <xsl:for-each select="messages/ChatMsg">
    <li>
     <b><xsl:value-of select="@sent" /></b>:
     <xsl:value-of select="msg" /> 
     <i> (expires: <xsl:value-of select="@expires" />)</i>
    </li>
   </xsl:for-each>
  </ul>
 </xsl:template>

</xsl:stylesheet>