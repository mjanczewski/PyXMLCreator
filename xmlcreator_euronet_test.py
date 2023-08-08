import pandas as pd


KodyEAN_Zero = ('024066058973','024066059000','024066059017','024066059024','024066063274','024066583338','024066002839','024066002846','024066070999',
'024066055743','024066058621','024066061164','024066071088','024066071095','024066071101','024066071118','024066061218','024066071125','024066071132','024066071156',
'024066070616','024066070623','024066070630','024066070654','024066067265','024066067302','024066070098','024066070104','024066070128','024066070142','024066070159',
'024066070173','024066070180','024066070203','024066057310','024066071613','024066071651','024066069238','024066069290','024066070906','024066070913','024066070920',
'024066070937','024066070944','024066070951','024066065780','024066065797','024066070432','024066070449','024066070456','024066070463','024066070470','024066070487',
'024066070494','024066069979','024066070012','024066070029','024066070043','024066070050','024066070067','024066069870','024066069887','024066069948')



for i in range(len(KodyEAN_Zero)):
    print(KodyEAN_Zero[i])

# ceny_euro = pd.read_excel('ceny_xml.xlsx')
ceny_euro = pd.read_excel('ceny_xml.xlsx', dtype={'EAN': object, 'CENA':float})
print(ceny_euro)

XMLStart = """<?xml version="1.0" encoding="utf-8"?>
<products>
{% foreach p in products -%}
<product>
<reference><![CDATA[{{ p.Code }}]]></reference>
<product_name><![CDATA[{{ p.NameNoHtml }}]]></product_name>"""

XMLEnd = """{% else -%}<price>{{ p.SubtotalPrice }}</price>{% endif -%}\n
{% if p.StockLevel < 101 -%}<quantity>{{ p.StockLevel | ToInt }}</quantity>{% else -%}<quantity>100</quantity>{% endif -%}
<producent><![CDATA[{{ p.Brand }}]]></producent>
<guarantee><![CDATA[{{ p.Attributes['Gwarancja'].Values[0] }}]]></guarantee>
<ean13><![CDATA[{{ p.UPC }}]]></ean13>
<categories><![CDATA[{{ p.GroupName }}]]></categories>
<description><![CDATA[{{ p.Description }}]]></description>
<images>{{ p.Images | Map:'Url' | Join:',' }}</images>
<retail_price>{{ p.TotalPreviousPrice }}</retail_price>
{% comment -%}<length>{{ p.Dimensions.Length }}</length>{% endcomment -%}
{% comment -%}<width>{{ p.Dimensions.Width }}</width>{% endcomment -%}
{% comment -%}<height>{{ p.Dimensions.Height }}</height>{% endcomment -%}
<gross_weight>{{ p.Weight }}</gross_weight>
<net_weight>{{ p.NetWeight }}</net_weight>
</product>
{% endforeach -%}
</products>"""

szablonXML = ""

for index, row in ceny_euro.iterrows():
    if index == 0:
        EAN = row['EAN']
        EAN = str(EAN)
        CENA = row['CENA']
        CENA = str(row['CENA'])
        doXML = "{% if p.UPC == '"+EAN+"' -%}<price>"+CENA+"</price>\n"
        szablonXML = doXML
    elif index <= len(ceny_euro)-1:
        EAN = row['EAN']
        EAN = str(EAN)
        CENA = row['CENA']
        # print(row['CENA'])
        CENA = str(row['CENA'])

        
        doXML = "{% elseif p.UPC == '"+EAN+"' -%}<price>"+CENA+"</price>\n"
        szablonXML = szablonXML+doXML

    # else:
    #     EAN = row['EAN']
    #     EAN = str(EAN)
    #     CENA = row['CENA']
    #     CENA = str(row['CENA'])
    #     doXML = "{% else -%}<price>{{ p.SubtotalPrice }}</price>{% endif -%}\n"
    #     szablonXML = szablonXML+doXML


szablonTotal = XMLStart + szablonXML + XMLEnd
f = open('szablonXML_euronet.txt', "w")
f.write(szablonTotal)
f.close()

