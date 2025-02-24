import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import base64

from time import sleep

def create_onedrive_directdownload (onedrive_link):
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    return resultUrl

# String Cliente (arreglamos si dice "Cliente o REf")
def string_cliente(cliente):
    pos_ref = cliente.find("Ref")
    if pos_ref == -1:
        pos_ref = cliente.find("REF")
    if pos_ref == -1:
        pos_ref = cliente.find("ref")
    if pos_ref != -1:
        resultCliente = cliente[: pos_ref-1]
    else:
        resultCliente = cliente
    pos_cli = resultCliente[:].find("Cliente")     #busca en todo el string
    if pos_cli != -1:
        resultCliente = resultCliente.replace("Cliente ", "")
    return resultCliente


def analysis():
    # Fuente:
    onedrive_link = "https://1drv.ms/x/s!AuH0cqh1REoYnh0TVaXnn9QZQ6_7?e=YohsZS"
    onedrive_direct_link = create_onedrive_directdownload(onedrive_link)
    # print(f"Original OneDriveLink: {onedrive_link}")
    # print(f"Generated Direct Download Link: {onedrive_direct_link}")
    
    # Usuarios -------------------
    df_usuarios = pd.read_excel(onedrive_direct_link, sheet_name = "Usuarios", skiprows=0)
    df_usuarios.drop(["Contraseña"],axis=1, inplace=True) # borramos las columnas inservibles
    # # Cliente (Nombres)
    # df_usuarios['Cliente'] = df_usuarios['Cliente'].astype(str)
    # df_usuarios['Cliente'] = df_usuarios['Cliente'].apply(lambda x: x.replace('nan',''))
    
    # Bases ----------------------
    df = pd.read_excel(onedrive_direct_link, sheet_name = "Magis", skiprows=3)
    df.drop(["Unnamed: 8", "Vendedor", "Créditos", "$"],axis=1, inplace=True) # borramos las columnas inservibles
    df.drop(["#", "CRÉDITOS", "MONTO", "VENDEDOR"],axis=1, inplace=True) # borramos las columnas inservibles
    df2 = pd.read_excel(onedrive_direct_link, sheet_name = "DirecTV Go", skiprows=1)
    df2.drop(["#", "Fecha de pago",  "Correo", "Contraseña"],axis=1, inplace=True) # borramos las columnas inservibles

    # Unimos bases
    df = pd.concat([df, df2], axis=0)

    # Borramos clientes duplicados
    df.drop_duplicates(['Usuario'], keep='last', inplace=True)

    # # Observaciones
    # df['Observaciones'] = df['Observaciones'].astype(str)
    # df['Observaciones'] = df['Observaciones'].apply(lambda x: x.replace('nan',''))

    # Días de vigencia
    fecha_hoy = datetime.datetime.now()
    df["Días de vigencia"] = (df["Fecha exp"] - fecha_hoy).dt.days  # Extrae solo los días y convierte a entero
    df["Días de vigencia"] = df["Días de vigencia"].fillna(-1000).astype(int)

    # Merge df with df_usuarios on "Usuario" column
    df = df.merge(df_usuarios[['Usuario', 'Cliente', 'Whpp', 'Plataforma']], on='Usuario', how='left')

    return df


def por_vencer(n_days=10):
    df = analysis()

    fecha_hoy = datetime.datetime.now()
    fecha_hoy = fecha_hoy.date() + datetime.timedelta(days=0)
    fecha_hoy = pd.to_datetime(fecha_hoy)

    mask = (df['Fecha exp'] >= fecha_hoy) & (df['Fecha exp'] <= (fecha_hoy + pd.Timedelta(days=n_days)))
    df_vencer = df[mask]
    df_vencer.sort_values(by=['Días de vigencia'], ascending=True, inplace=True)

    string = ""
    for index, row in df_vencer.iterrows():
        string = f"{string} \n \n{row['Cliente']}\n{row['Días de vigencia']}"
        if pd.notna(row['Observaciones']):
            string = f"{string}\n{row['Observaciones']}"
        else:
            pass
        message = message = f"Buen día estimado/a {row['Cliente']}, este mensaje es para recordarle que su usuario {row['Usuario']} en la plataforma {row['Plataforma']} tiene {row['Días de vigencia']} días de vigencia. Agradecemos su gentil preferencia."
        message = message.replace(" ", "%20")
        message = message.replace("í", "%C3%AD")
        string = f"{string}\nhttps://api.whatsapp.com/send?phone={row['Whpp']}&text={message}"
    
    # print(f"Telegram: {string}")
    return string, df_vencer

