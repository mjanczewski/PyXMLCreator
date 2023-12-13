import pandas as pd

ceny_euro = pd.read_excel('ceny_xml.xlsx', dtype={'EAN': object, 'CENA':float})

XMLStart = """<?xml version="1.0" encoding="utf-8"?>
<products>
{% foreach p in products -%}
<product>
<reference><![CDATA[{{ p.Code }}]]></reference>
<product_name><![CDATA[{{ p.NameNoHtml }}]]></product_name>"""

XMLEnd = """{% else -%}<price>{{ p.SubtotalPrice }}</price>{% endif -%}\n
{% if p.StockLevel < 101 -%}<quantity>{{ p.StockLevel | ToInt }}</quantity>{% else -%}<quantity>100</quantity>{% endif -%}
{% if p.Brand == 'ANKER MAKE' -%}<producent>ANKER</producent>
{% else -%}<producent>{{ p.Brand }}</producent>{% endif -%}
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
        CENA = str(round(row['CENA'],2))
        doXML = "{% if p.UPC == '"+EAN+"' -%}<price>"+CENA+"</price>\n"
        szablonXML = doXML
    elif index <= len(ceny_euro)-1:
        EAN = row['EAN']
        EAN = str(EAN)
        CENA = str(round(row['CENA'],2))

        
        doXML = "{% elseif p.UPC == '"+EAN+"' -%}<price>"+CENA+"</price>\n"
        szablonXML = szablonXML+doXML


szablonTotal = XMLStart + szablonXML + XMLEnd
f = open('szablonXML_euronet.txt', "w")
f.write(szablonTotal)
f.close()

