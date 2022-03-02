################# cálculo das coordenadas utilizando o vizinho mais próximo  ################
def vizinho_mais_proximo(training_data_set_only_attributes,training_data_set,test_data_set_only_attributes,test_data_set, k_neighbors):
  
  training_data_set_array = training_data_set_only_attributes.to_numpy()
  test_data_set_only_attributes_array = test_data_set_only_attributes.to_numpy()
  tree = spatial.KDTree(training_data_set_array)
  axis_x_mean = []
  axis_x_desvio = []
  axis_y_mean = []
  axis_y_desvio = []
  test_data_set_only_attributes_list = test_data_set_only_attributes.values.tolist()

  size_test_set = len(test_data_set)

  for i in range(size_test_set):
    query_result = tree.query(test_data_set_only_attributes_list[i],k_neighbors)
    df_para_media = training_data_set.loc[query_result[1]]
    axis_x_mean.append(df_para_media['Eixo_x'].mean())
    axis_x_desvio.append(df_para_media['Eixo_x'].std())
    axis_y_mean.append(df_para_media['Eixo_y'].mean())
    axis_y_desvio.append(df_para_media['Eixo_y'].std())

  test_data_set['Eixo_x'] = axis_x_mean
  test_data_set['Eixo_x_desvio'] = axis_x_desvio
  test_data_set['Eixo_y'] = axis_y_mean
  test_data_set['Eixo_y_desvio'] = axis_y_desvio
  return test_data_set



path = '/content/drive/MyDrive/BINGO/BINGO/t-SNE analysis/SAMPLE/'
file_name = 'sample_per_npix_50_test.fits'

teste_sample = Table.read(path+file_name).to_pandas()

teste_sample['class'] = teste_sample['class'].str.decode("utf-8")
#filtra o df original para conter apenas os atributos de interesse
teste_sample_filtrado = filtro_para_treino(teste_sample)
#normaliza o df para condicionar ao modelo
teste_sample_filtrado = minmax_norm(teste_sample_filtrado)


teste_vizinho_mais_proximo = vizinho_mais_proximo(training_sample_filtrado,tsne_analysis_100_5000,teste_sample_filtrado,teste_sample)