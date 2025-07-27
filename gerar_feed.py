import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import xml.dom.minidom as minidom

# Leitura do Excel da Yampi
df = pd.read_excel("Produto da loja yampi.xlsx")

# Filtrar e preparar
df = df[['id', 'nome', 'seo_descricao', 'link_produto', 'link_foto_principal', 'valor_de_presente']].dropna()
df['seo_descricao'] = df['seo_descricao'].fillna("")
df['nome'] = df['nome'].astype(str)

# Criar XML base
rss = Element('rss', version="2.0", attrib={'xmlns:g': "http://base.google.com/ns/1.0"})
channel = SubElement(rss, 'channel')
SubElement(channel, 'title').text = "Amelie Flores & Afins - Produtos"
SubElement(channel, 'link').text = "https://www.ameliefloreseafins.store"
SubElement(channel, 'description').text = "Catálogo de produtos atualizado para Google Shopping."

# Preencher produtos
for _, row in df.iterrows():
    item = SubElement(channel, 'item')
    SubElement(item, 'g:id').text = str(row['id'])
    SubElement(item, 'title').text = row['nome']
    SubElement(item, 'description').text = row['seo_descricao']
    SubElement(item, 'link').text = row['link_produto']
    SubElement(item, 'g:image_link').text = row['link_foto_principal']
    SubElement(item, 'g:price').text = f"{float(row['valor_de_presente']):.2f} BRL"
    SubElement(item, 'g:condition').text = "new"
    SubElement(item, 'g:availability').text = "in stock"

# Salvar XML
xml_str = minidom.parseString(tostring(rss)).toprettyxml(indent="  ")
with open("feed_amelie_produtos.xml", "w", encoding="utf-8") as f:
    f.write(xml_str)