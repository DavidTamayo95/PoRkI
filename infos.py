from pyobigram.utils import sizeof_fmt,nice_time
import datetime
import time
import os

def text_progres(index,max):
	try:
		if max<1:
			max += 1
		porcent = index / max
		porcent *= 100
		porcent = round(porcent)
		make_text = ''
		index_make = 1
		make_text += ' 【 '
		while(index_make<21):
			if porcent >= index_make * 5: make_text+='◆'
			else: make_text+='◇'
			index_make+=1
		make_text += ' 】 '
		return make_text
	except Exception as ex:
			return ''

def porcent(index,max):
    porcent = index / max
    porcent *= 100
    porcent = round(porcent)
    return porcent

def createDownloading(filename,totalBits,currentBits,speed,time,tid=''):
    msg = "▶️𝐄𝐬𝐭𝐚𝐝𝐨: Descargando archivo...\n\n"
    msg += "📔: "+filename+'\n\n'
    msg += "⬇️𝐃𝐞𝐬𝐜𝐚𝐫𝐠𝐚𝐝𝐨: "+sizeof_fmt(currentBits) + ' de ' + sizeof_fmt(totalBits) + '\n'
    msg += "⚡️𝐒𝐏𝐃: "+sizeof_fmt(speed)+'/s ''| ''⏰𝐄𝐓𝐀: '+str(datetime.timedelta(seconds=int(time)))+'s\n\n'
    if tid!='':
        msg+= '🚫 /cancel_' + tid
    return msg

def createUploading(filename,totalBits,currentBits,speed,time,originalname=''):
    msg = "▶️𝐄𝐬𝐭𝐚𝐝𝐨: Agregando a la nube...\n\n"
    msg += '📄: '+filename+'\n\n'
    msg += "⬆️𝐒𝐮𝐛𝐢𝐝𝐨: "+sizeof_fmt(currentBits) + ' de ' + sizeof_fmt(totalBits) + '\n'
    msg += "⚡️𝐒𝐏𝐃: "+sizeof_fmt(speed)+'/s ''| ''⏰𝐄𝐓𝐀: '+str(datetime.timedelta(seconds=int(time)))+'s\n\n'
    return msg

def createCompresing(filename,filesize,splitsize):
    msg  = "▶️𝐄𝐬𝐭𝐚𝐝𝐨: Comprimiendo archivo...\n\n"
    msg += "🗜Comprimiendo "+ str(round(int(filesize/splitsize)+1,1))+" en partes de "+str(sizeof_fmt(splitsize))+'\n\n'
    return msg

def createFinishUploading(filename,filesize,urls,username):
    msg = "▶️𝐄𝐬𝐭𝐚𝐝𝐨: Subida finalizada ...\n\n"
    msg += "📓: "+ str(filename)+'\n\n'
    msg += '<b>🔗𝐄𝐧𝐥𝐚𝐜𝐞 𝐝𝐞 𝐝𝐞𝐬𝐜𝐚𝐫𝐠𝐚:</b>\n'
    msg += urls
    msg += "\n⚡️¡Siempre su mejor opción!⚡️\n\n"
    return msg

def createFileMsg(filename,files):
    import urllib
    if len(files)>0:
        msg= '<b>Links</b>\n'
        for f in files:
            url = urllib.parse.unquote(f['directurl'],encoding='utf-8', errors='replace')
            #msg+= '<a href="'+f['url']+'">' + f['name'] + '</a>'
            msg+= "<a href='"+url+"'>"+f['name']+'</a>\n'
        return msg
    return ''

def createFilesMsg(evfiles):
    msg = '➣ Archivos ('+str(len(evfiles))+')\n\n'
    i = 0
    for f in evfiles:
            try:
                fextarray = str(f['files'][0]['name']).split('.')
                fext = ''
                if len(fextarray)>=3:
                    fext = '.'+fextarray[-2]
                else:
                    fext = '.'+fextarray[-1]
                fname = f['name'] + fext
                msg+= '/txt_'+ str(i) + ' /del_'+ str(i) + '\n' + fname +'\n\n'
                i+=1
            except:pass
    return msg
def createStat(username,userdata,isadmin):
    from pyobigram.utils import sizeof_fmt
    msg = "👥 Usuario: "+str(userdata['moodle_user'])+'\n'
    msg += "🔑 Contraseña: "+str(userdata['moodle_password'])+'\n'
    msg += "☁️Página: "+ str(userdata['moodle_host'])+'\n'
    msg += "🗜Tamaño por archivo: "+ sizeof_fmt(userdata['zips']*1024*1024) + '\n\n'
    proxy = '❌'
    if userdata['proxy'] !='':
       proxy = '✅'
    msg += "🔌 Proxy: " + proxy +"\n"
    msgAdmin = '❌'
    if isadmin:
        msgAdmin = '✅'
    msg+= '🦾Admin : ' + msgAdmin + '\n\n'
    
    return msg
