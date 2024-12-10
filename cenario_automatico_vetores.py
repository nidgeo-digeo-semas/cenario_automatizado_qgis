from qgis.core import QgsProject, QgsLayerTreeGroup, QgsVectorLayer
import os

# Lista de camadas e seus caminhos
camadas_e_grupos = [
    ("Vetores/Abas de Sobreposições de IR/Terra_Legal_Glebas_Públicas", "Z:/TERRA LEGAL/TERRA_LEGAL_GLEBAS_PÚBLICAS.shp"),
    ("Vetores/Abas de Sobreposições de IR/Área_Imovel_CAR", "Z:/CAR/SICAR/AREA_IMOVEL.shp"),
    ("Vetores/Abas de Sobreposições de IR/Parcela_Regularização_PA_Terra_Legal", "Z:/TERRA LEGAL/PARCELA_REGULARIZACAO_PA.shp"),
    ("Vetores/Abas de Sobreposições de IR/Imóvel_Certificado_SNCI_Brasil_PA", "Z:/INCRA/SIGEF/Imovel_certificado_SNCI_Brasil_PA.shp"),
    ("Vetores/Abas de Sobreposições de IR/SIGEF_Brasil_PA", "Z:/INCRA/SIGEF/Sigef_Brasil_PA.shp"),
    ("Vetores/Sobreposição com Terras Indígenas/Terras_Indígenas", "Z:/FUNAI/TERRAS_INDIGENAS.shp"),
    ("Vetores/Sobreposição com Terras Indígenas/Aldeias", "Z:/FUNAI/ALDEIAS.shp"),
    ("Vetores/Sobreposição com Unidades de Conservação/UC_Municipal_Abaetetuba", "Z:/BASES MUNICIPAIS/ABAETETUBA/UC_MUNICIPAL_ABAETETUBA.shp"),
    ("Vetores/Sobreposição com Unidades de Conservação/Ucs_Municipais_MMA", "Z:/MMA/UNIDADES DE CONSERVAÇÃO MUNICIPAIS/UCS_MUNICIPAIS_MMA.shp"),
    ("Vetores/Sobreposição com Unidades de Conservação/Ucs_Estaduais_IDEFLOR_BIO", "Z:/IDEFLOR-BIO/UNIDADES DE CONSERVAÇÃO/UCS_ESTADUAIS.shp"),
    ("Vetores/Sobreposição com Unidades de Conservação/Ucs_Federais_ICMBIO", "Z:/ICMBIO/UNIDADES DE CONSERVAÇÃO/UCs FEDERAIS.shp"),
    ("Vetores/Sobreposição com Unidades de Conservação/Zona_Amortecimento_UCs_Federais_ICMBIO", "Z:/ICMBIO/ZONAS DE AMORTECIMENTO DE UC'S/ZA_UCS_FEDERAIS.shp"),
    ("Vetores/Sobreposição com Unidades de Conservação/RPPN", "Z:/ICMBIO/UNIDADES DE CONSERVAÇÃO/RPPN.shp"),
    ("Vetores/Sobreposição com Áreas Embargadas/OP_20_21", "Z:/SEMAS/LDI/OP_20_21.shp"),
    ("Vetores/Sobreposição com Áreas Embargadas/Autos_de_Infração_IBAMA", "Z:/IBAMA/ÁREAS EMBARGADAS/AUTOs_DE_INFRACAO_IBAMA.shp"),
    ("Vetores/Sobreposição com Áreas Embargadas/Embargos_IBAMA", "Z:/IBAMA/ÁREAS EMBARGADAS/EMBARGOS_IBAMA.shp"),
    ("Vetores/Sobreposição com Áreas Embargadas/Embargos_ICMBIO", "Z:/ICMBIO/EMBARGOS/Embargos_ICMBIO.shp"),
    ("Vetores/Sobreposição com Áreas Embargadas/Embargos_ICMBIO_eletrônicos", "Z:/ICMBIO/EMBARGOS/Embargos_ICMBIO_eletronicos.shp"),
    ("Vetores/Sobreposição com Áreas Embargadas/Autos_Infração_ICMBIO", "Z:/ICMBIO/EMBARGOS/Autos_Infracao_ICMBIO.shp"),
    ("Vetores/Sobreposição com Assentamento /Assentamento_Federal_PA_INCRA", "Z:/INCRA/ASSENTAMENTOS/Assentamento_Federal_PA.shp"),
    ("Vetores/Sobreposição com Assentamento /Assentamento_Estadual_ITERPA", "Z:/ITERPA/ASSENTAMENTOS/ASSENTAMENTOS_ESTADUAIS.shp"),
    ("Vetores/Sobreposição com Assentamento /PA_Carajas_I_III", "Z:/INCRA/ASSENTAMENTOS/PA_Carajas_I_III.shp"),
    ("Vetores/Outras Sobreposições /Quilombos_Estaduais_ITERPA", "Z:/ITERPA/QUILOMBOS/QUILOMBOS.shp"),
    ("Vetores/Outras Sobreposições /Quilombos_Federais_INCRA", "Z:/INCRA/QUILOMBOS/QUILOMBOS_FEDERAIS.shp"),
    ("Vetores/Outras Sobreposições /Glebas_Estaduais_ITERPA", "Z:/ZONA INDUSTRIAL/BARCARENA/ZONA_INDUSTRIAL.shp"),
    ("Vetores/Outras Sobreposições /COLONIAS_ESTADUAIS", "Z:/ITERPA/COLÔNIAS/COLONIAS_ESTADUAIS.shp"),
    ("Vetores/Outras Sobreposições /Alunorte_Barcarena", "Z:/ZONA INDUSTRIAL/BARCARENA/ALUNORTE.shp"),
    ("Vetores/Outras Sobreposições /ZONA_INDUSTRIAL", "Z:/ZONA INDUSTRIAL/BARCARENA/ZONA_INDUSTRIAL.shp"),
    ("Vetores/Outras Sobreposições /CNFP_2022", "Z:/SFB/FLORESTAS PÚBLICAS/CNFP_2022.shp"),
    ("Vetores/Cobertura do Solo/Prodes_Acumulado_até_2007", "Z:/INPE/PRODES/PRODES_ACUMULADO_ATE_2007.shp"),
    ("Vetores/Cobertura do Solo/Prodes_2008_a_2023", "Z:/INPE/PRODES/PRODES_2008_A_2023.shp"),
    ("Vetores/Cobertura do Solo/Prodes_Cerrado_2002_a_2023", "Z:/INPE/PRODES/PRODES_CERRADO_PA_2002_2023.shp"),
    ("Vetores/Área de Servidão Administrativa -  Reservatório para Abastecimento ou Geração de Energia/UHE_Belo_Monte", "Z:/HIDRELÉTRICA/UHE_Belo_Monte.shp"),
    ("Vetores/Área de Servidão Administrativa -  Reservatório para Abastecimento ou Geração de Energia/Reservatorio_Usina", "Z:/HIDRELÉTRICA/RESERVATORIO_USINA.shp"),
    ("Vetores/Área de Servidão Administrativa -  Reservatório para Abastecimento ou Geração de Energia/Zona_de_Barragem", "Z:/ZONA DE BARRAGEM/ZONA_DE_BARRAGEM.shp"),
    ("Vetores/Área de Servidão Administrativa - Infraestrutura e Utilidade Pública/Rodovia_DSG_IBGE_Total", "Z:/IBGE/IBGE-SEMAS/ESTRADA/RODOVIA_DSG_IBGE_TOTAL.shp"),
    ("Vetores/Área de Servidão Administrativa - Infraestrutura e Utilidade Pública/Estrada_Marajó_Belém_Nordeste", "Z:/IBGE/IBGE-SEMAS/ESTRADA/ESTRADA_MARAJO-BELEM-NORDESTE.shp"),
    ("Vetores/Área de Servidão Administrativa - Infraestrutura e Utilidade Pública/Estrada_Sudoeste_Paraense", "Z:/IBGE/IBGE-SEMAS/ESTRADA/ESTRADA_SUDOESTE_PARAENSE.shp"),
    ("Vetores/Área de Servidão Administrativa - Infraestrutura e Utilidade Pública/Estrada_Sudeste_Paraense", "Z:/IBGE/IBGE-SEMAS/ESTRADA/ESTRADA_SUDESTE_PARAENSE.shp"),
    ("Vetores/Área de Servidão Administrativa - Infraestrutura e Utilidade Pública/Estrada_Baixo_Amazonas", "Z:/IBGE/IBGE-SEMAS/ESTRADA/ESTRADA_BAIXO_AMAZONAS.shp"),
    ("Vetores/Área de Servidão Administrativa - Servidão Minerária /ANM_PA", "Z:/ANM/ANM_PA.shp"),
    ("Vetores/APP's/mosaico_nascente_area_1_cadastravel", "Z:/SEMAS/HIDROGRAFIA/NASCENTES/mosaico_nascente_area_1_cadastravel.shp"),
    ("Vetores/APP's/mosaico_nascente_area_2_cadastravel", "Z:/SEMAS/HIDROGRAFIA/NASCENTES/mosaico_nascente_area_2_cadastravel.shp"),
    ("Vetores/APP's/geoft_bho_trecho_drenagem_bacia_4", "Z:/SEMAS/HIDROGRAFIA/BACIA_4/geoft_bho_trecho_drenagem_bacia_4.shp"),
    ("Vetores/APP's/geoft_bho_trecho_drenagem_bacia_5", "Z:/SEMAS/HIDROGRAFIA/BACIA_5/geoft_bho_trecho_drenagem_bacia_5.shp"),
    ("Vetores/APP's/geoft_bho_trecho_drenagem_bacia_6", "Z:/SEMAS/HIDROGRAFIA/BACIA_6/geoft_bho_trecho_drenagem_bacia_6.shp"),
    ("Vetores/APP's/geoft_bho_trecho_drenagem_bacia_7", "Z:/SEMAS/HIDROGRAFIA/BACIA_7/geoft_bho_trecho_drenagem_bacia_7.shp"),
    ("Vetores/APP's/MASSA_DAGUA_LESTE", "Z:/SEMAS/MASSA D'ÁGUA/massa_dagua_LESTE.shp"),
    ("Vetores/APP's/massa_dagua_OESTE", "Z:/SEMAS/MASSA D'ÁGUA/massa_dagua_OESTE.shp"),
    ("Vetores/MZEE e ZEE/MZEE", "Z:/SEMAS/MZEE/MZEE.shp"),
    ("Vetores/MZEE e ZEE/ZEE", "Z:/SEMAS/ZEE/ZEE.shp"),
    ("Vetores/Malha de Imagens/GRADE_SPOT_2007", "Y:/Imagem_SPOT/2007/GRADE_SPOT_2007.shp"),
    ("Vetores/Malha de Imagens/GRADE_SPOT_2008", "Y:/Imagem_SPOT/2008/GRADE_SPOT__2008.shp"),
    ("Vetores/Malha de Imagens/GRADE_SPOT_2009", "Y:/Imagem_SPOT/2009/GRADE_SPOT_2009.shp"),
    ("Vetores/Malha de Imagens/GRADE_SPOT_2010", "Y:/Imagem_SPOT/2010/GRADE_SPOT_2010.shp"),
    ("Vetores/Malha de Imagens/GRADE_SPOT_2011", "Y:/Imagem_SPOT/2011/GRADE_SPOT_2011.shp"),
    ("Vetores/Malha de Imagens/LANDSAT", "Z:/MALHA_IMAGENS/LANDSAT2.shp"),
    ("Vetores/Malha de Imagens/RAPIDEYE", "Z:/MALHA_IMAGENS/RAPIDEYE.shp"),
    ("Vetores/Malha de Imagens/RESOURCESAT", "Z:/MALHA_IMAGENS/RESORCESAT.shp"),
    ("Vetores/Malha de Imagens/SENTINEL", "Z:/MALHA_IMAGENS/SENTINEL.shp"),
    ("Vetores/Malha de Imagens/MUNICIPIOS", "Z:/IBGE/MUNICÍPIOS/MUNICIPIOS.shp"),
    ("Vetores/Malha de Imagens/FUSOS UTM", "Z:/ZONAS-PARÁ/FUSOSUTM.shp"),
    ("Vetores/Analise Licenciamento/Bovinocultura", "Z:/SEMAS/LAR_BOVINOCULTURA/Bovinocultura.shp"),
    ("Vetores/Analise Licenciamento/APAT", "Z:/SEMAS/APAT/APAT.shp"),
    ("Vetores/Analise Licenciamento/Àreas_Coletivas_ITERPA", "Z:/ITERPA/ÁREAS COM TITULAÇÃO COLETIVA/AREAS_COLETIVAS_ITERPA.shp"),
    ("Vetores/Analise Licenciamento/Supressão_RDR", "Z:/SEMAS/SUPRESSÃO/RDR/SUPRESSÃO_RDR.shp"),
    ("Vetores/Analise Licenciamento/Reflorestamento", "Z:/SEMAS/REFLORESTAMENTO/REFLORESTAMENTO.shp"),
    ("Vetores/Analise Licenciamento/Supressão", "Z:/SEMAS/SUPRESSÃO/SUPRESSÃO.shp"),
    ("Vetores/Analise Licenciamento/AMF", "Z:/SEMAS/PMFS/AMF.shp"),
    ("Vetores/Analise Licenciamento/UPA", "Z:/SEMAS/PMFS/UPA.shp"),
    ("Vetores/Sítios Arqueológicos/Sitios_Arqueologicos_PA", "Z:/IPHAN/Sitios_Arqueologicos_PA.shp")
]

# Obter o nó raiz do projeto
projeto = QgsProject.instance()
raiz = projeto.layerTreeRoot()

# Função para criar grupos recursivamente
def criar_grupo_recursivo(nome_completo):
    partes = nome_completo.split("/")
    grupo_atual = raiz
    for parte in partes[:-1]:  # Excluir o nome da camada
        grupo_existente = grupo_atual.findGroup(parte)
        if not grupo_existente:
            grupo_existente = grupo_atual.addGroup(parte)
        grupo_atual = grupo_existente
    return grupo_atual

# Adicionar as camadas ao projeto e aos grupos
for caminho_grupo, caminho_arquivo in camadas_e_grupos:
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        continue

    # Criar o grupo
    grupo = criar_grupo_recursivo(caminho_grupo)

    # Adicionar a camada ao grupo
    camada = QgsVectorLayer(caminho_arquivo, caminho_grupo.split("/")[-1], "ogr")
    if camada.isValid():
        projeto.addMapLayer(camada, False)  # Adicionar sem exibir na raiz
        grupo.addLayer(camada)
    else:
        print(f"Falha ao carregar a camada: {caminho_arquivo}")

print("Cenário recriado com sucesso!")
