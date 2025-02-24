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

    # Días de vigencia
    fecha_hoy = datetime.datetime.now()
    df["Días de vigencia"] = (df["Fecha exp"] - fecha_hoy).dt.days  # Extrae solo los días y convierte a entero
    df["Días de vigencia"] = df["Días de vigencia"].fillna(-1000).astype(int)

    # Merge df with df_usuarios on "Usuario" column
    df = df.merge(df_usuarios[['Usuario', 'Cliente', 'Whpp', 'Plataforma']], on='Usuario', how='left')

    return df


def por_vencer(n_days=10):
    
    df = analysis()

    # Obtener la fecha actual sin horas
    fecha_hoy = pd.Timestamp.today().normalize()

    # Filtrar usuarios cuyo vencimiento está dentro del rango de días especificado
    mask = (df['Fecha exp'] >= fecha_hoy - pd.Timedelta(days=2)) & (df['Fecha exp'] <= (fecha_hoy + pd.Timedelta(days=n_days)))
    df_vencer = df[mask].copy()

    # Ordenar por días de vigencia en orden ascendente
    df_vencer.sort_values(by=['Días de vigencia'], ascending=True, inplace=True)

    # Construcción del mensaje
    string = ""
    for _, row in df_vencer.iterrows():
        # Información del cliente
        string += f"\n\n{row['Cliente']}\n{row['Días de vigencia']} días"

        # Agregar observaciones si existen
        if pd.notna(row['Observaciones']):
            string += f"\n{row['Observaciones']}"

        # Mensaje para WhatsApp
        message = (
            f"Buen día estimado/a {row['Cliente']}, este mensaje es para recordarle que su usuario "
            f"{row['Usuario']} en la plataforma {row['Plataforma']} tiene {row['Días de vigencia']} "
            f"días de vigencia. Agradecemos su gentil preferencia."
        )

        # Formatear mensaje para URL de WhatsApp
        message = (
            message.replace(" ", "%20")
            .replace("í", "%C3%AD")
        )

        # Enlace de WhatsApp
        whatsapp_link = f"https://api.whatsapp.com/send?phone={row['Whpp']}&text={message}"
        string += f"\n{whatsapp_link}"

    print(f"Telegram: {string}")
    
    # Check if string exceeds the maximum length for Telegram messages
    if len(string) > 4096:
        string = string[:4093] + "..."
    
    return string, df_vencer

def activos():
    
    df = analysis()

    # Obtener la fecha actual sin horas
    fecha_hoy = pd.Timestamp.today().normalize()

    mask = (df['Fecha exp'] >= fecha_hoy)
    df_activos = df[mask].copy()
    df_activos.sort_values(by=['Días de vigencia'], ascending=True, inplace=True)
    
    # Construcción del mensaje
    string = ""
    for _, row in df_activos.iterrows():
        # Información del cliente
        string += f"\n\n{row['Cliente']}\n{row['Usuario']}\n{row['Días de vigencia']} días"

        # Agregar observaciones si existen
        if pd.notna(row['Observaciones']):
            string += f"\n{row['Observaciones']}"

        string += f"\n{''}"

    print(f"Telegram: {string}")
    
    # Check if string exceeds the maximum length for Telegram messages
    if len(string) > 4096:
        string = string[:4093] + "..."
    
    return string, df_activos

def vencidos():
    
    df = analysis()

    # Obtener la fecha actual sin horas
    fecha_hoy = pd.Timestamp.today().normalize()

    mask = (df['Fecha exp'] < fecha_hoy)
    df_vencidos = df[mask].copy()
    df_vencidos = df_vencidos.sort_values(by=['Días de vigencia'], ascending=False, inplace=False)
        
    # Construcción del mensaje
    string = ""
    for _, row in df_vencidos.iterrows():
        # Información del cliente
        string += f"\n\n{row['Cliente']}\n{row['Usuario']}\n{row['Días de vigencia']} días"

        # Agregar observaciones si existen
        if pd.notna(row['Observaciones']):
            string += f"\n{row['Observaciones']}"

        # Mensaje para WhatsApp
        message = (
            f"Buen día estimado/a {row['Cliente']}, este mensaje es para recordarle que su usuario "
            f"{row['Usuario']} en la plataforma {row['Plataforma']} tiene {row['Días de vigencia']} "
            f"días de vigencia. Agradecemos su gentil preferencia."
        )

        # Formatear mensaje para URL de WhatsApp
        message = (
            message.replace(" ", "%20")
            .replace("í", "%C3%AD")
        )

        # Enlace de WhatsApp
        whatsapp_link = f"https://api.whatsapp.com/send?phone={row['Whpp']}&text={message}"
        string += f"\n{whatsapp_link}"

    print(f"Telegram: {string}")
    
    # Check if string exceeds the maximum length for Telegram messages
    if len(string) > 4096:
        string = string[:4093] + "..."
    
    return string, df_vencidos


def observaciones():
    
    df = analysis()
    
    # Obtener la fecha actual sin horas
    fecha_hoy = pd.Timestamp.today().normalize()

    mask = (df['Fecha exp'] >= fecha_hoy) & (df['Fecha exp'] <= (fecha_hoy + pd.Timedelta(days=100))) & (df['Observaciones'] != "")
    df_observaciones=df[mask].copy()
    df_observaciones = df_observaciones.sort_values(by=['Días de vigencia'], ascending=True, inplace=False)
    # df_observaciones

    # Construcción del mensaje
    string = ""
    for _, row in df_observaciones.iterrows():
        # Información del cliente
        string += f"\n\n{row['Cliente']}\n{row['Usuario']}\n{row['Días de vigencia']} días"

        # Agregar observaciones si existen
        if pd.notna(row['Observaciones']):
            string += f"\n{row['Observaciones']}"

        # Mensaje para WhatsApp
        message = (
            f"Buen día estimado/a {row['Cliente']}, este mensaje es para recordarle que su usuario "
            f"{row['Usuario']} en la plataforma {row['Plataforma']} tiene {row['Días de vigencia']} "
            f"días de vigencia. Agradecemos su gentil preferencia."
        )

        # Formatear mensaje para URL de WhatsApp
        message = (
            message.replace(" ", "%20")
            .replace("í", "%C3%AD")
        )

        # Enlace de WhatsApp
        whatsapp_link = f"https://api.whatsapp.com/send?phone={row['Whpp']}&text={message}"
        string += f"\n{whatsapp_link}"

    print(f"Telegram: {string}")
    
    # Check if string exceeds the maximum length for Telegram messages
    if len(string) > 4096:
        string = string[:4093] + "..."
    
    return string, df_observaciones
