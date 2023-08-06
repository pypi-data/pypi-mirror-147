class INDECError(Exception):
    pass

class WaveError(Exception):
    pass

class TrimesterError(Exception):
    pass

class YearError(Exception):
    pass

class AdvertenciaINDEC(Warning):
    pass

def get_microdata(year, trimester_or_wave, type='hogar', advertencias=True, download=False):
    """Genera un DataFrame con los microdatos de la EPH.
       Hasta 2018, usa los datos recopilados por Humai (ihum.ai).
       Desde 2019, los descarga desde la página de INDEC (salvo que cambie el formato del nombre de los archivos y links, debería andar para años posteriores, pero se probó hasta 2021)

    Args:
        @year (int): Año de la EPH
        @trimester_or_wave (int): Trimestre (si año >= 2003) u onda (si año < 2003)
        @type (str, optional): Tipo de base (hogar o individual). Default: 'hogar'.
        @advertencias (bool, optional): Mostrar advertencias metodológicas de INDEC. Defaults to True.
        @download (bool, optional): Descargar los csv de las EPH (en vez de cargarlos directamente a la RAM). Defaults to False.

    Returns:
        pandas.DataFrame: DataFrame con los microdatos de la EPH
    """
    
    from zipfile import ZipFile
    from io import BytesIO
    import os
    import wget
    import fnmatch
    import requests
    import pandas as pd
    
    handle_exceptions_microdata(year, trimester_or_wave, type, advertencias)
    
    if year < 2019:
        if year >= 2003 and trimester_or_wave is not None:
            url = f'https://datasets-humai.s3.amazonaws.com/eph/{type}/base_{type}_{year}T{trimester_or_wave}.csv'
        
        elif year < 2003  and trimester_or_wave is not None:
            url = f'https://datasets-humai.s3.amazonaws.com/eph/{type}/base_{type}_{year}O{trimester_or_wave}.csv'
        if download:
            filename = url.split('/')[-1]
            
            if os.path.exists(filename):
                os.remove(filename)
                
            filename = wget.download(url)
            df = pd.read_csv(filename, low_memory=False, encoding='unicode_escape')
        else:
            df = pd.read_csv(url, low_memory=False, encoding='unicode_escape')
    elif year >= 2019:
        if trimester_or_wave == 1:
            suffix = 'er' 
        elif trimester_or_wave == 2:
            suffix = 'do'
        elif trimester_or_wave == 3:
            suffix = 'er'
        elif trimester_or_wave == 4:
            suffix = 'to'
            
        try:
            query_str = f"https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_usu_{trimester_or_wave}_Trim_{year}_txt.zip"
            r = requests.get(query_str)
            print('Descomprimiendo...(si tarda mas de 1 min reintentar, seguramente la página de INDEC esté caída)', end='\r')
            files = ZipFile(BytesIO(r.content))
        except:
            try:
                query_str = f'https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_usu_{trimester_or_wave}{suffix}_Trim_{year}_txt.zip'
                r = requests.get(query_str)
                print('Descomprimiendo...(si tarda mas de 1 min reintentar, seguramente la página de INDEC esté caída)', flush=True, end='\r')
                files = ZipFile(BytesIO(r.content))
            except:
                try:
                    query_str = f'https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_usu_{trimester_or_wave}{suffix}Trim_{year}_txt.zip'
                    r = requests.get(query_str)
                    print('Descomprimiendo...(si tarda mas de 1 min reintentar, seguramente la página de INDEC esté caída)', flush=True, sep='', end='\r')
                    files = ZipFile(BytesIO(r.content))
                except:
                    raise 
        try:
            df = pd.read_csv(files.open(f"EPH_usu_{trimester_or_wave}{suffix}_Trim_{year}_txt/usu_{type}_T{trimester_or_wave}{str(year)[-2:]}.txt.txt"), delimiter=';')
            return df
        except:
            try:
                for file in files.namelist():
                    if fnmatch.fnmatch(file, f'*{type}*.txt'):
                        print('Importando a pandas...')
                        df = pd.read_csv(files.open(file), low_memory=False, delimiter=';')
                        return df
            except:
                raise ValueError('No se encontró el archivo de microdatos en la base de INDEC')
                
    return df


def handle_exceptions_microdata(year, trimester_or_wave, type, advertencias):
    
    import warnings
    
    if not isinstance(year,int):
        raise YearError("El año tiene que ser un numero")
    
    if not isinstance(trimester_or_wave,int) and not isinstance(trimester_or_wave,int) :
        raise TrimesterError("Debe haber trimestre desde 2003 en adelante (1, 2, 3 o 4) \
                          u onda si es antes de 2003 (1 o 2)")
    
    if (isinstance(trimester_or_wave,int) and trimester_or_wave not in [1,2,3,4]) and (year >= 2003):
        raise TrimesterError("Trimestre/Onda inválido (debe ser entre 1 y 4)")
    
    # if (isinstance(trimester_or_wave,int) and trimester_or_wave not in [1,2]) and (year <= 2003):
    #     raise WaveError("Onda inválida (debe ser 1 o 2)")
    
    if type not in ['individual','hogar']:
        raise TypeError("Seleccione un tipo de base válido: individual u hogar")
    
    if year==2007 and trimester_or_wave==3:
        raise INDECError("\nLa informacion correspondiente al tercer trimestre \
2007 no está disponible ya que los aglomerados Mar del Plata-Batan, \
Bahia Blanca-Cerri y Gran La Plata no fueron relevados por causas \
de orden administrativo, mientras que los datos correspondientes al \
Aglomerado Gran Buenos Aires no fueron relevados por paro del \
personal de la EPH")
        
    if (year == 2015 and trimester_or_wave in [3,4]) |  (year ==2016 and trimester_or_wave==3):
        raise INDECError("En el marco de la emergencia estadistica, el INDEC no publicó la base solicitada. \
                 mas información en: https://www.indec.gob.ar/ftp/cuadros/sociedad/anexo_informe_eph_23_08_16.pdf")
    
    if (year == 2003 and trimester_or_wave in [1, 2]):
        raise INDECError('Debido al cambio metodológico en la EPH, en 2003 solo se realizó la encuesta para el 3er y 4to trimestre')
    
    if advertencias:
        if year >= 2007 and year <= 2015:
            warnings.warn('''\n
Las series estadisticas publicadas con posterioridad a enero 2007 y hasta diciembre \
2015 deben ser consideradas con reservas, excepto las que ya hayan sido revisadas en \
2016 y su difusion lo consigne expresamente. El INDEC, en el marco de las atribuciones \
conferidas por los decretos 181/15 y 55/16, dispuso las investigaciones requeridas para \
establecer la regularidad de procedimientos de obtencion de datos, su procesamiento, \
elaboracion de indicadores y difusion.
Más información en: https://www.indec.gob.ar/ftp/cuadros/sociedad/anexo_informe_eph_23_08_16.pdf 
(Se puede desactivar este mensaje con advertencias=False)\n-------------------------------------------------------------------------------------------------'''
, AdvertenciaINDEC, stacklevel=3)

        