import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

# Carrega os dados do Excel
df = pd.read_excel("Produto da loja yampi.xlsx")

# Criação do XML base
rss = Element('rss', {
    'xmlns:g': "http://base.google.com/ns/1.0",
    'version': "2.0"
})
channel = SubElement(rss, 'channel')

# Informações gerais do feed
SubElement(channel, 'title').text = "Produtos Amelie Flores e Afins"
SubElement(channel, 'link').text = "https://ameliefloreseafins.com.br"
SubElement(channel, 'description').text = "Feed de produtos para o Google Merchant"

# Iterar sobre os produtos
for _, row in df.iterrows():
    if pd.isna(row.get("id")) or pd.isna(row.get("title")) or pd.isna(row.get("price")):
        continue  # Pular produtos incompletos

    item = SubElement(channel, 'item')

    SubElement(item, 'g:id').text = str(row.get("id"))
    SubElement(item, 'g:title').text = str(row.get("title"))
    SubElement(item, 'g:description').text = str(row.get("description", "Produto artesanal da Amelie"))
    SubElement(item, 'g:link').text = str(row.get("link"))
    SubElement(item, 'g:image_link').text = str(row.get("image_link"))

    # Preço (obrigatório)
    preco = float(row.get("price", 0))
    SubElement(item, 'g:price').text = f"{preco:.2f} BRL"

    # Preço promocional (opcional, só se > 0 e < price)
    sale = float(row.get("sale_price", 0))
    if 0 < sale < preco:
        SubElement(item, 'g:sale_price').text = f"{sale:.2f} BRL"

    # Disponibilidade padrão
    SubElement(item, 'g:availability').text = "in stock"

    # Frete fixo para BR
    shipping = SubElement(item, 'g:shipping')
    SubElement(shipping, 'g:country').text = "BR"
    SubElement(shipping, 'g:price').text = "15.00 BRL"

# Salvar XML
tree = ElementTree(rss)
tree.write("feed_amelie_produtos.xml", encoding='utf-8', xml_declaration=True)