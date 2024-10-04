from genericpath import isdir
from pyrogram import Client, filters
from pyrogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import ReplyKeyboardMarkup
import aiogram
from aiogram import Bot, Dispatcher, types 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from os.path import exists
from json import loads,dumps 
from pathlib import Path, PurePath
from os import listdir
from os import mkdir
from os import unlink
from os.path import isfile, join
from datetime import timedelta
from random import randint
from re import findall
from bs4 import BeautifulSoup
from py7zr import SevenZipFile, FILTER_COPY
from multivolumefile import MultiVolume
from zipfile import ZipFile
from io import BufferedReader
from py7zr import SevenZipFile
from move_profile import move_to_profile
from urllib.parse import quote
from time import time, localtime
from yarl import URL
import re
import asyncio
import aiohttp_socks
import aiohttp
import tgcrypto
import requests
import traceback
import threading
import time
import os
import ssl
import http.server
import socketserver
import yt_dlp
from uptodl import search, get_info
import psutil
from upload import NextcloudClient
import json
import shutil
import certifi
from concurrent.futures import ThreadPoolExecutor
from configs import api_id, api_hash, token
import sqlite3

user_data = {}

ssl._create_default_https_context = ssl._create_unverified_context

def split_file(file_path, chunk_size):
    """Divide un archivo en chunks y los almacena en una lista.
    
    Args:
        file_path: La ruta del archivo a dividir.
        chunk_size: El tamaño de cada chunk en bytes.
    
    Returns:
        Una lista de rutas de archivo para cada chunk.
    """
    file_path = Path(file_path)
    file_name = file_path.name
    
    chunks = []
    with open(file_path, 'rb') as file:
        chunk_num = 0
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            chunk_file_name = f"{file_name}_part{chunk_num}"
            chunk_file_path = file_path.parent / chunk_file_name
            chunks.append(chunk_file_path)
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_num += 1
    
    return chunks

def sevenzip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+".7z"), mode="wb", volume=volume, ext_digits=ext_digits
    ) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

admins = ['JAGB2021']
JAGB2021 = admins
bot = Client("client",api_id,api_hash,bot_token=token) 
CONFIG = {}
global_conf = {
       "token": "",
       "host": ""
   }

traffic = {
"downlink":"0",
"uplink":"0"}

traffico = 0

print(global_conf["host"])

stream_sites = ['youtube.com', 'xnxx.com', 'twitch.tv', 'dailymotion.com']

SECOND = 0

def getuser(username):
    try:
        user_info = CONFIG[username]
        return user_info
    except:
        return None

def createuser(username):
    CONFIG[username] = {"username":"","password":"","proxy":"","zips":"99","calidad":"480p","automatic":"off","server":"1547","mode":"moodle"}

def deleteuser(username):

    if username in CONFIG:
        del CONFIG[username]
        print(f"✅Usuario {username} eliminado de la configuración.")
    else:
        print(f"❌El usuario {username} no existe en la configuración.")

async def limite_msg(text,user_id):
    lim_ch = 1500
    text = text.splitlines() 
    msg = ''
    msg_ult = '' 
    c = 0
    for l in text:
        if len(msg +"\n" + l) > lim_ch:     
            msg_ult = msg
            await bot.send_message(user_id,msg) 
            msg = ''
        if msg == '':   
            msg+= l
        else:       
            msg+= "\n" +l   
        c += 1
        if len(text) == c and msg_ult != msg:
            await bot.send_message(user_id,msg)

def sizeof_folder(ruta):
    tamano_total = 0
    for raiz, directorios, archivos in os.walk(ruta):
        for archivo in archivos:
            ruta_archivo = os.path.join(raiz, archivo)
            tamano_archivo = os.path.getsize(ruta_archivo)
            tamano_total += tamano_archivo
    return tamano_total

def files_formatter(user_id):
    if not os.path.exists(str(user_id)):
        os.mkdir(str(user_id))
    try:
        rut = user_id
        filespath = Path(str(rut))
        result = []
        dirc = []
        final = []
        for p in os.listdir(filespath):
            if Path(f"{filespath}/{p}").is_file():
                result.append(p)
            elif Path(f"{filespath}/{p}").is_dir():
                dirc.append(p)
        result.sort()
        dirc.sort()
        msg = "**Directorio actual**"+f'\n\n `./{rut}`\n\n'
        if result == [] and dirc == [] :
            return msg , final
        for k in dirc:
            final.append(k)
        for l in result:
            final.append(l)
        i = 0
        for n in final:
            if os.path.isdir(f"{rut}/{n}"):
                size = sizeof_folder(f"{rut}/{n}")
                msg+=f"**{i}**🗂`{n}`\n 🔎__/cd_{i}__🔎 🗑️__/rm_{i}__🗑️\n\n"
            elif os.path.isfile(f"{rut}/{n}"):
                size = Path(f"{rut}/{n}").stat().st_size
                msg+=f"**{i}**📋`{n}`\n 📤__/up_{i}__📤 🗑️__/rm_{i}__🗑️ **[{sizeof_fmt(size)}]**\n\n"
            i+=1
        msg+= f"\nEliminar Directorio Raiz\n**/delall**"
        return msg , final
    except Exception as e:
        print(str(e))

def filezip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+"zip"), mode="wb", volume=volume, ext_digits=0) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

