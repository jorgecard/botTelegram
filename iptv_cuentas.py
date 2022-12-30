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

onedrive_link = "https://1drv.ms/x/s!AuH0cqh1REoYnh0TVaXnn9QZQ6_7?e=YohsZS"
onedrive_direct_link = create_onedrive_directdownload(onedrive_link)
print(f"Original OneDriveLink: {onedrive_link}")
print(f"Generated Direct Download Link: {onedrive_direct_link}")
df = pd.read_excel(onedrive_direct_link, sheet_name = "Magis", skiprows=3)

df.drop(["Unnamed: 8", "Vendedor", "Créditos", "$"],axis=1, inplace=True) # borramos las columnas inservibles

# Índice
df = df.set_index(["#"])

# Observaciones
df['Observaciones'] = df['Observaciones'].astype(str)
df['Observaciones'] = df['Observaciones'].apply(lambda x: x.replace('nan',''))

#Borramos clientes duplicados
df_cl = df.drop_duplicates(['Usuario'], keep='last', inplace=False)

#Clientes por vencer
n_days = 3

fecha_hoy = datetime.datetime.now()
fecha_hoy = fecha_hoy.date() + datetime.timedelta(days=0)
fecha_hoy = pd.to_datetime(fecha_hoy)
fecha_hoy

mask = (df_cl['Fecha exp'] >= fecha_hoy) & (df_cl['Fecha exp'] <= (fecha_hoy + pd.Timedelta(days=n_days)))
df_vencer=df_cl.loc[mask]
df_vencer["Días de vigencia"] = df_vencer["Fecha exp"] - fecha_hoy
df_vencer

# Usuarios
df_usuarios = pd.read_excel(onedrive_direct_link, sheet_name = "Usuarios", skiprows=0)
df_usuarios.drop(["Contraseña"],axis=1, inplace=True) # borramos las columnas inservibles
# Cliente (Nombres)
df_usuarios['Cliente'] = df_usuarios['Cliente'].astype(str)
df_usuarios['Cliente'] = df_usuarios['Cliente'].apply(lambda x: x.replace('nan',''))

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

string = ""
for index, registro in df_vencer.iterrows():
    exp = (df_vencer.at[index, "Fecha exp"])
    user = (df_vencer.at[index, "Usuario"])
    días = str(df_vencer.at[index, "Fecha exp"] - fecha_hoy)
    días = días.replace('days 00:00:00','días')
    buscador = True                # bandera
    for i, registro in df_usuarios.iterrows():
        if user == str(df_usuarios.at[i, "Usuario"]):
            cliente = df_usuarios.at[i, "Cliente"]
            whpp = df_usuarios.at[i, "Whpp"]
            plataforma = df_usuarios.at[i, "Plataforma"]
            buscador = False
            break
        else:
            cliente = ''
            whpp = ""
            plataforma = ""
    if buscador:
        print("usuario no encontrado: " + user)
    if cliente == "":
        cliente = user
    cliente = string_cliente(cliente)
    mensaje = f"Buen día estimado usuario {cliente}, este mensaje es para recordarle que su cuenta en la plataforma {plataforma} tiene {días} de vigencia. Agradecemos su gentil preferencia."
    mensaje = mensaje.replace(" ", "%20")
    mensaje = mensaje.replace("í", "%C3%AD")
    num = whpp.replace("wa.me/", "")
    # https://api.whatsapp.com/send?phone=593555555&text=Hola%20texto
    string = f"{string} \n \n{cliente}\nhttps://api.whatsapp.com/send?phone={num}&text={mensaje}"
print(string)
