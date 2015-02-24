
from lxml import etree

AttentionLEDTable={'1' : 1,
                   '2' : 2,
                   '3' : 3,
                   '4' : 4
                  }

PowerTable={'1' : 5,
            '2' : 6,
            '3' : 7,
            '4' : 8
           }


def init():
    print "Mock Ready"


def SetBladeAttentionLEDOn(bladeId):
    response = etree.Element('BladeResponse')
    etree.SubElement(response, 'CompletionCode').text = 'Success'
    etree.SubElement(response, 'statusDescription').text = ''
    etree.SubElement(response, 'apiVersion').text = '1'
    etree.SubElement(response, 'bladeNumber').text = bladeId
    return etree.tostring(response, pretty_print=True)

def SetAllBladesAttentionLEDOn():
    response = etree.Element('AllBladesResponse')
    for bladeId in AttentionLEDTable:
        blade = etree.SubElement(response, 'BladeResponse')
        etree.SubElement(blade, 'CompletionCode').text = 'Success'
        etree.SubElement(blade, 'statusDescription').text = ''
        etree.SubElement(blade, 'apiVersion').text = '1'
        etree.SubElement(blade, 'bladeNumber').text = bladeId
    return etree.tostring(response, pretty_print=True)

def SetBladeAttentionLEDOff(bladeId):
    response = etree.Element('BladeResponse')
    etree.SubElement(response, 'CompletionCode').text = 'Success'
    etree.SubElement(response, 'statusDescription').text = ''
    etree.SubElement(response, 'apiVersion').text = '1'
    etree.SubElement(response, 'bladeNumber').text = bladeId
    return etree.tostring(response, pretty_print=True)

def SetAllBladesAttentionLEDOff():
    response = etree.Element('AllBladesResponse')
    for bladeId in AttentionLEDTable:
        blade = etree.SubElement(response, 'BladeResponse')
        etree.SubElement(blade, 'CompletionCode').text = 'Success'
        etree.SubElement(blade, 'statusDescription').text = ''
        etree.SubElement(blade, 'apiVersion').text = '1'
        etree.SubElement(blade, 'bladeNumber').text = bladeId
    return etree.tostring(response, pretty_print=True)

def GetAllPowerState():
    PowerState = { '1' : 'ON',
                   '2' : 'OFF',
                   '3' : 'OFF',
                   '4' : 'ON'
                 }
    response = etree.Element('GetAllPowerStateResponse')
    for bladeId in PowerTable:
        power = etree.SubElement(response, 'PowerStateResponse')
        blade = etree.SubElement(power, 'bladeResponse')
        etree.SubElement(blade, 'CompletionCode').text = 'Success'
        etree.SubElement(blade, 'statusDescription').text = ''
        etree.SubElement(blade, 'apiVersion').text = '1'
        etree.SubElement(blade, 'bladeNumber').text = bladeId
        etree.SubElement(power, 'powerState').text = PowerState[ bladeId ]
    return etree.tostring(response, pretty_print=True)


