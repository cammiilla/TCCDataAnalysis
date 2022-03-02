################# imports  ################
import os, sys #biblioteca para manipular arquivos e pastas
import numpy as np
from astropy.io import ascii, fits
from astropy.table import Table
import pandas as pd

################# lista todos os arquivos que tem no diretório indicado ################
diretorio = '/media/new-drive/optical-data/DESzxcorr/FITS/64-stars-dr2'
'''
# para verificar os arquivos contidos no diretório descomente essa secção 
for diretorio, subpastas, arquivos in os.walk(diretorio):
    for arquivo in arquivos:
        print(os.path.join(diretorio, arquivo))
'''
filename_list = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]

qnty_arquivos_lidos_por_intervalo = 1000

#lista com o particionamento da leitura dos arquivos
intervalos = list(np.arange(0, len(filename_list), qnty_arquivos_lidos_por_intervalo,dtype=int))
intervalos.append(len(filename_list))

for w in range(len(intervalos)-1):
    inicio = intervalos[w]
    fim = intervalos[w+1]
    table_list = []
    for j in range (inicio,fim):
        #lê o arquivo i que está contido no diretório
        path = os.path.join(diretorio,filename_list[j])
        df = Table.read(path).to_pandas()

        #escolhe somente as colunas de interesse da tabela 
        df_filtrado = pd.DataFrame()
        df_filtrado['COADD_OBJECT_ID'] = df['COADD_OBJECT_ID']
        df_filtrado['RA'] = df['RA']
        df_filtrado['DEC'] = df['DEC']
        df_filtrado['HPIX_64'] = df['HPIX_64']
        df_filtrado['CLASS_STAR_G'] = df['CLASS_STAR_G']
        df_filtrado['CLASS_STAR_R'] = df['CLASS_STAR_R']
        df_filtrado['CLASS_STAR_I'] = df['CLASS_STAR_I']
        df_filtrado['CLASS_STAR_Z'] = df['CLASS_STAR_Z']
        df_filtrado['CLASS_STAR_Y'] = df['CLASS_STAR_Y']
        df_filtrado['MAG_AUTO_G'] = df['MAG_AUTO_G']
        df_filtrado['MAG_AUTO_R'] = df['MAG_AUTO_R']
        df_filtrado['MAG_AUTO_I'] = df['MAG_AUTO_I']
        df_filtrado['MAG_AUTO_Z'] = df['MAG_AUTO_Z']
        df_filtrado['MAG_AUTO_Y'] = df['MAG_AUTO_Y']
        df_filtrado['COLOR_g-r'] = df['MAG_AUTO_G']-df['MAG_AUTO_R']
        df_filtrado['COLOR_r-i'] = df['MAG_AUTO_R']-df['MAG_AUTO_I']
        df_filtrado['COLOR_i-z'] = df['MAG_AUTO_I']-df['MAG_AUTO_Z']
        df_filtrado['COLOR_z-Y'] = df['MAG_AUTO_Z']-df['MAG_AUTO_Y']
        table_list.append(df_filtrado)


    des_data_partitioned = pd.concat(table_list, axis=0, ignore_index=True)
    des_data_partitioned_table = Table.from_pandas(des_data_partitioned)
    des_data_partitioned_table.write('/media/new-drive/CamilaCardoso/DES/DES_DR2_interval_'+str(inicio)+'_'+str(fim)+'.fits') 
    
    
################# lê e concatena todas as tabelas que tem no diretório indicado ################
diretorio = '/media/new-drive/CamilaCardoso/DES/'
table_list = []
for diretorio, subpastas, arquivos in os.walk(diretorio):
    for arquivo in arquivos:
        df = Table.read(os.path.join(diretorio, arquivo)).to_pandas()
        table_list.append(df)
        print(os.path.join(diretorio, arquivo))
des_data = pd.concat(table_list, axis=0, ignore_index=True)