@bot.on_message()                
async def new_event(client: Client, message: Message):
    global traffico

    msg = message.text
    id = message.from_user.id
    username = message.from_user.username

    @bot.on_callback_query(filters.regex(r"^/download"))
    async def download_callback(client, query):
        url = url_temp["Actual_url"]  # Obtén la URL almacenada en el diccionario
    # Llama a la función download_file() con los parámetros necesarios
        await download_file(url, id, query.message, callback=download_func)  # Usa query.message para el mensaje
        await query.answer("📥Descargando archivo📥")
    if msg is None:
        msg = ""

    if getuser(username):
        if exists(str(id)):
            pass
        else:
            mkdir(str(id))
        pass
    else:
        if username in admins:
            createuser(username)
        else:
            await bot.send_message(id,f"⭕️**@{username} no tienes acceso a este bot.**")
            return
    if "/start" in msg:
        await message.reply(f"✅Bienvenido @{username}. **Este bot es capaz de subir 📥 a la nube.\n\nUse /config para ⚙️ configurar host token.\nUse /command para ver los comandos🎛️")

    elif "/calidad" in msg:
        calidad = msg.split(" ")[1]
        CONFIG[username]["calidad"] = calidad
        await bot.send_message(id, "✅Se a actualizado la preferencia de calidad")

    elif "/zips" in msg:
        zips = msg.split(" ")[1]
        CONFIG[username]["zips"] = zips
        await bot.send_message(id,"📦**Se guardo correctamente el tamaño de los zips.**")

    elif "/server" in msg:
        server = msg.split(" ")[1]
        CONFIG[username]["server"] = server
        await bot.send_message(id, "✅Server configurado")

    elif "/addadmin" in msg:
        admin = msg.split()[1]
        if admin in admins:
            await bot.send_message(id, "⭕️El usuario ya es admin")
        else:
            admins.append(admin)
            await bot.send_message(id, f"✅Ahora {admin} es admin del bot")

    elif "/removeadmin" in msg:
        try:
            admin = msg.split()[1]
            if admin in admins:
                admins.remove(admin)
                deleteuser(username)
                admins = msg.split()[1]
                await bot.send_message(id, f"❌Se eliminó a {admin} como admin del bot.")
            else:
                await bot.send_message(id, f"⭕️El usuario {admin} no es admin del bot.")
        except:
            admin.remove(MarlonSu)
            await bot.send_message(id, f"❌Error no puedes dejar de usarme")

    elif "/addsite" in msg:
        site = msg.split()[1]
        if site in stream_sites:
            await bot.send_message(id, "⭕️Ya estan habilitadas las descargas de ese sitio")
        else:
            stream_sites.append(site)
            await bot.send_message(id, f"✅Ahora el bot tambien descargara de {site} ")

    elif "/proxy" in msg:
        zips = msg.split(" ")[1]
        proxy = iprox(zips.replace("socks5://",""))
        CONFIG[username]["proxy"] = f"socks5://{proxy}"
        await bot.send_message(id,"✅**Se guardo correctamente el proxy.**")

    elif "/offproxy" in msg:
        CONFIG[username]["proxy"] = ""
        await bot.send_message(id,"❌**Se eliminó correctamente el proxy.**")

    elif "/add" in msg:
        if username in admins:  
            usernames = msg.split(" ")[1]  
            createuser(usernames)  
            await bot.send_message(id, f"✅@{usernames} fue añadido al bot.")
        else:
           await bot.send_message(id, "❌No puedes usar este comando. Es solo para administradores.")
           return

    elif "/ban" in msg:
        if username in admins:  
            usernames = msg.split(" ")[1]  
            deleteuser(usernames)  
            await bot.send_message(id, f"✅ @{usernames} fue eliminado del bot.")
        else:
            await bot.send_message(id, "❌ No puedes usar este comando. Es solo para administradores.")
            return
        
    elif "/auto" in msg:
        try:
            if CONFIG[username]["automatic"] == "off":
                CONFIG[username]["automatic"] = "on"
                await bot.send_message(id, "✅Subidas automaticas activadas.")
                
            else:
                CONFIG[username]["automatic"] = "off"
                await bot.send_message(id, "⭕️Subida automatica desactivada")

        except Exception as e:
            await bot.send_message(id, f"❌Error al cambiar el modo automático: {e}")


    elif "/mode" in msg:
        try:
            if CONFIG[username]["mode"] == "moodle":
                CONFIG[username]["mode"] = "uo"
                await bot.send_message(id, "✅Se cambio modo de subida a UO x cookies")
            else:
                CONFIG[username]["mode"] = "moodle"
                await bot.send_message(id, "✅Se cambio el modo a moodle")
        except Exception as e:
            await bot.send_message(id, f"❌Error al cambiar el modo: {e}")

    elif "/seven" in msg:
        if "_" in msg:
            lista = msg.split("_")
        else:
            lista = msg.split(" ")
        msgh = files_formatter(id)
        if len(lista) == 2:
            i = int(lista[1])
            j = str(msgh[1][i])
            if not "." in j:
                h = await bot.send_message(id,f"📦Comprimiendo")
                g = Path(str(id)+"/"+msgh[1][i])
                try:
                    p = await bot.loop.run_in_executor(None,shutil.make_archive,j,"zip",g)
                except:
                    g = str(id)
                    p = await bot.loop.run_in_executor(None,shutil.make_archive,j,"zip",g)
                await h.delete()
                shutil.move(p,str(id))    
                msg = files_formatter(id)
                await limite_msg(msg[0],id)
            else:
                g = str(id)+"/"+msgh[1][i]
                o = await bot.send_message(id,"📦Comprimiendo")
                a = await bot.loop.run_in_executor(None,filezip,g,None,None)
                await o.delete()
                msg = files_formatter(id)
                await limite_msg(msg[0],id)
        elif len(lista) == 3:
            i = int(lista[1])
            j = str(msgh[1][i])
            t = int(lista[2])
            g = str(id)+"/"+msgh[1][i]
            h = await bot.send_message(id,"📦Comprimiendo")
            if not "." in j:
                p = await bot.loop.run_in_executor(None,shutil.make_archive,j,"zip",g)
                await h.edit("...")
                await bot.loop.run_in_executor(None,filezip,g,None)
                a = await bot.loop.run_in_executor(None,sevenzip,p,None,t*1024*1024)
                os.remove(p)
                for i in a :
                    shutil.move(i,user_path)
                await h.delete()
                msg = files_formatter(id)
                await limite_msg(msg[0],id)
                return
            else:
                a = await bot.loop.run_in_executor(None,sevenzip,g,None,t*1024*1024)
                await h.delete()
                msg = files_formatter(id)
                await limite_msg(msg[0],id)
                return

    elif "/config" in msg:
        parts = msg.split(" ", 2)  
        if len(parts) == 3:
            _, host, token = parts  
            global_conf["host"] = host
            global_conf["token"] = token 
            await bot.send_message(id, f"✅Configuración almacenada correctamente: \n 🛰️Host: {host}\n 🧬Token: {token}")
        else:
            await bot.send_message(id, "❌Error al guardar la configuración. Formato correcto: /config host token")

    elif "/next" in msg:
        try:
            parts = msg.split()  
            if len(parts) >= 2:
                index = int(parts[1])  
                count = 1
                directory = os.path.join(str(id))
                if os.path.exists(directory):
                    for item in listdir(directory):
                        if isfile(join(directory, item)):
                            if count == index:
                                filename = item  # Obtener el nombre del archivo
                                msg = await bot.send_message(id, "📤Comenzando a subir📤")
                                await upx(f"{id}/{filename}", msg, username)
                                
                                return  # Termina la ejecución del comando
                            count += 1
                    await bot.send_message(id, f"❌Índice {index} no encontrado.") 
                else:
                    await bot.send_message(id, f"❌La ruta {directory} no existe.") 
            else:
                await bot.send_message(id, "❌Uso incorrecto del comando. Usa __/upx__ <índice>")
        except (IndexError, ValueError):
            await bot.send_message(id, "❌Uso incorrecto del comando. Usa __/upx__ <índice>")
        except Exception as e:
            await bot.send_message(id, f"❌Error al subir el archivo: {e}")						

    elif "/up" in msg:
        try:
            if "_" in msg:
                lista = msg.split("_")
            else:
                lista = msg.split(" ")
            msgh = files_formatter(id)
            parts = msg.split()
            if len(lista) == 2:
                a = str(id)
                b = int(lista[1])
                e = Path(str(id)+"/"+msgh[1][b])
                f = await bot.send_message(id, f"📤Comenzando a subir📤")
                await uploadfile(e, f, username)
                await f.edit("✅ Subida Finalizada")
                msg = files_formatter(id)
                await limite_msg(msg[0], id)
                return  # Termina la ejecución del comando
        except Exception as ex:
            await bot.send_message(id, f"❌Error al subir el archivo: {ex}")

    elif "/rename" in msg:
            parts = msg.split()
            if len(parts) >= 3:
                index = int(parts[1])
                old_filename = parts[1]
                new_filename = parts[2]
            count = 0
            directory = os.path.join(str(id))
            if os.path.exists(directory):
                for item in listdir(directory):
                    if count == index:
                        old_filename = item
                        old_path = os.path.join(directory, old_filename)
                        new_path = os.path.join(directory, new_filename)
                    os.rename(old_path, new_path)
                    await bot.send_message(id, f"✅Archivo {old_filename} renombrado a {new_filename}.")
                    msg = files_formatter(id)
                    await limite_msg(msg[0], id)
                    return

    elif "/delcloud" in msg:
        filename = msg.split(" ")[1]
        msg = await bot.send_message(id, "🗑️Borrando🗑️")
        await delcloud(filename, msg, username)

    elif "/rm" in msg:
        try:
            parts = msg.split("_") if "_" in msg else msg.split(" ")
            index = int(parts[1])  # Obtiene el índice del archivo a borrar
            count = 0
            directory = os.path.join(str(id))
            if os.path.exists(directory):
                for item in listdir(directory):
                    if count == index:
                        file_to_delete = join(directory, item)
                        try:os.unlink(file_to_delete)
                        except:shutil.rmtree(file_to_delete)
                        await bot.send_message(id, f"✅Archivo {item} eliminado correctamente.")
                        msg = files_formatter(id)
                        await limite_msg(msg[0], id)
                        return
                    count += 1
                await bot.send_message(id, f"❌Índice {index} no encontrado.") 
            else:
                await bot.send_message(id, f"❌La ruta {directory} no existe.") 
        except (IndexError, ValueError):
            await bot.send_message(id, "❌Uso incorrecto del comando. Usa __/rm__ [Índice]")

    elif "/help" in msg:
        msg = "Bienvenido soy un bot que descarga y sube a la nube\n\n"	
        msg += "Primero debes configurar el token usando __/config__\n"
        msg += "Si deseas editar el archivo antes de subirlo puedes usar __/seven__ o __/rename__\n"
        msg += "Puedes crear carpetas y gestionar los archivos dentro de ella\n"
        msg += "Si no deseas no deseas gestionar los archivos y que el proceso sea automático usa /auto\n"
        msg += "Para ver todos los comandos del bot usa __/command__\n"
        msg += "Gracias por usarme"
        await bot.send_message(id,msg)

    elif "/command" in msg:
        msg = "start - 🔛Inicia el Bot\n"
        msg += "help - 🆘Muestra ayuda básica sobre el bot\n"
        msg += "config - ⚙️Configurar el host y el token EJ /config /config https://cursos.uo.edu.cu/ 8f9e...\n"
        msg += "ls - 🗂Listar archivos en la base de datos del bot\n"
        msg += "up - 📤Subir a moodle EJ /up [Ítem]\n"
        msg += "cd - 🗂Ir a directorio en raiz EJ:/cd [Ítem]\n"
        msg += "back - 🗂Ir a directorio superior\n"
        msg += "mkdir - 🗂Crear directorio en ruta actual\n"
        msg += "mv - 🗂Mover directorio hacia otro existente en ruta actual\n"
        msg += "rm - 🗑️Borrar archivo o carpeta almacenada en el bot\n"
        msg += "delall - 📛🗑️Borrar todos los archivos y carpetas almacenadas en el bot\n"
        msg += "rename - 📝Renombrar directorios o archivos\n"
        msg += "seven - ✂️Comprimir y cortar directorios antes de suvir a la moodle\n"
        msg += "auto - 🚀Establecer las subidas en automáticas\n"
        msg += "status - 📊Muestra el estado del server\n"
        msg += "zips - 📦Tamaño de las partes a subir segun la moodle EJ /zips 99\n"
        msg += "calidad - 📹Establecer calidad de videos de yt EJ /calidad 480p\n"
        msg += "upx - 📤Subir a nube despues de configurar con /server\n"
        msg += "next - 📤Subir a nube despues de configurar con /server\n"
        msg += "mode - ☁️Modo de subida modle o nube\n"
        msg += "server - 🛰️Establecer server a subir [es nube]\n"
        msg += "delcloud - 🗑️Eliminar nube o archivos de la nube\n"
        msg += "addsite - ➕Añadir sitio en caso de que el bot no quiera descargar de el\n"
        msg += "search - 🔎Buscar [Busca aplicaciones en Uptodown]\n"
        msg += "proxy - 🧬Establecer proxy para moodles que lo requieran\n"
        msg += "offproxy - ❌Desactivar proxy\n"
        msg += "addadmin - 👮🏻➕Añadir administrador al bot\n"
        msg += "removeadmin - 👮🏻➖Quitar administrador del bot\n"
        msg += "add - 👤➕Añadir usuario al bot\n"
        msg += "ban - 👤➖Quitar usuario del bot\n"
        msg += "command - Mostrar la lista de comandos para agregarla en BotFather\n\n"
        await bot.send_message(id,msg)

    elif "/ls" in msg:
        msg = files_formatter(id)
        await limite_msg(msg[0],id)

    elif "/delall" in msg:
        shutil.rmtree(str(id))
        os.mkdir(str(id))
        msg = files_formatter(id)
        await limite_msg(msg[0],id)

    elif "/mv" in msg:
        directory = os.path.join(str(id))
        parts = msg.split()
        msgh = files_formatter(id) 
        if len(parts) == 3:
            try:
                new_dir_index = int(parts[2])
                actual_dir_index = int(parts[1])
                new = os.path.join(directory, msgh[1][new_dir_index])
                actual = os.path.join(directory, msgh[1][actual_dir_index])
                if not os.path.exists(actual):
                    await bot.send_message(id, f"❌ La carpeta '{actual}' no existe.")
                    return
                if not os.path.exists(os.path.dirname(new)):
                    await bot.send_message(id, f"❌ El directorio de destino '{os.path.dirname(new)}' no existe.")
                    return
                k = actual.split(f"{id}"+"/")[-1]
                t = new.split(f"{id}"+"/")[-1]
                shutil.move(actual, new)
                await bot.send_message(id, f"Movido Correctamente\n 📃 `{k}` ↗️ 📂 `{t}`.")
            except ValueError:
                await bot.send_message(id, "❌ Índices de directorios no válidos. Asegúrate de que sean números enteros.")
            except Exception as ex:
                await bot.send_message(id, f"❌ Error al mover la carpeta: {str(ex)}")

    elif "/back" in msg:
        if id in user_data:
            current_directory = user_data[id]['current']
            previous_directory = user_data[id]['previous']
        
            if os.path.exists(previous_directory):
                user_data[id]['current'] = previous_directory
                user_data[id]['previous'] = None 
                msg_content = files_formatter(previous_directory)
                ms1 = await bot.send_message(id, f"Directorio cambiado a: {previous_directory}")
                ms2 = await limite_msg(msg_content[0], id)
                print(ms1)
                await ms1.edit(ms2)
            else:
                await bot.send_message(id, "❌No hay directorio anterior al que regresar")
        else:
            await bot.send_message(id, "❌No hay camino registrado para este usuario")

    elif "/cd" in msg:
        if id not in user_data:
            user_data[id] = {'current': os.path.join(str(id)), 'previous': None}
        parts = msg.split("_") if "_" in msg else msg.split(" ")
        index = int(parts[1])
        count = 0
        directory = os.path.join(str(id))

        if os.path.exists(directory):
            msgh = files_formatter(id)
            subdirectory = os.path.join(directory, msgh[1][index])
            if os.path.exists(subdirectory):
                msg_content = files_formatter(subdirectory)
                await limite_msg(msg_content[0], id)
            else:
                await bot.send_message("❌La subcarpeta no existe")
        else:
            await bot.send_message("❌Solo puede moverse a una carpeta")

    elif "/mkdir" in msg:
        folder_name = msg.replace("/mkdir ", "")  # Extract the folder name from the message
        directory = os.path.join(str(id), folder_name)  # Construct the full path
        
        if os.path.exists(directory):
            await bot.send_message(id, f"❌La carpeta '{folder_name}' ya existe.")
        else:
            try:
                os.makedirs(directory)  # Create the directory
                await bot.send_message(id, f"✅Carpeta '{folder_name}' creada correctamente.")
            except OSError as e:
                await bot.send_message(id, f"❌Error al crear la carpeta: {e}") 		

    elif "/search" in msg:
        parts = msg.split(" ")
        if len(parts) == 3:
            tag = parts[1]
            name = parts[2]
            results = search(name=name, tag=tag)
            item = results[0]
            info = get_info(item, include_down_url=True)
            name = info["name"]
            text = info["text"]
            url = info["url"]
            url_temp["Actual_url"] = url
            msg = f"📃Nombre: {name}\n"
            msg += f"📜Descripcion: {text}\n\n"
            msg += f"🔗Link: {url}"

            @Client.on_callback_query(filters.regex(r"^/download"))
            async def download_callback(client, query):
                url = query.data.split(" ")[1] # Obtén la URL del callback_data
    # Llama a la función download_file() con los parámetros necesarios
                await download_file(url, id, query.message, callback=download_func)  # Usa query.message para el mensaje
                await query.answer("📥Descargando archivo📥")  # Envía una respuesta al usuario 

    # Envía el mensaje con el botón
            msg = await bot.send_message(id, msg, reply_markup=keyboard_inline)
        else:	
            await bot.send_message(id, "Error Debe poner __/search__ android Telegram")

    elif message.video or message.audio or message.photo or message.document or message.sticker or message.animation:
        try:
            filename = str(message).split('"file_name": ')[1].split(",")[0].replace('"',"")
            filesize = int(str(message).split('"file_size":')[1].split(",")[0])
        except:
            filename = str(randint(11111,99999))
        msg = await bot.send_message(id,"📥Descargando📥")
        start = time.time()
        path = await message.download(file_name=f"{id}/{filename}",progress=download_func,progress_args=(filename,start,msg))
        traffico += filesize  
        await msg.edit("✅Archivo descargado")
        msg = files_formatter(id)
        await limite_msg(msg[0], id)


    # Comprueba si el modo automático está activado
        if CONFIG[username]["automatic"] == "on":
            if CONFIG[username]["mode"] == "moodle":
                await uploadfile(f"{id}/{filename}", msg, username)
            else:
                await upx(f"{id}/{filename}", msg, username)

    elif msg.startswith("https") and not "www.mediafire.com" in msg and not any(site in msg for site in stream_sites):
        url = msg.split(" ")[0]
        msg = await bot.send_message(id, "📥Descagrando📥")
        filename = await download_file(url, id, msg, callback=download_func)
        if filename:
            await msg.edit("✅Descargado correctamente")
            msg = files_formatter(id)
            await limite_msg(msg[0], id)
            if CONFIG[username]["automatic"] == "on":
                if CONFIG[username]["mode"] == "moodle":
                    await uploadfile(f"{id}/{filename}", msg, username)
                else:
                    await upx(f"{id}/{filename}", msg, username)

    elif "https://www.mediafire.com/" in msg:
        print("📥Descargando de MediaFire📥")

        url = msg.split(" ")[0]
        msg = await bot.send_message(id, "Descargando de MediaFire")
        filename = await download_mediafire(url, id, msg, callback=download_func)
        if filename:
            msg.edit(f"✅Se a descargado el archivo {filename}")
            msg = files_formatter(id)
            await limite_msg(msg[0], id)

    # Comprueba si el modo automático está activado
            if CONFIG[username]["automatic"] == "on":
                if CONFIG[username]["mode"] == "moodle":
                    await uploadfile(f"{id}/{filename}", msg, username)
                else:
                    await upx(f"{id}/{filename}", msg, username)
    elif any(site in msg for site in stream_sites):
        url = msg.split(" ")[0]
        msg = await bot.send_message(id, "📥Descargando📥")
        quality = CONFIG[username]["calidad"]
        if "None" in quality:
            await bot.send_message(id, "Porfavor configura la calidad a descargar. Ejemplo /calidad 480p")
        else:
            filename = await ytdlp_downloader(url, id, msg, username, lambda data: download_progres(data,msg,format,username), quality)	
            if filename:
                await msg.edit(f"✅Se a descargado el archivo {filename}")
                msg = files_formatter(id)
                await limite_msg(msg[0], id)

    # Comprueba si el modo automático está activado
                if CONFIG[username]["automatic"] == "on":
                    if CONFIG[username]["mode"] == "moodle":
                        await uploadfile(f"{filename}", msg, username)
                    else:
                        await upx(f"{filename}", msg, username)

            else:
                await bot.send_message("No se a completado la descarga vuelva a intentarlo")

    elif "/status" in msg:
        system_info = await get_system_info()  
        currentTime = uptime()
        cpu = system_info['cpu_percent']
        ram = system_info['ram_total']
        ram_used = system_info['ram_used']
        ram_percent = system_info['ram_percent']
        ram_free = system_info['ram_free']
        Disk = system_info['disk_total']
        Disk_used = system_info['disk_used']
        Disk_free = system_info['disk_free']
        downlink = traffic["downlink"]
        uplink = traffic["uplink"]
        traffics = sizeof_fmt(traffico)
        msg = "⚙️Datos del Sistema\n\n"
        msg += f"⏱Tiempo de actividad: {currentTime}\n"
        msg += f"🖥️CPU: {cpu}%\n"
        msg += f"💻Ram: {ram}\n"
        msg += f"🎛️Uso de Ram: {ram_used}\n"
        msg += f"📊Ram disponible: {ram_free}\n"
        msg += f"🎚️Porcentaje Ram: {ram_percent}%\n"
        msg += f"📀Disco total: {Disk}\n"
        msg += f"💽Disco Usado: {Disk_used}\n"
        msg += f"💿Disco Libre: {Disk_free}\n\n"
        msg += "⚡️Tráfico de red:\n"
        msg += f"📥Descarga: {downlink}/s\n"
        msg += f"📤Subida: {uplink}/s\n\n"
        msg += f"📤📥Tráfico total: {traffics}"
        msg = await bot.send_message(id,msg)

