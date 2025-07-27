import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom as minidom

df = pd.read_excel("Produto da loja yampi.xlsx")

df = df[['id', 'nome', 'seo_descricao', 'link_produto', 'link_foto_principal', 'valor_de_presente']]
df = df.dropna(subset=['valor_de_presente', 'link_produto'])
df['seo_descricao'] = df['seo_descricao'].fillna("")
df['nome'] = df['nome'].astype(str)

# Definindo preços originais simulados (promoção: 10% acima do valor atual)
df['preco_normal'] = df['valor_de_presente'] * 1.10

rss = Element('rss', version="2.0", attrib={'xmlns:g': "http://base.google.com/ns/1.0"})
channel = SubElement(rss, 'channel')
SubElement(channel, 'title').text = "Amelie Flores & Afins - Produtos"
SubElement(channel, 'link').text = "https://www.ameliefloreseafins.store"
SubElement(channel, 'description').text = "Catálogo de produtos atualizado para Google Shopping."

for _, row in df.iterrows():
    item = SubElement(channel, 'item')
    SubElement(item, 'g:id').text = str(row['id'])
    SubElement(item, 'title').text = row['nome']
    SubElement(item, 'description').text = row['seo_descricao']
    SubElement(item, 'link').text = row['link_produto']
    SubElement(item, 'g:image_link').text = row['link_foto_principal']
    SubElement(item, 'g:price').text = f"{row['preco_normal']:.2f} BRL"
    SubElement(item, 'g:sale_price').text = f"{row['valor_de_presente']:.2f} BRL"
    SubElement(item, 'g:condition').text = "new"
    SubElement(item, 'g:availability').text = "in stock"

xml_str = minidom.parseString(tostring(rss)).toprettyxml(indent="  ")
with open("feed_amelie_produtos.xml", "w", encoding="utf-8") as f:
    f.write(xml_str)
