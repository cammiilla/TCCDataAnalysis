################# IMPORTS  ################

#################  FUNCTIONS  ################

################# Normalização do df ################
def minmax_norm(df_input):
    """
    Normalizes all columns of a data frame, leaving all values between 0 and 1
    Input: Data Frame consisting of numeric values
    Output: Data Frame with all columns normalized
    """
    normalization = (df_input - df_input.min()) / ( df_input.max() - df_input.min())
    return normalization

################# análise TSNE  ################

def tsne_analisys(data_to_analisys, perplexity, n_iter):
    """
    t-SNE is applied in a dataframe, with reduction to two dimensions, perplexity and number of iterations according to the input value
    The input is a dataframe with N dimensions (columns) and the output is a dataframe with two columns, "x-axis" and "y_axis"
    """

    tsne_analisys = TSNE(n_components=2, perplexity=perplexity, n_iter=n_iter).fit_transform(data_to_analisys)
    tsne_analisys = pd.DataFrame(tsne_analisys, columns = ['Eixo_x','Eixo_y'])
    return tsne_analisys

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

################# filtro do df para treino  ################

def filtro_para_treino(df):
  df_filtrado  = df.copy()
  df_filtrado.drop(['Npix', 'specObjID', 'survey', 'instrument', 'class', 'ra', 'dec', 'z',
       'zErr', 'COADD_OBJECT_ID', 'RA', 'DEC', 'HPIX_64'], axis=1, inplace=True)
  return df_filtrado

################# cria uma matriz com a taxa de quasares por estrelas  ################

def matriz_distribuicao(df,i_lines,j_colunms,min_linha,min_coluna): 
  '''
  This function creates a matrix with i_lines and j_colunms 
  
  '''
  matrix = np.zeros((i_lines, j_colunms))
  for i in range(len(matrix)):
    min_linha = min_linha
    coordenada_linha = min_linha + i
    for j in range(len(matrix)):
        min_coluna = min_coluna
        coordenada_coluna = min_coluna + j
        contagem = df.copy()
        contagem = contagem[contagem['Eixo_x']<=coordenada_linha]
        contagem = contagem[contagem['Eixo_x']>coordenada_linha-1]
        contagem = contagem[contagem['Eixo_y']<=coordenada_coluna]
        contagem = contagem[contagem['Eixo_y']>coordenada_coluna-1]
        if len(contagem[contagem['class']=='STAR']) == 0:
          ratio = 0
        else:
          ratio = len(contagem[contagem['class']=='QSO'])/len(contagem[contagem['class']=='STAR'])
        matrix[i][j] = ratio
  return matrix 
  #convulução dos pixels através da transformada de fourrier 

  #regularizar a matriz, utilizando um smoothing con kernel (?). Kernel sendo uma gaussiana 