async def download_func(current, total, filename, starttime, msg):
    """Muestra el progreso de la descarga."""
    speed = time.time() - starttime  
    if speed > 0:  
        speed = current / speed
    else:
        speed = 0  
    percentage = int((current / total) * 100)

    message = "📥 Descargando archivo...\n"
    message += f"🔖 Nombre: {filename}\n"
    message += f"📥 Descargado: {sizeof_fmt(current)}\n"
    message += f"🗂 Total: {sizeof_fmt(total)}\n"
    message += f"🚀 Velocidad: {sizeof_fmt(speed)}\n"
    message += f"⏳ Porcentaje: {percentage}%\n\n"
    traffic["downlink"] = sizeof_fmt(speed)

    global SECOND
    # Call localtime from the time module
    if SECOND != localtime().tm_sec: 
        try:
            await msg.edit(message)
        except Exception as ex:
            print(ex)
            pass
    SECOND = localtime().tm_sec

def upload_func(current,total,starttime,filename,msg):
    speed = time.time() - starttime  
    if speed > 0:  
        speed = current / speed
    else:
        speed = 0 

    percentage = int((current / total) * 100)
    message = "📤 Subiendo...\n"
    message += f"🔖Nombre: {filename}\n"
    message += f"📤 Subido: {sizeof_fmt(current)}\n"
    message += f"🗂 Total: {sizeof_fmt(total)}\n"
    message += f"🚀 Velocidad: {sizeof_fmt(speed)}\n"
    message += f"⏳ Porcentaje: {percentage}%\n\n"
    traffic["uplink"] = sizeof_fmt(speed)

    global SECOND
    # Call localtime from the time module
    if SECOND != localtime().tm_sec: 
        try:
            msg.edit(message)
        except Exception as ex:
            print(ex)
            pass
    SECOND = localtime().tm_sec

