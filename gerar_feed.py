import pandas as pd
from xml.etree.ElementTree import Element, SubElement, ElementTree

# Caminho da planilha
excel_path = "Produto da loja yampi.xlsx"

# Leitura do Excel
df = pd.read_excel(excel_path)

# Filtrar apenas produtos ativos
df = df[df["ativo"] == 1]

# Criar estrutura base do XML
rss = Element("rss", {
    "xmlns:g": "http://base.google.com/ns/1.0",
    "version": "2.0"
})
channel = SubElement(rss, "channel")
SubElement(channel, "title").text = "Produtos Amelie Flores e Afins"
SubElement(channel, "link").text = "https://ameliefloreseafins.com.br"
SubElement(channel, "description").text = "Feed de produtos para catálogo do Facebook"

# Adicionar itens ao XML
for _, row in df.iterrows():
    item = SubElement(channel, "item")
    SubElement(item, "g:id").text = str(row["id"])
    SubElement(item, "g:title").text = str(row["nome"])
    SubElement(item, "g:description").text = str(row["descricao"])
    SubElement(item, "g:link").text = str(row["link_produto"])
    SubElement(item, "g:image_link").text = str(row["link_foto_principal"])
    SubElement(item, "g:availability").text = "in stock"
    SubElement(item, "g:condition").text = "new"
    SubElement(item, "g:price").text = f'{float(row["valor_de_presente"]):.2f} BRL'
    SubElement(item, "g:brand").text = "Amelie Flores & Afins"

# Salvar arquivo XML
tree = ElementTree(rss)
tree.write("feed_facebook.xml", encoding="utf-8", xml_declaration=True)