def activos():
    df = analysis()

    fecha_hoy = datetime.datetime.now()
    fecha_hoy = fecha_hoy.date() + datetime.timedelta(days=0)
    fecha_hoy = pd.to_datetime(fecha_hoy)

    mask = (df['Fecha exp'] >= fecha_hoy)
    df_activos = df[mask]
    df_activos.sort_values(by=['Días de vigencia'], ascending=True, inplace=True)

    string = ""
    for index, registro in df_activos.iterrows():
        user = (df_activos.at[index, "Usuario"])
        cliente = (df_activos.at[index, "Cliente"])
        cliente0 = (df_activos.at[index, "Cliente0"])
        whpp = df_activos.at[index, "Whpp"]
        num = whpp.replace("wa.me/", "")
        plataforma = df_activos.at[index, "Plataforma"]
        días = str(df_activos.at[index, "Días de vigencia"])
        días = días.replace('days 00:00:00', 'días')
        observaciones = (df_activos.at[index, "Observaciones"])
        if observaciones != "":
            string = f"{string} \n \n Cliente: {cliente} - {cliente0}\n Plataforma: {plataforma} \n{días}\n{observaciones}"
        else:
            string = f"{string} \n \n Cliente: {cliente} - {cliente0}\n Plataforma: {plataforma} \n{días}"
    # print(f"Telegram: {string}")
    return string, df_activos

def vencidos():
    df = analysis()

    fecha_hoy = datetime.datetime.now()
    fecha_hoy = fecha_hoy.date() + datetime.timedelta(days=0)
    fecha_hoy = pd.to_datetime(fecha_hoy)

    mask = (df['Fecha exp'] < fecha_hoy)
    df_vencidos = df[mask]
    df_vencidos = df_vencidos.sort_values(by=['Días de vigencia'], ascending=False, inplace=False)
    df_vencidos = df_vencidos.head(15)

    string = ""
    for index, registro in df_vencidos.iterrows():
        user = (df_vencidos.at[index, "Usuario"])
        cliente = (df_vencidos.at[index, "Cliente"])
        cliente0 = (df_vencidos.at[index, "Cliente0"])
        whpp = df_vencidos.at[index, "Whpp"]
        whpp = str(whpp)
        num = whpp                      # para que se borre el anterior
        if whpp != "nan":
            num = str(whpp.replace("wa.me/", ""))
        plataforma = df_vencidos.at[index, "Plataforma"]
        días = str(df_vencidos.at[index, "Días de vigencia"])
        días = días.replace('days +00:00:00', 'días')
        observaciones = (df_vencidos.at[index, "Observaciones"]) + "\n" +"num: " + num
        mensaje = f"{cliente}, {plataforma}."
        mensaje = mensaje.replace(" ", "%20")
        mensaje = mensaje.replace("í", "%C3%AD")
        string = f"{string} \n \n{cliente0}\n{días}\n{observaciones}\nhttps://api.whatsapp.com/send?phone={num}&text={mensaje}"
        df_vencidos
    return string, df_vencidos


def observaciones():
    
    df = analysis()
    
    fecha_hoy = datetime.datetime.now()
    fecha_hoy = fecha_hoy.date() + datetime.timedelta(days=0)
    fecha_hoy = pd.to_datetime(fecha_hoy)

    mask = (df['Fecha exp'] >= fecha_hoy) & (df['Fecha exp'] <= (fecha_hoy + pd.Timedelta(days=100))) & (df['Observaciones'] != "")
    df_observaciones=df[mask]
    df_observaciones = df_observaciones.sort_values(by=['Días de vigencia'], ascending=True, inplace=False)
    # df_observaciones

    string = ""
    for index, registro in df_observaciones.iterrows():
        user = (df_observaciones.at[index, "Usuario"])
        cliente = (df_observaciones.at[index, "Cliente"])
        cliente0 = (df_observaciones.at[index, "Cliente0"])
        whpp = df_observaciones.at[index, "Whpp"]
        whpp = str(whpp)
        if whpp != "nan":
            num = str(whpp.replace("wa.me/", ""))
        plataforma = df_observaciones.at[index, "Plataforma"]
        días = str(df_observaciones.at[index, "Días de vigencia"])
        días = días.replace('days 00:00:00','días')
        observaciones = (df_observaciones.at[index, "Observaciones"])
        mensaje = f"Buen día estimado usuario {cliente}, queríamos informarle que en {plataforma}."
        mensaje = mensaje.replace(" ", "%20")
        mensaje = mensaje.replace("í", "%C3%AD")
        string = f"{string} \n \n{cliente0}\n{días}\n{observaciones}\nhttps://api.whatsapp.com/send?phone={num}&text={mensaje}"
    return string, df_observaciones