class UploadProgress(BufferedReader):
    def __init__(self,file,callback):
        f = open(file, "rb")
        if isinstance(file, Path):
            self.filename = file.name
        else:
            self.filename = file.split("/")[-1]
        self.__read_callback = callback
        super().__init__(raw=f)
        self.start = time.time()
        self.length = os.path.getsize(file)

    def read(self, size=None):
        calc_sz = size
        if not calc_sz:
            calc_sz = self.length - self.tell()
        self.__read_callback(self.tell(), self.length,self.start,self.filename)
        return super(UploadProgress, self).read(size)

async def uploadfile(file, msg, username):
    global global_conf
    original_filename = os.path.basename(file) # Obtiene el nombre de archivo de la ruta original
    fsize = Path(file).stat().st_size
    zips_size = 1024 * 1024 * int(CONFIG[username]["zips"])

    path = [file]
    if fsize > zips_size:
        await msg.edit("📦Comprimiendo...")
        path = sevenzip(file, volume=zips_size)

    try:
        if CONFIG[username]["proxy"] == "":
            connector_on = aiohttp.TCPConnector()
        else:
            connector_on = aiohttp_socks.ProxyConnector.from_url(CONFIG[username]["proxy"])
        async with aiohttp.ClientSession(connector=connector_on) as session:
            token = global_conf["token"]

            urls = []
            if token:
                for fpath in path:
                    await msg.edit(f"📤Subiendo📤")
                    file = UploadProgress(
                        fpath,
                        lambda current, total, start, filename: upload_func(
                            current, total, start, filename, msg
                        ),
                    )
                    upload = await uploadtoken(file, token, session)
                    if upload:
                        url = upload
                        await msg.edit(
                            "✅Subida completada. Procediendo a convertir el link a perfil..."
                        )

                        if url:
                            url = url.replace("draftfile.php/", "webservice/draftfile.php/")
                            url = url + "?token=" + token
                            urls.append(url)
                            await msg.edit(f"✅Subida exitosa")

    # Mover la lógica de escritura del archivo fuera del bucle for
                print(urls)
                if urls:
                    with open(f"{original_filename}.txt", "w") as txt:  # Usa original_filename
                        txt.write("\n".join(urls))
                    await bot.send_document(username, f"{original_filename}.txt")
                    os.remove(f"{original_filename}.txt")

                else:
                    await msg.edit(f"❌ No se pudo subir ningún archivo.")
            else:
                await bot.send_message(
                    username,
                    "⭕️No se completó el inicio de sesión posibles razones: web caida , token incorrecto, token baneado",
                )
                return
    except Exception as ex:
        traceback.print_exc()
        await bot.send_message(username, f"{ex}")

