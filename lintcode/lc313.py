
s='''
<books name="aaa">
    <a value="1"></a>
    <b value="2"></b>
    <c value="3"></c>
    <d value="4"></d>
    <e value="5"></e>
    <f value="6"></f>
</books>
'''

import xml.dom.minidom as minidom

xml_obj=minidom.parseString(s)

print(*sorted(dir(xml_obj)),sep='\n')

print(xml_obj.childNodes[0].childNodes)