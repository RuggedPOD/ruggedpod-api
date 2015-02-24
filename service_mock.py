
from lxml import etree

def init():
    print "Mock Ready"


def SetBladeAttentionLEDOn(bladeId):
    return """
<BladeResponse
xmlns=http://schemas.datacontract.org/2004/07/Microsoft.GFS.ACS.Contracts
xmlns:i=http://www.w3.org/2001/XMLSchema-instance>
    <CompletionCode>Success</CompletionCode>
    <statusDescription></statusDescription>
    <apiVersion>1</apiVersion>
    <bladeNumber>%s</bladeNumber>
</BladeResponse>""" %bladeId