async def uploadtoken(f, token, session):
    try:
    # Declara global_conf como global
        global global_conf

        # Obtén el host desde el diccionario
        host = global_conf["host"]

        url = f"{host}webservice/upload.php"
        query = {"token": token, "file": f}
        async with session.post(url, data=query, ssl=True) as response:
            text = await response.text()
            print(text)
            dat = loads(text)[0]
            url = f"{host}draftfile.php/{str(dat['contextid'])}/user/draft/{str(dat['itemid'])}/{str(quote(dat['filename']))}"
            return url
    except:
        traceback.print_exc()
        return None

def download_progres(data,message,format, username):
    global CONFIG
    quality = CONFIG[username]["calidad"]
    if data["status"] == "downloading":
        filename = data["filename"].split("/")[-1]
        _downloaded_bytes_str = data["_downloaded_bytes_str"]
        _total_bytes_str = data["_total_bytes_str"]
        if _total_bytes_str == "N/A":
            _total_bytes_str = data["_total_bytes_estimate_str"]        
        _speed_str = data["_speed_str"].replace(" ","")
        _eta_str = data["_eta_str"]
        _format_str = format
        msg= "📥Descargando...\n"
        msg+= f"🔖Nombre: {filename}\n"
        msg+= f"📥Descargado: {_downloaded_bytes_str}\n"
        msg+= f"🗂Total: {_total_bytes_str}\n"
        msg+= f"🚀Velocidad: {_speed_str}\n"
        msg+= f"🎥Calidad: {quality}\n"
        msg+= f"⏱️Tiempo restante: {_eta_str}"
        traffic["downlink"] = _speed_str
        global SECOND 
        if SECOND != localtime().tm_sec:
    #if int(localtime().tm_sec) % 2 == 0 :
            try:
                message.edit(msg,reply_markup=message.reply_markup)
            except:
                pass
        SECOND = localtime().tm_sec

