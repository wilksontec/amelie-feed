import pandas as pd
import xml.etree.ElementTree as ET

# Lê a planilha com todos os dados
df = pd.read_excel("Produto da loja yampi.xlsx")

# ==============================
# 1. GERAÇÃO DO XML COMPLETO PADRÃO
# ==============================
root = ET.Element("produtos")

for _, row in df.iterrows():
    produto = ET.SubElement(root, "produto")

    for col in df.columns:
        valor = str(row[col]) if not pd.isna(row[col]) else ""
        ET.SubElement(produto, col).text = valor

tree = ET.ElementTree(root)
tree.write("feed_amelie_produtos.xml", encoding="utf-8", xml_declaration=True)

# ==============================
# 2. GERAÇÃO DO XML PARA FACEBOOK
# ==============================

rss = ET.Element("rss", attrib={
    "version": "2.0",
    "xmlns:g": "http://base.google.com/ns/1.0"
})

channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Produtos Amelie Flores e Afins"
ET.SubElement(channel, "link").text = "https://ameliefloreseafins.com.br"
ET.SubElement(channel, "description").text = "Feed de produtos para o Facebook"

for _, row in df.iterrows():
    if str(row.get("ativo")).lower() != "sim":
        continue

    item = ET.SubElement(channel, "item")

    ET.SubElement(item, "g:id").text = str(row["id"])
    ET.SubElement(item, "g:title").text = str(row["nome"])
    ET.SubElement(item, "g:description").text = str(row["descricao"])
    ET.SubElement(item, "g:link").text = str(row["link_produto"])
    ET.SubElement(item, "g:image_link").text = str(row["link_foto_principal"])

    preco = float(row["valor_de_presente"]) if not pd.isna(row["valor_de_presente"]) else 0
    ET.SubElement(item, "g:price").text = f"{preco:.2f} BRL"

    frete = float(row["valor_do_frete"]) if not pd.isna(row["valor_do_frete"]) else 0
    ET.SubElement(item, "g:shipping").append(ET.Element("g:price", text=f"{frete:.2f} BRL"))

    ET.SubElement(item, "g:brand").text = "Amelie Flores & Afins"
    ET.SubElement(item, "g:condition").text = "new"
    ET.SubElement(item, "g:availability").text = "in stock"

facebook_tree = ET.ElementTree(rss)
facebook_tree.write("feed_facebook.xml", encoding="utf-8", xml_declaration=True)
