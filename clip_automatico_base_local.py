import os
from qgis.core import (
    QgsVectorLayer, QgsFeatureRequest, QgsProject, QgsVectorFileWriter,
    QgsCoordinateReferenceSystem, QgsFeature
)

# Caminho do shapefile com a base de dados
caminho_basecar = r"G:\BASE CAR NIDGEO\basecar_nidgeo.shp"

# Caminho para salvar os arquivos
pasta_base = r"N:\SAMUEL SANTOS\AUTOMAÇÃO QGIS"

# Código do imóvel a filtrar
cod_imovel_teste = "PA-1500107-00C38A0403EE4017B44F8B5C6C37E674"

# Função para criar grupos recursivamente no QGIS
def criar_grupo_recursivo(raiz, nome_completo):
    partes = nome_completo.split("/")
    grupo_atual = raiz
    for parte in partes[:-1]:  # Excluir o nome da camada
        grupo_existente = grupo_atual.findGroup(parte)
        if not grupo_existente:
            grupo_existente = grupo_atual.addGroup(parte)
        grupo_atual = grupo_existente
    return grupo_atual

try:
    print("Carregando camada base...")
    camada_base = QgsVectorLayer(caminho_basecar, "Base CAR NIDGEO", "ogr")
    if not camada_base.isValid():
        raise Exception(f"Erro ao carregar a camada base: {caminho_basecar}")
    print("Camada base carregada com sucesso.")

    print("Filtrando imóvel...")
    request = QgsFeatureRequest().setFilterExpression(f"\"cod_imovel\" = '{cod_imovel_teste}'")
    features = camada_base.getFeatures(request)
    feature_imovel = next(features, None)

    if not feature_imovel:
        raise Exception(f"Imóvel com cod_imovel '{cod_imovel_teste}' não encontrado na base.")

    print("Imóvel encontrado. Preparando exportação...")
    nome_imovel = feature_imovel["nom_imovel"]
    nome_pasta = f"{cod_imovel_teste}-{nome_imovel}".replace(" ", "_")
    caminho_pasta = os.path.join(pasta_base, nome_pasta)
    os.makedirs(caminho_pasta, exist_ok=True)

    # Salvar shapefile do imóvel filtrado
    caminho_shapefile = os.path.join(caminho_pasta, f"{cod_imovel_teste}.shp")
    camada_filtrada = QgsVectorLayer(f"Polygon?crs=EPSG:4674", "Imóvel Filtrado", "memory")
    provedor = camada_filtrada.dataProvider()
    provedor.addAttributes(camada_base.fields())
    camada_filtrada.updateFields()

    # Criar uma nova feature com a geometria e atributos
    nova_feature = QgsFeature(camada_base.fields())
    nova_feature.setGeometry(feature_imovel.geometry())
    for campo in camada_base.fields():
        nova_feature[campo.name()] = feature_imovel[campo.name()]
    provedor.addFeatures([nova_feature])

    QgsVectorFileWriter.writeAsVectorFormat(
        camada_filtrada, caminho_shapefile, "utf-8", camada_filtrada.crs(), "ESRI Shapefile"
    )
    print(f"Imóvel exportado: {caminho_shapefile}")

    # Adicionar camada ao projeto
    projeto = QgsProject.instance()
    raiz = projeto.layerTreeRoot()
    grupo_imovel = criar_grupo_recursivo(raiz, "Clips/Imóvel Filtrado")

    # Criar buffer de 15 km
    print("Criando buffer de 15 km...")
    crs_4674 = QgsCoordinateReferenceSystem("EPSG:4674")
    crs_metrico = QgsCoordinateReferenceSystem("EPSG:31983")
    transform = QgsCoordinateTransform(crs_4674, crs_metrico, QgsProject.instance())
    geom_transformada = feature_imovel.geometry()
    geom_transformada.transform(transform)
    buffer_geom = geom_transformada.buffer(15000, 10)
    transform_inverso = QgsCoordinateTransform(crs_metrico, crs_4674, QgsProject.instance())
    buffer_geom.transform(transform_inverso)

    # Salvar o buffer em EPSG:4674
    caminho_buffer = os.path.join(caminho_pasta, "buffer_15km.shp")
    camada_buffer = QgsVectorLayer(f"Polygon?crs=EPSG:4674", "Buffer 15km", "memory")
    provedor_buffer = camada_buffer.dataProvider()
    buffer_feature = QgsFeature()
    buffer_feature.setGeometry(buffer_geom)
    provedor_buffer.addFeatures([buffer_feature])
    QgsVectorFileWriter.writeAsVectorFormat(camada_buffer, caminho_buffer, "utf-8", camada_buffer.crs(), "ESRI Shapefile")
    print(f"Buffer criado e salvo: {caminho_buffer}")

    # Adicionar camadas exportadas ao projeto
    projeto = QgsProject.instance()
    grupo_clips = projeto.layerTreeRoot().findGroup("Clips") or projeto.layerTreeRoot().addGroup("Clips")

    # Adicionar imóvel exportado ao projeto
    if os.path.exists(caminho_shapefile):
        camada_imovel_salva = QgsVectorLayer(caminho_shapefile, "Imóvel Exportado", "ogr")
        projeto.addMapLayer(camada_imovel_salva, False)
        grupo_clips.addLayer(camada_imovel_salva)

    # Adicionar buffer exportado ao projeto
    if os.path.exists(caminho_buffer):
        camada_buffer_salva = QgsVectorLayer(caminho_buffer, "Buffer 15km", "ogr")
        projeto.addMapLayer(camada_buffer_salva, False)
        grupo_clips.addLayer(camada_buffer_salva)

    # Adicionar esta função para garantir que a projeção seja configurada corretamente
    def corrigir_projecao(camada, epsg="EPSG:4674"):
        crs = QgsCoordinateReferenceSystem(epsg)
        if camada.crs() != crs:
            print(f"Corrigindo projeção da camada {camada.name()} para {epsg}.")
            camada.setCrs(crs)

    # Função para recortar camadas
    def recortar_camadas(buffer_geom, grupo_origem, grupo_destino, pasta_destino):
        if not grupo_origem:
            print("Grupo 'Vetores' não encontrado. Certifique-se de que ele existe no projeto.")
            return

        for subgrupo in grupo_origem.children():
            if isinstance(subgrupo, QgsLayerTreeGroup):
                nome_subgrupo = subgrupo.name()
                subgrupo_destino = grupo_destino.findGroup(nome_subgrupo) or grupo_destino.addGroup(nome_subgrupo)
                pasta_subgrupo = os.path.join(pasta_destino, nome_subgrupo)
                os.makedirs(pasta_subgrupo, exist_ok=True)

                for camada_tree in subgrupo.children():
                    if isinstance(camada_tree, QgsLayerTreeLayer):
                        camada = camada_tree.layer()
                        if not camada.isValid():
                            continue
                        camada_recortada = QgsVectorLayer(f"Polygon?crs=EPSG:4674", camada.name(), "memory")
                        provedor_recorte = camada_recortada.dataProvider()
                        provedor_recorte.addAttributes(camada.fields())
                        camada_recortada.updateFields()

                        for feature in camada.getFeatures():
                            if feature.geometry() and feature.geometry().intersects(buffer_geom):
                                feature_recortada = QgsFeature(camada.fields())
                                feature_recortada.setGeometry(feature.geometry().intersection(buffer_geom))
                                for campo in camada.fields():
                                    feature_recortada[campo.name()] = feature[campo.name()]
                                provedor_recorte.addFeatures([feature_recortada])

                        if camada_recortada.featureCount() > 0:
                            caminho_saida = os.path.join(pasta_subgrupo, f"{camada.name()}.shp")
                            QgsVectorFileWriter.writeAsVectorFormat(camada_recortada, caminho_saida, "utf-8", camada_recortada.crs(), "ESRI Shapefile")
                            if os.path.exists(caminho_saida):  # Verifica se o arquivo foi criado
                                camada_recortada_salva = QgsVectorLayer(caminho_saida, camada.name(), "ogr")
                                corrigir_projecao(camada_recortada_salva, "EPSG:4674")  # Corrigir projeção ao carregar
                                projeto.addMapLayer(camada_recortada_salva, False)
                                subgrupo_destino.addLayer(camada_recortada_salva)

    # Remover subgrupos vazios
    def remover_subgrupos_vazios(grupo_destino):
        for subgrupo in grupo_destino.children():
            if isinstance(subgrupo, QgsLayerTreeGroup) and not subgrupo.findLayerIds():
                grupo_destino.removeChildNode(subgrupo)

    # Recortar camadas
    print("Recortando camadas no grupo 'Vetores'...")
    grupo_origem = projeto.layerTreeRoot().findGroup("Vetores")
    recortar_camadas(buffer_geom, grupo_origem, grupo_clips, os.path.join(caminho_pasta, "Clips"))
    remover_subgrupos_vazios(grupo_clips)
    print("Recortes concluídos com sucesso.")

except Exception as e:
    print(f"Erro: {e}")

finally:
    print("Finalizando...")