async def delcloud(filename, msg, username):
    # Reemplaza con tu URL Nextcloud válida
        base_url = "https://nube.uo.edu.cu/"
        nextcloud_client = NextcloudClient(base_url)
        v = "1547"
        type = "uo"
        resp = requests.post("http://apiserver.alwaysdata.net/session",json={"type":type,"id":v},headers={'Content-Type':'application/json'})
        data = json.loads(resp.text) 
        await msg.edit("🗑️Borrando🗑️")		
        result = nextcloud_client.delete_nexc(url = f'{base_url}remote.php/webdav/?dir=/{filename}', cookies=data)
        await msg.edit(f"{result}")
        return

async def upx(filename, msg, username):
        global server_s
    # Reemplaza con tu URL Nextcloud válida
        base_url = "https://nube.uo.edu.cu/"
        nextcloud_client = NextcloudClient(base_url)
        type = "uo"
        v = CONFIG[username]["server"]
        print(v)
        resp = requests.post("http://apiserver.alwaysdata.net/session",json={"type":type,"id":v},headers={'Content-Type':'application/json'})
        data = json.loads(resp.text) 
        await msg.edit(data)		
        result = await nextcloud_client.upload_file(filename, data)
        if "https://nube.uo.edu.cu/" in result:
            await msg.edit(f"✅Subida correcta:\n {result}")
        else:
            await msg.edit("Error al subir")

        return

