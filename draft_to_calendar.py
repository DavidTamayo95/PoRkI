from os import unlink
from random import randint
from pyrogram import Client
from pyrogram.types import Message
import asyncio
from aiohttp_socks import ProxyConnector
import aiohttp
from yarl import URL
import re
import urllib.parse
import json
from bs4 import BeautifulSoup



async def send_calendar(moodle: str, user: str, passw: str, urls: list, proxy: str = "") -> list:
    if proxy == "":
        connector = aiohttp.TCPConnector()
    else:
        connector = ProxyConnector.from_url(proxy)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Extraer el token de inicio de sesión
        try:
            # Login
            async with session.get(moodle + "/login/index.php") as response:
                html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            token = soup.find("input", attrs={"name": "logintoken"})
            if token:
                token = token["value"]
            else:
                token = ""
            payload = {
                "anchor": "",
                "logintoken": token,
                "username": user,
                "password": passw,
                "rememberusername": 1,
            }
            async with session.post(moodle + "/login/index.php", data=payload) as response:
                html = await response.text()

            sesskey = re.findall('(?<="sesskey":")(.*?)(?=")', html)[-1]
            userid = re.findall('(?<=userid=")(.*?)(?=")', html)[-1]
            # Mover a calendario
            base_url = (
                "{}/lib/ajax/service.php?sesskey={}&info=core_calendar_submit_create_update_form"
            )
            payload = [
                {
                    "index": 0,
                    "methodname": "core_calendar_submit_create_update_form",
                    "args": {
                        "formdata": "id=0&userid={}&modulename=&instance=0&visible=1&eventtype=user&sesskey={}&_qf__core_calendar_local_event_forms_create=1&mform_showmore_id_general=1&name=Evento&timestart[day]=4&timestart[month]=10&timestart[year]=2022&timestart[hour]=18&timestart[minute]=55&description[text]={}&description[format]=1&description[itemid]={}&location=&duration=0"
                    },
                }
            ]
            urls_payload = '<p dir="ltr"><span style="font-size: 14.25px;">{}</span></p>'
            base_url = base_url.format(moodle, sesskey)
            urlparse = lambda url: urllib.parse.quote_plus(urls_payload.format(url))
            urls_parsed = "".join(list(map(urlparse, urls)))
            payload[0]["args"]["formdata"] = payload[0]["args"]["formdata"].format(
                userid, sesskey, urls_parsed, randint(1000000000, 9999999999)
            )
            async with session.post(base_url, data=json.dumps(payload)) as result:
                resp = await result.json()
                resp = resp[0]["data"]["event"]["description"]

            return re.findall("https?://[^\s\<\>]+[a-zA-z0-9]", resp)
        except Exception as e:
            print(
                "Error in send_calendar()\nMoodle: {}\nUser: {}\nPassword: {}\nURLs: {}".format(
                    moodle, user, passw, urls
                )
            )
            print(e)