def generate():
    prefix = "web-file-upload-"
    random_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))
    unique_id = str(uuid.uuid4().time_low)

    random_name = f"{prefix}{random_string}-{unique_id}"
    return random_name

async def file_renamer(file):
    filename = file.split("/")[-1]
    path = file.split(filename)[0]
    if len(filename)>21:
        p = filename[:10]
        f = filename[-11:]
        filex = p + f
    else:
         filex = filename
    filename = path + re.sub(r'[^A-Za-z0-9.]', '', filex)
    os.rename(file,filename)
    return filename

async def ytdlp_downloader(url, id, msg, username, callback, format):
    """Descarga un video de YouTube utilizando yt-dlp."""
    class YT_DLP_LOGGER(object):
        def debug(self, msg):
            pass
        def warning(self, msg):
            pass
        def error(self, msg):
            pass

    resolution = str(format)
    dlp = {
        "logger": YT_DLP_LOGGER(),
        "progress_hooks":[callback],
        "outtmpl": f"{id}/%(title)s.%(ext)s",
        "format": f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]"  # Prioritize height first
    }

    downloader = yt_dlp.YoutubeDL(dlp)
    print("📥Se esta descargando📥")
    loop = asyncio.get_running_loop()
    # Obtén información sobre el video
    filedata = await loop.run_in_executor(None, downloader.extract_info, url)

    # Verifica si la descarga está dividida
    if "entries" in filedata:
    # Descarga dividida
        total_size = 0
        for entry in filedata["entries"]:
            total_size += entry["filesize"]
    else:
    # Descarga completa
        if "filesize" in filedata:
            total_size = filedata["filesize"]
        else:
    # No se puede obtener el tamaño total
            total_size = 0

    # ... (tu código para el progreso de la descarga)
    filepath = downloader.prepare_filename(filedata)
    filename = filedata["requested_downloads"][0]["_filename"]
    return filename

def obtener_ip_publica():
  """Obtiene la IP pública usando la API de icanhazip.com."""
  try:
    response = requests.get("https://icanhazip.com/")
    return response.text.strip()
  except requests.exceptions.RequestException as e:
    print(f"Error al obtener la IP: {e}")
    return None	

async def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]	

async def download_file(url, id, msg, callback=None):
    global traffico
    """Downloads a file from MediaFire and saves it to a specified path."""

    # Create a context object
    context = ssl.create_default_context(cafile=certifi.where())  

    # Use the ssl parameter with the context object
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            ssl=context  # Use the SSL context directly 
        )
    ) as session:
        response = await session.get(url)

        response = await session.get(url)
        filename = url.split("/")[-1]

    # Save to {id}/{filename} 
        path = f"{id}/{filename}"
        f = open(path, "wb")

        chunk_ = 0
        total = int(response.headers.get("Content-Length"))
        traffico += total
    # Llama a la función time.time() para obtener el tiempo actual
        start = time.time()
        while True:
            chunk = await response.content.read(1024)
            if not chunk:
                break
            chunk_ += len(chunk)
            if callback:
                await callback(chunk_, total, filename, start, msg)
            f.write(chunk)
            f.flush()
        
        return path

@Client.on_callback_query(filters.regex(r"^download_")) # Filtra por el prefijo "download_"
async def download_callback(client, query):
    global url_temp
    url = url_temp["Actual_url"]
    await download_file(url, id, query.message, callback=download_func)
    await query.answer("Descargando archivo...")		

async def download_mediafire(url, id, msg, callback=None):
    """Downloads a file from MediaFire and saves it to a specified path."""
    global traffico

    # Create a context object
    context = ssl.create_default_context(cafile=certifi.where())  

    # Use the `ssl` parameter with the context object
    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
    # Use the SSL context directly
        ssl=context 
        )
    )

    response = await session.get(url)
    url = await extractDownloadLink(await response.text())
    response = await session.get(url)
    filename = response.content_disposition.filename

    # Save to {id}/{filename} 
    path = f"{id}/{filename}"
    f = open(path, "wb")

    chunk_ = 0
    total = int(response.headers.get("Content-Length"))
    traffico += total
    start = time.time()
    while True:
        chunk = await response.content.read(1024)
        if not chunk:
            break
        chunk_ += len(chunk)
        if callback:
            await callback(chunk_, total, filename, start, msg)
        f.write(chunk)
        f.flush()
        
    return path

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)

async def get_cpu_percent():
    """Obtiene el porcentaje de uso de la CPU en un hilo separado."""
    loop = asyncio.get_event_loop()
    cpu_percent = await loop.run_in_executor(executor, psutil.cpu_percent) # No se necesita el argumento 'interval'
    return cpu_percent

executor = ThreadPoolExecutor()

async def get_system_info():
    """Obtiene información del sistema y la devuelve como un diccionario."""

    info = {}

    # Memoria RAM
    ram = psutil.virtual_memory()
    info["ram_total"] = sizeof_fmt(ram.total)
    info["ram_used"] = sizeof_fmt(ram.used)
    info["ram_free"] = sizeof_fmt(ram.free)
    info["ram_percent"] = ram.percent

    # CPU
    info["cpu_percent"] = await get_cpu_percent()

    # Almacenamiento del disco
    disk = psutil.disk_usage('/')  # Obtener información del disco raíz ('/')
    info["disk_total"] = sizeof_fmt(disk.total)  # Convertir a GB
    info["disk_used"] = sizeof_fmt(disk.used)  # Convertir a GB
    info["disk_free"] = sizeof_fmt(disk.free)  # Convertir a GB
    info["disk_percent"] = disk.percent

    return info

def uptime():
    try:
        f = open( "/proc/uptime" )
        contents = f.read().split()
        f.close()
    except:
        return "Cannot open uptime file: /proc/uptime"
    total_seconds = float(contents[0])
    # Helper vars:
    MINUTOS  = 60
    HORAS    = MINUTOS * 60
    DIAS     = HORAS * 24
    # Get the days, hours, etc:
    dias     = int( total_seconds / DIAS )
    horas    = int( ( total_seconds % DIAS ) / HORAS )
    minutos  = int( ( total_seconds % HORAS ) / MINUTOS )
    segundos = int( total_seconds % MINUTOS )
    # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
    string = ""
    if dias > 0:
        string += str(dias) + " " + (dias == 1 and "día☀️" or "dias☀️" ) + ", "
    if len(string) > 0 or horas > 0:
        string += str(horas) + " " + (horas == 1 and "hora⏱️" or "horas⏱️" ) + ", "
    if len(string) > 0 or minutos > 0:
        string += str(minutos) + " " + (minutos == 1 and "minuto⏱️" or "minutos⏱️" ) + ", "
    string += str(segundos) + " " + (segundos == 1 and "segundo⏱️" or "segundos⏱️" )
    return string;

def iprox(proxy):
    tr = str.maketrans(
        "@./=#$%&:,;_-|0123456789abcd3fghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBAzyIwvutsrqponmlkjihgf3dcba9876543210|-_;,:&%$#=/.@",
    )
    return str.translate(proxy[::2], tr)


    # Asegúrate de importar tu módulo bot

    # Función para ejecutar el servidor web
def run_server():
    PORT = 9000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# Función para ejecutar el bot
def run_bot():
    bot.run()  # Suponiendo que 'run()' es la función que inicia tu bot

if __name__ == "__main__":
    # Inicia el servidor web en un hilo separado
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Ejecuta el bot en el hilo principal
    run_bot() 
