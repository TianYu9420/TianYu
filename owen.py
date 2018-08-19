# -*-coding: utf-8 -*-

from Linephu.linepy import *
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse, timeit
#==============================================================================#
botStart = time.time()

cl = LINE()
cl.log("Auth Token : " + str(cl.authToken))

clMID = cl.profile.mid

clProfile = cl.getProfile()
lineSettings = cl.getSettings()

oepoll = OEPoll(cl)
#==============================================================================#
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
banOpen = codecs.open("ban.json","r","utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)
ban = json.load(banOpen)

msg_dict = {}
bl = [""]

#==============================================================================#
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = ban
        f = codecs.open('ban.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def helpmessage():
    helpMessage = """╔══════════════
╠♥ ✿✿✿ 公開回應機 ✿✿✿ ♥
║
╠➥ /Runtime 運作時間
╠➥ /Speed 速度
╠➥ #About關於本帳
╠➥ #Stread 已讀點設置
╠➥ #Clread 取消偵測
╠➥ #lkread 已讀偵測
╠➥ Back_add:關鍵字:回復文字
╠➥ Back_del:刪除關鍵字
╚═〘 Created By: ©淫蕩™ 〙"""
    return helpMessage
wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
}
setTime = {}
setTime = wait2['setTime']

def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))

admin =['u787d6464e208dad899bdc1f80eaf9284',"u6ef9e80ab0abb7f5a429172abb52eb8c",clMID]
owners = ["u787d6464e208dad899bdc1f80eaf9284","u6ef9e80ab0abb7f5a429172abb52eb8c"]
#if clMID not in owners:
#    python = sys.executable
#    os.execl(python, python, *sys.argv)
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            contact = cl.getContact(op.param1)
            print ("[ 5 ] 通知添加好友 名字: " + contact.displayName)
            if settings["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                cl.sendMessage(op.param1, "感謝您加入我為好友！".format(str(contact.displayName)))
                cl.sendMessage(op.param1, "歡迎邀請我加群組喔! 此機器為回應機")
        if op.type == 11:
            group = cl.getGroup(op.param1)
            contact = cl.getContact(op.param2)
            if settings["qrprotect"] == True:
                if op.param2 in admin or op.param2 in ban["bots"] or op.param2 in group.creator:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
        if op.type == 13:
            contact1 = cl.getContact(op.param2)
            contact2 = cl.getContact(op.param3)
            group = cl.getGroup(op.param1)
            GS = group.creator.mid
            print ("[ 13 ] 通知邀請群組: " + str(group.name) + "\n邀請者: " + contact1.displayName + "\n被邀請者" + contact2.displayName)
            if clMID in op.param3:
                if settings["autoJoin"] == True:
                    cl.acceptGroupInvitation(op.param1)
                    cl.sendMessage(op.param1, "歡迎邀請我加入群組")
                    cl.sendMessage(op.param1, "此機器為回應機")
#                    if group.preventedJoinByTicket == True:
#                        group.preventedJoinByTicket = False
#                        cl.updateGroup(group)
#                    else:
#                        pass
  #           elif settings["invprotect"] == True:
   #              if op.param2 in admin or op.param2 in ban["bots"] or op.param2 in group.creator:
  #                  pass
 #               else:
#                    cl.cancelGroupInvitation(op.param1,[op.param3])
 #           else:
#                group = cl.getGroup(op.param1)
#                gInviMids = []
#                for z in group.invitee:
#                    if z.mid in ban["blacklist"]:
#                        gInviMids.append(z.mid)
#                if gInviMids == []:
#                    pass
#                else:
#                    cl.cancelGroupInvitation(op.param1, gInviMids)
#                    cl.sendMessage(op.param1,"被誘姦者黑單中...")
#        if op.type == 17:
#            if op.param2 in admin or op.param2 in ban["bots"]:
#                return
#            ginfo = str(cl.getGroup(op.param1).name)
#            try:
#	        strt = int(3)
#                akh = int(3)
#                akh = akh + 8
#            	aa = """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(op.param2)+"},"""
#        	aa = (aa[:int(len(aa)-1)])
#            	cl.sendMessage(op.param1, "歡淫 @wanping 加入"+ginfo , contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
#            except Exception as e:
#                print(str(e))
#        if op.type == 19:
#            msg = op.message
#            group = cl.getGroup(op.param1)
#            chiya = []
##            chiya.append(op.param2)
#            chiya.append(op.param3)
#            cmem = cl.getContacts(chiya)
#            if op.param2 not in admin or op.param2 not in group.creator:
#                if op.param2 in ban["bots"]:
#                    pass
#                elif settings["protect"] == True:
#                    ban["blacklist"][op.param2] = True
#                    cl.kickoutFromGroup(op.param1,[op.param2])
#                    cl.inviteIntoGroup(op.param1,[op.param3])
#                else:
#                    cl.sendMessage(op.param1,"")
#            else:
#                cl.sendMessage(op.param1,"")
        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 25 or op.type == 26:
            K0 = admin
            msg = op.message
            if settings["share"] == True:
                K0 = msg._from
            else:
                K0 = admin
        if op.type == 25 :
            if msg.toType ==2:
                g = cl.getGroup(op.message.to)
                print ("sended:".format(str(g.name)) + str(msg.text))
            else:
                print ("sended:" + str(msg.text))
        if op.type == 26:
            msg =op.message
            pop = cl.getContact(msg._from)
            print ("replay:"+pop.displayName + ":" + str(msg.text))
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
            if sender in K0 or sender in owners:
                if text.lower() == '/help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                    cl.sendContact(to,"u6ef9e80ab0abb7f5a429172abb52eb8c")
                elif text.lower() == '/bye':
                    cl.sendMessage(to,"See you next time.")
                    cl.leaveGroup(msg.to)
#==============================================================================#
                elif text.lower() == '/speed':
                    start = time.time()
                    cl.sendMessage(to, "月老降臨...牽紅線時間")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)) + "秒")

                elif text.lower() == '/sp':
                    start = time.time()
                    cl.sendMessage(to, "月老降臨...牽紅線時間到")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)) + "秒")								
					
                elif text.lower() == '/Speed':
                    start = time.time()
                    cl.sendMessage(to, "月老降臨...牽紅線時間")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)) + "秒")								
				
                elif text.lower() == '/Sp':
                    start = time.time()
                    cl.sendMessage(to, "月老降臨...牽紅線時間到")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)) + "秒")
                    
#                elif text.lower() == 'save':
#                    backupData()
#                    cl.sendMessage(to,"儲存設定成功!")
 #               elif text.lower() == 'restart':
 #                   cl.sendMessage(to, "重新啟動中...")
                    time.sleep(5)
 #                   cl.sendMessage(to, "重啟成功，請重新登入")
#                    restartBot()
                elif text.lower() == '/runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    cl.sendMessage(to, "我已尻了 {}".format(str(runtime)))
                elif text.lower() == '#about':
                    try:
                        arr = []
                        owner ="u787d6464e208dad899bdc1f80eaf9284"
                        creator = cl.getContact(owner)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        ret_ = "╔══[ 關於使用者 ]"
                        ret_ += "\n╠ 使用者名稱 : {}".format(contact.displayName)
                        ret_ += "\n╠ 群組數 : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ 好友數 : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ 已封鎖 : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ 關於本bot ]"
                        ret_ += "\n╠ 版本 : 最新"
                        ret_ += "\n╠ 製作者 : {}".format(creator.displayName)
                        ret_ += "\n╚══[ 感謝您的使用 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == 'set':
                    try:
                        ret_ = "╔══[ 狀態 ]"
                        if settings["autoAdd"] == True: ret_ += "\n╠ Auto Add ✅"
                        else: ret_ += "\n╠ Auto Add ❌"
                        if settings["autoJoin"] == True: ret_ += "\n╠ Auto Join ✅"
                        else: ret_ += "\n╠ Auto Join ❌"
                        if settings["autoLeave"] == True: ret_ += "\n╠ Auto Leave ✅"
                        else: ret_ += "\n╠ Auto Leave ❌"
                        if settings["autoRead"] == True: ret_ += "\n╠ Auto Read ✅"
                        else: ret_ += "\n╠ Auto Read ❌"
                        if settings["protect"] ==True: ret_+="\n╠ Protect ✅"
                        else: ret_ += "\n╠ Protect ❌"
                        if settings["qrprotect"] ==True: ret_+="\n╠ QrProtect ✅"
                        else: ret_ += "\n╠ QrProtect ❌"
                        if settings["invprotect"] ==True: ret_+="\n╠ InviteProtect ✅"
                        else: ret_ += "\n╠ InviteProtect ❌"
                        if settings["detectMention"] ==True: ret_+="\n╠ DetectMention ✅"
                        else: ret_ += "\n╠ DetectMention ❌"
                        if settings["reread"] ==True: ret_+="\n╠ Reread ✅"
                        else: ret_ += "\n╠ Reread ❌"
                        if settings["share"] ==True: ret_+="\n╠ Share ✅"
                        else: ret_ += "\n╠ Share ❌"
                        ret_ += "\n╚══[ Finish ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "Auto Add on success")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "Auto Add off success")
                elif text.lower() == 'autojoin on':
                    settings["autoJoin"] = True
                    cl.sendMessage(to, "Auto Join on success")
                elif text.lower() == 'autojoin off':
                    settings["autoJoin"] = False
                    cl.sendMessage(to, "Auto Join off success")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    cl.sendMessage(to, "Auto Leave on success")
                elif text.lower() == 'autojoin off':
                    settings["autoLeave"] = False
                    cl.sendMessage(to, "Auto Leave off success")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    cl.sendMessage(to, "Auto Read on success")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    cl.sendMessage(to, "Auto Read off success")
                elif text.lower() == 'reread on':
                    settings["reread"] = True
                    cl.sendMessage(to,"reread on success")
                elif text.lower() == 'reread off':
                    settings["reread"] = False
                    cl.sendMessage(to,"reread off success")
#                   cl.sendMessage(to, "踢人保護開啟")
#                elif text.lower() == 'protect off':
#                    settings["protect"] = False
#                     cl.sendMessage(to, "踢人保護關閉")
                elif text.lower() == 'share on':
                    settings["share"] = True
                    cl.sendMessage(to, "已開啟分享")
                elif text.lower() == 'share off':
                    settings["share"] = False
                    cl.sendMessage(to, "已關閉分享")
 #               elif text.lower() == 'detect on':
#                    settings["detectMention"] = True
#                    cl.sendMessage(to, "已開啟標註偵測")
#                elif text.lower() == 'detect off':
#                    settings["detectMention"] = False
#                    cl.sendMessage(to, "已關閉標註偵測")
#                elif text.lower() == 'qrprotect on':
#                    settings["qrprotect"] = True
#                    cl.sendMessage(to, "網址保護開啟")
#                elif text.lower() == 'qrprotect off':
#                    settings["qrprotect"] = False
#                    cl.sendMessage(to, "網址保護關閉")
#                elif text.lower() == 'invprotect on':
#                    settings["invprotect"] = True
#                    cl.sendMessage(to, "邀請保護開啟")
#                elif text.lower() == 'invprotect off':
#                    settings["invprotect"] = False
#                    cl.sendMessage(to, "邀請保護關閉")
#                elif text.lower() == 'getmid on':
#                    settings["getmid"] = True
#                    cl.sendMessage(to, "mid獲取開啟")
#                elif text.lower() == 'getmid off':
#                    settings["getmid"] = False
#                    cl.sendMessage(to, "mid獲取關閉")
#                elif text.lower() == 'timeline on':
#                    settings["timeline"] = True
#                    cl.sendMessage(to, "文章預覽開啟")
#                elif text.lower() == 'timeline off':
#                    settings["timeline"] = False
#                    cl.sendMessage(to, "文章預覽關閉")
#                elif text.lower() == 'pro on':
#                    settings["protect"] = True
#                    settings["qrprotect"] = True
#                    settings["invprotect"] = True
#                    cl.sendMessage(to, "踢人保護開啟")
#                    cl.sendMessage(to, "網址保護開啟")
#                    cl.sendMessage(to, "邀請保護開啟")
#                elif text.lower() == 'pro off':
#                    settings["protect"] = False
#                    settings["qrprotect"] = False
##                    settings["invprotect"] = False
#                    cl.sendMessage(to, "踢人保護關閉")
#                    cl.sendMessage(to, "網址保護關閉")
#                    cl.sendMessage(to, "邀請保護關閉")
#==============================================================================#
#                elif msg.text.lower().startswith("adminadd "):
#                    MENTION = eval(msg.contentMetadata['MENTION'])
#                    inkey = MENTION['MENTIONEES'][0]['M']
#                    admin.append(str(inkey))
#                    cl.sendMessage(to, "已獲得權限！")
#                elif msg.text.lower().startswith("admindel "):
#                    MENTION = eval(msg.contentMetadata['MENTION'])
#                    inkey = MENTION['MENTIONEES'][0]['M']
#                    admin.remove(str(inkey))
#                    cl.sendMessage(to, "已取消權限！")
#                elif text.lower() == 'adminlist':
##                    if admin == []:
#                        cl.sendMessage(to,"無擁有權限者!")
 #                   else:
##                        mc = "╔══[ Admin List ]"
#                        for mi_d in admin:
#                            mc += "\n╠ "+cl.getContact(mi_d).displayName
#                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
#                elif msg.text.lower().startswith("invite "):
#                    targets = []
#                    key = eval(msg.contentMetadata["MENTION"])
##                    key["MENTIONEES"][0]["M"]
#                    for x in key["MENTIONEES"]:
#                        targets.append(x["M"])
#                    G = cl.getGroup
#                    cl.inviteIntoGroup(to,targets)
#                elif ("Say " in msg.text):
#                    x = text.split(' ',2)
#                    c = int(x[2])
#                    for c in range(c):
#                        cl.sendMessage(to,x[1])
#                elif msg.text.lower().startswith("tag "):
#                    MENTION = eval(msg.contentMetadata['MENTION'])
#                    inkey = MENTION['MENTIONEES'][0]['M']
#                    x = text.split(' ',2)
#                    c = int(x[2])
#                    for c in range(c):
#                        sendMessageWithMention(to, inkey)
##                elif msg.text.lower().startswith("botsadd "):
#                    MENTION = eval(msg.contentMetadata['MENTION'])
##                    inkey = MENTION['MENTIONEES'][0]['M']
#                    ban["bots"].append(str(inkey))
#                    cl.sendMessage(to, "已加入分機！")
#                elif msg.text.lower().startswith("botsdel "):
#                    MENTION = eval(msg.contentMetadata['MENTION'])
#                    inkey = MENTION['MENTIONEES'][0]['M']
##                    ban["bots"].remove(str(inkey))
#                    cl.sendMessage(to, "已取消分機！")
#                elif text.lower() == 'botslist':
#                    if ban["bots"] == []:
#                        cl.sendMessage(to,"無分機!")
#                    else:
#                        mc = "╔══[ Inviter List ]"
#                        for mi_d in ban["bots"]:
#                            mc += "\n╠ "+cl.getContact(mi_d).displayName
#                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
##                elif text.lower() == 'join':
#                    if msg.toType == 2:
##                        G = cl.getGroup
##                        cl.inviteIntoGroup(to,ban["bots"])
#                elif msg.text.lower().startswith("ii "):
#                    MENTION = eval(msg.contentMetadata['MENTION'])
#                    inkey = MENTION['MENTIONEES'][0]['M']
#                    cl.createGroup("fuck",[inkey])
#                    cl.leaveGroup(op.param1)
#==============================================================================#
#                elif text.lower() == 'me':
#                    if msg.toType == 2 or msg.toType == 1:
#                        sendMessageWithMention(to, sender)
#                        cl.sendContact(to, sender)
#                    else:
#                        cl.sendContact(to,sender)
#                elif text.lower() == 'mymid':
#                    cl.sendMessage(msg.to,"[MID]\n" +  sender)
#                elif text.lower() == 'myname':
#                    me = cl.getContact(sender)
#                    cl.sendMessage(msg.to,"[Name]\n" + me.displayName)
#                elif text.lower() == 'mybio':
##                    me = cl.getContact(sender)
#                    cl.sendMessage(msg.to,"[StatusMessage]\n" + me.statusMessage)
#                elif text.lower() == 'mypicture':
##                    me = cl.getContact(sender)
#                    cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
#                elif text.lower() == 'myvideoprofile':
#                    me = cl.getContact(sender)
#                    cl.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
#                elif text.lower() == 'mycover':
#                    me = cl.getContact(sender)
#                    cover = cl.getProfileCoverURL(sender)
#                    cl.sendImageWithURL(msg.to, cover)
#                elif msg.text.lower().startswith("contact "):
#                    if 'MENTION' in msg.contentMetadata.keys()!= None:
#                        names = re.findall(r'@(\w+)', text)
#                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
#                        mentionees = mention['MENTIONEES']
#                        lists = []
#                        for mention in mentionees:
#                            if mention["M"] not in lists:
#                                lists.append(mention["M"])
#                        for ls in lists:
#                            contact = cl.getContact(ls)
#                            mi_d = contact.mid
#                            cl.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("/mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "[ Mid User ]"
                        for ls in lists:
                            ret_ += "\n" + ls
                        cl.sendMessage(msg.to, str(ret_))
#                elif msg.text.lower().startswith("name "):
#                    if 'MENTION' in msg.contentMetadata.keys()!= None:
#                        names = re.findall(r'@(\w+)', text)
#                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
#                        mentionees = mention['MENTIONEES']
#                        lists = []
####                        for mention in mentionees:
#                            if mention["M"] not in lists:
#                                lists.append(mention["M"])
#                        for ls in lists:
#                            contact = cl.getContact(ls)
#                            cl.sendMessage(msg.to, "[ 名字 ]\n" + contact.displayName)
#                        for ls in lists:
#                            contact = cl.getContact(ls)
#                            cl.sendMessage(msg.to, "[ 個簽 ]\n" + contact.statusMessage)
#                        for mention in mentionees:
#                            if mention["M"] not in lists:
#                                lists.append(mention["M"])
#                        for ls in lists:
#                            path = "http://dl.profile.line-cdn.net/" + cl.getContact(ls).pictureStatus
#                            cl.sendImageWithURL(msg.to, str(path))
#                        if 'MENTION' in msg.contentMetadata.keys()!= None:
#                            names = re.findall(r'@(\w+)', text)
#                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
#                            mentionees = mention['MENTIONEES']
#                            lists = []
##                            for mention in mentionees:
#                                if mention["M"] not in lists:
 #                                   lists.append(mention["M"])
#                            for ls in lists:
#                                path = cl.getProfileCoverURL(ls)
#                                cl.sendImageWithURL(msg.to, str(path))
#                
#==============================================================================#
#                elif msg.text.lower().startswith("mimicadd "):
#                    targets = []
#                    key = eval(msg.contentMetadata["MENTION"])
#                    key["MENTIONEES"][0]["M"]
 #                   for x in key["MENTIONEES"]:
#                        targets.append(x["M"])
#                    for target in targets:
#                        try:
#                            ban["mimic"]["target"][target] = True
#                            cl.sendMessage(msg.to,"已加入模仿名單!")
#                            break
#                        except:
#                            cl.sendMessage(msg.to,"添加失敗 !")
#                            break
#                elif msg.text.lower().startswith("mimicdel "):
#                    targets = []
#                    key = eval(msg.contentMetadata["MENTION"])
#                    key["MENTIONEES"][0]["M"]
#                    for x in key["MENTIONEES"]:
#                        targets.append(x["M"])
#                    for target in targets:
#                        try:
#                            del settings["模仿名單"]["target"][target]
#                            cl.sendMessage(msg.to,"刪除成功 !")
 #                           break
#                        except:
#                            cl.sendMessage(msg.to,"刪除失敗 !")
#                            break
#                elif text.lower() == 'mimiclist':
#                    if ban["mimic"]["target"] == {}:
 #                       cl.sendMessage(msg.to,"未設定模仿目標")
 #                   else:
#                        mc = "╔══[ Mimic List ]"
#                        for mi_d in ban["mimic"]["target"]:
#                            mc += "\n╠ "+cl.getContact(mi_d).displayName
#                        cl.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
#                elif "mimic" in msg.text.lower():
#                    sep = text.split(" ")
#                    mic = text.replace(sep[0] + " ","")
#                    if mic == "on":
#                        if ban["mimic"]["status"] == False:
#                            ban["mimic"]["status"] = True
#                            cl.sendMessage(msg.to,"Reply Message on")
#                    elif mic == "off":
#                        if ban["mimic"]["status"] == True:
#                            ban["mimic"]["status"] = False
#                            cl.sendMessage(msg.to,"Reply Message off")
#==============================================================================#
#                elif text.lower() == 'groupcreator':
#                    group = cl.getGroup(to)
#                    GS = group.creator.mid
#                    cl.sendContact(to, GS)
#                elif text.lower() == 'groupid':
#                    gid = cl.getGroup(to)
#                    cl.sendMessage(to, "[ID Group : ]\n" + gid.id)
#                elif text.lower() == 'grouppicture':
#                    group = cl.getGroup(to)
#                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
#                    cl.sendImageWithURL(to, path)
#                elif text.lower() == 'groupname':
#                    gid = cl.getGroup(to)
#                    cl.sendMessage(to, "[群組名稱 : ]\n" + gid.name)
#                elif text.lower() == 'grouplink':
#                    if msg.toType == 2:
#                        group = cl.getGroup(to)
#                        if group.preventedJoinByTicket == False:
#                            ticket = cl.reissueGroupTicket(to)
#                            cl.sendMessage(to, "[ Group Ticket ]\nhttps://cl.me/R/ti/g/{}".format(str(ticket)))
#                        else:
#                            cl.sendMessage(to, "Grouplink未開啟 {}openlink".format(str(settings["keyCommand"])))
#                elif text.lower() == 'link on':
#                    if msg.toType == 2:
#                        group = cl.getGroup(to)
#                        if group.preventedJoinByTicket == False:
#                            cl.sendMessage(to, "群組網址已開")
#                        else:
#                            group.preventedJoinByTicket = False
#                            cl.updateGroup(group)
#                            cl.sendMessage(to, "開啟成功")
#                elif text.lower() == 'link off':
#                    if msg.toType == 2:
#                        group = cl.getGroup(to)
#                        if group.preventedJoinByTicket == True:
#                            cl.sendMessage(to, "群組網址已關")
#                        else:
#                            group.preventedJoinByTicket = True
#                            cl.updateGroup(group)
#                            cl.sendMessage(to, "關閉成功")
#                elif text.lower() == 'groupinfo':
#                    group = cl.getGroup(to)
#                    try:
#                        gCreator = group.creator.displayName
#                    except:
#                        gCreator = "不明"
#                    if group.invitee is None:
#                        gPending = "0"
#                    else:
#                        gPending = str(len(group.invitee))
#                    if group.preventedJoinByTicket == True:
#                        gQr = "關閉"
 #                       gTicket = "無"
#                    else:
#                        gQr = "開啟"
#                        gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
#                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
#                    ret_ = "╔══[ Group Info ]"
#                    ret_ += "\n╠ 群組名稱 : {}".format(str(group.name))
#                    ret_ += "\n╠ 群組 Id : {}".format(group.id)
#                    ret_ += "\n╠ 創建者 : {}".format(str(gCreator))
#                    ret_ += "\n╠ 群組人數 : {}".format(str(len(group.members)))
##                    ret_ += "\n╠ 邀請中 : {}".format(gPending)
#                    ret_ += "\n╠ 網址狀態 : {}".format(gQr)
#                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
#                    ret_ += "\n╚══[ Finish ]"
#                    cl.sendMessage(to, str(ret_))
##                    cl.sendImageWithURL(to, path)
#                elif text.lower() == 'groupmemberlist':
#                    if msg.toType == 2:
#                        group = cl.getGroup(to)
#                        ret_ = "╔══[ 成員名單 ]"
#                        no = 0 + 1
#                        for mem in group.members:
#                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
#                            no += 1
#                        ret_ += "\n╚══[ 全部成員共 {} 人]".format(str(len(group.members)))
#                        cl.sendMessage(to, str(ret_))
#                elif text.lower() == 'grouplist':
#                        groups = cl.groups
#                        ret_ = "╔══[ Group List ]"
#                        no = 0 + 1
#                        for gid in groups:
#                            group = cl.getGroup(gid)
#                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
#                            no += 1
#                        ret_ += "\n╚══[ Total {} Groups ]".format(str(len(groups)))
#                        cl.sendMessage(to, str(ret_))
#                elif msg.text.lower().startswith("nk "):
##                    targets = []
#                    key = eval(msg.contentMetadata["MENTION"])
#                    key["MENTIONEES"][0]["M"]
#                    for x in key["MENTIONEES"]:
#                        targets.append(x["M"])
#                    for target in targets:
#                        if target in admin or target in owners:
 #                           pass
#                        else:
#                            try:
#                                cl.sendMessage(to,"幹你娘去死啦")
#                                cl.kickoutFromGroup(msg.to,[target])
 #                           except:
#                                cl.sendMessage(to,"Error")
  #              
#                elif "Zk" in msg.text:
#                    gs = cl.getGroup(to)
#                    targets = []
 #                   for g in gs.members:
#                        if g.displayName in "":
#                            targets.append(g.mid)
####                    if targets == []:
#                        pass
#                    else:
#                        for target in targets:
#                            if target in admin:
##                                pass
#                            else:
#                                try:
#                                    cl.kickoutFromGroup(to,[target])
#                                except:
#                                    pass
#
#                elif msg.text.lower().startswith("ri "):
#                    targets = []
#                    key = eval(msg.contentMetadata["MENTION"])
#                    key["MENTIONEES"][0]["M"]
#                    for x in key["MENTIONEES"]:
#                        targets.append(x["M"])
#                    for target in targets:
#                        try:
#                            cl.sendMessage(to,"免費ANA全日空來回機票一張ww 感謝您的搭乘 歡迎再次搭乘本航班")
#                            cl.kickoutFromGroup(msg.to,[target])
 #                           cl.inviteIntoGroup(to,[target])
#                        except:
#                            cl.sendMessage(to,"Error")
#                elif text.lower() == 'byeall':
#                    if msg.toType == 2:
 #                       print ("[ 19 ] KICK ALL MEMBER")
#                        _name = msg.text.replace("Byeall","")
#                        gs = cl.getGroup(msg.to)
#                        cl.sendMessage(msg.to,"冥魔军に栄光あれ☆")
#                        targets = []
#                        for g in gs.members:
#                            if _name in g.displayName:
#                                targets.append(g.mid)
#                        if targets == []:
#                            cl.sendMessage(msg.to,"Not Found")
#                        else:
#                            for target in targets:
#                                if target in admin or target in owners:
#                                    pass
#                                else:
#                                    try:
#                                        cl.kickoutFromGroup(msg.to,[target])
#                                        print (msg.to,[g.mid])
#                                    except:
#                                        cl.sendMessage(msg.to,"")
 ##               elif ("Gn " in msg.text):
#                    if msg.toType == 2:
#                        X = cl.getGroup(msg.to)
#                        X.name = msg.text.replace("Gn ","")
#                        cl.updateGroup(X)
#                    else:
#                        cl.sendMessage(msg.to,"It can't be used besides the group.")
#                elif text.lower() == 'cancel':
#                    if msg.toType == 2:
#                        group = cl.getGroup(to)
#                        gMembMids = [contact.mid for contact in group.invitee]
#                    for _mid in gMembMids:
#                        cl.cancelGroupInvitation(msg.to,[_mid])
#                    cl.sendMessage(msg.to,"已取消所有邀請!")
#                elif ("Inv " in msg.text):
#                    if msg.toType == 2:
#                        midd = msg.text.replace("Inv ","")
#                        cl.findAndAddContactsByMid(midd)
#                        cl.inviteIntoGroup(to,[midd])
#==============================================================================#
#                elif text.lower() == 'tagall':
#                    group = cl.getGroup(msg.to)
#                    nama = [contact.mid for contact in group.members]
#                    k = len(nama)//100
#                    for a in range(k+1):
#                        txt = u''
#                        s=0
#                        b=[]
#                        for i in group.members[a*100 : (a+1)*100]:
#                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
#                            s += 7
#                            txt += u'@Alin \n'
#                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
#                        cl.sendMessage(to, "Total {} Mention".format(str(len(nama))))
#                elif text.lower() == 'zt':
#                    gs = cl.getGroup(to)
#                    targets = []
#                    for g in gs.members:
##                        if g.displayName in "":
#                            targets.append(g.mid)
#                    if targets == []:
#                        pass
#                    else:
#                        for target in targets:
#                            sendMessageWithMention(to,target)
 #               elif text.lower() == 'zm':
#                    gs = cl.getGroup(to)
#                    targets = []
####                    for g in gs.members:
#                        if g.displayName in "":
#                            targets.append(g.mid)
#                    if targets == []:
#                        pass
#                    else:
#                        for mi_d in targets:
#                           cl.sendContect(to,mi_d)
                elif text.lower() == '#stread':
                    cl.sendMessage(msg.to, "已讀點設置成功")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                    except:
                        pass
                    now2 = datetime.now()
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = datetime.strftime(now2,"%H:%M")
                    wait2['ROM'][msg.to] = {}
                elif text.lower() == "#clread":
                    cl.sendMessage(to, "已讀點已刪除")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                        del wait2['setTime'][msg.to]
                    except:
                        pass
                elif msg.text in ["#lkread","#Lkread"]:
                    if msg.to in wait2['readPoint']:
                        if wait2["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait2["ROM"][msg.to].items():
                                chiya += rom[1] + "\n"
                        cl.sendMessage(msg.to, "[已讀順序]%s\n\n[已讀的人]:\n%s\n查詢時間:[%s]" % (wait2['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        cl.sendMessage(msg.to, "請輸入#stread")

#==============================================================================#
#                elif msg.text.lower().startswith("ban "):
#                    targets = []
#                    key = eval(msg.contentMetadata["MENTION"])
#                    key["MENTIONEES"][0]["M"]
#                    for x in key["MENTIONEES"]:
#                        targets.append(x["M"])
#                    for target in targets:
#                        try:
#                            ban["blacklist"][target] = True
##                            cl.sendMessage(msg.to,"已加入黑單!")
#                            break
#                        except:
#                            cl.sendMessage(msg.to,"添加失敗 !")
##                            break
#                elif msg.text == "ban contact":
#                    client.sendMessage(msg.to,"請丟出好友資料")
#                    ban["blacklist"][msg.contentMetadata] = True
#                elif "Ban:" in msg.text:
#                    mmtxt = text.replace("Ban:","")
#                    try:
#                        ban["blacklist"][mmtext] = True
#                        cl.sendMessage(msg.to,"已加入黑單!")
#                    except:
#                        cl.sendMessage(msg.to,"添加失敗 !")
#                elif msg.text.lower().startswith("unban "):
#                    targets = []
#                    key = eval(msg.contentMetadata["MENTION"])
#                    key["MENTIONEES"][0]["M"]
##                    for x in key["MENTIONEES"]:
#                        targets.append(x["M"])
 #                   for target in targets:
#                        try:
#                            del ban["blacklist"][target]
#                            cl.sendMessage(msg.to,"刪除成功 !")
#                            break
#                        except:
#                            cl.sendMessage(msg.to,"刪除失敗 !")
#                            break
#                elif text.lower() == 'banlist':
#                    if ban["blacklist"] == {}:
#                        cl.sendMessage(msg.to,"無黑單成員!")
#                    else:
#                        mc = "╔══[ Black List ]"
#                        for mi_d in ban["blacklist"]:
#                            mc += "\n╠ "+cl.getContact(mi_d).displayName
#                        cl.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
#                elif text.lower() == 'nkban':
#                    if msg.toType == 2:
#                        group = cl.getGroup(to)
#                        gMembMids = [contact.mid for contact in group.members]
#                        matched_list = []
 #                   for tag in ban["blacklist"]:
 #                       matched_list+=filter(lambda str: str == tag, gMembMids)
#                    if matched_list == []:
 #                       cl.sendMessage(msg.to,"There was no blacklist user")
#                        return
#                    for jj in matched_list:
#                        cl.kickoutFromGroup(msg.to,[jj])
#                    cl.sendMessage(msg.to,"Blacklist kicked out")
#                elif text.lower() == 'cleanban':
 ##                   for mi_d in ban["blacklist"]:
#                        ban["blacklist"] = {}
#                    cl.sendMessage(to, "已清空黑名單")
#                elif text.lower() == 'banmidlist':
#                    if ban["blacklist"] == {}:
#                        cl.sendMessage(msg.to,"無黑單成員!")
#                    else:
#                        mc = "╔══[ Black List ]"
#                        for mi_d in ban["blacklist"]:
#                            mc += "\n╠ "+mi_d
#                        cl.sendMessage(to,mc + "\n╚══[ Finish ]")
#
#==============================================================================#
                elif text.lower() == 'backlist':
                    ret = "[關鍵字列表]\n"
                    for name in settings['react']:
                        ret +="->" + name + "\n"
                    cl.sendMessage(to, ret)
                if msg.text in settings['react']:
                    cl.sendMessage(to, settings['react'][msg.text])
                elif msg.text.lower().startswith("back_add"):
                    list_ = msg.text.split(":")
                    if list_[1] not in settings['react']:
                        try:
                            settings['react'][list_[1]] = list_[2]
                            with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "[新增回應]\n" + "關鍵字: " + list_[1])
                        except:
                            cl.sendMessage(to, "新增關鍵字失敗")
                    else:
                        cl.sendMessage(to, "關鍵字已存在")
                elif msg.text.lower().startswith("back_del"):
                    list_ = msg.text.split(":")
                    if list_[1] in settings['react']:
                        try:
                            del settings['react'][list_[1]]
                            with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "[刪除關鍵字]\n成功刪除關鍵字\n關鍵字:")
                        except:
                            cl.sendMessage(to, "刪除關鍵字失敗")
                    else:
                        cl.sendMessage(to, "[ERROR]\n指定刪除的關鍵字並不在列表中!!!")
                elif msg.text.lower().startswith("update_back"):
                    list_ = msg.text.split(":")


#==============================================================================#
#                elif "Fbc:" in msg.text:
#                    bctxt = text.replace("Fbc:","")
#                    t = cl.getAllContactIds()
#                    for manusia in t:
#                        cl.sendMessage(manusia,(bctxt))
#                elif "Gbc:" in msg.text:
#                    bctxt = text.replace("Gbc:","")
#                    n = cl.getGroupIdsJoined()
#                    for manusia in n:
#                        cl.sendMessage(manusia,(bctxt))
#                elif "Copy " in msg.text:
#                    targets = []
#                    key = eval(msg.contentMetadata["MENTION"])
#                    key["MENTIONEES"][0]["M"]
#                            lol = cl.getProfile()
#                            lol.statusMessage = Y
#                            cl.updateProfile(lol)
#                            path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
#                            P = contact.pictureStatus
#                            cl.updateProfilePicture(P)
#                        except Exception as e:
#                            cl.sendMessage(to, "Failed!")
#            if text.lower() == 'cc9487':
#                if sender in ['ua10c2ad470b4b6e972954e1140ad1891']:
#                    python = sys.executable
#                    os.execl(python, python, *sys.argv)
#                else:
#                    pass
#==============================================================================#
#            if msg.contentType == 13:
#                if settings["getmid"] == True:
#                    if 'displayName' in msg.contentMetadata:
#                        contact = cl.getContact(msg.contentMetadata["mid"])
#                        cl.sendMessage(msg.to,"[mid]:\n" + msg.contentMetadata["mid"])
#                    else:
#                        cl.sendMessage(msg.to,"[mid]:\n" + msg.contentMetadata["mid"])
#            elif msg.contentType == 16:
#                if settings["timeline"] == True:
#                    msg.contentType = 0
#                    msg.text = "文章網址：\n" + msg.contentMetadata["postEndUrl"]
#                  #  detail = cl.downloadFileURL(to,msg,msg.contentMetadata["postEndUrl"])
#                    cl.sendMessage(msg.to,msg.text)
#==============================================================================#
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    cl.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in ban["mimic"]["target"] and ban["mimic"]["status"] == True and ban["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        cl.sendMessage(msg.to,text)
#                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
#                    if 'MENTION' in msg.contentMetadata.keys()!= None:
#                        names = re.findall(r'@(\w+)', text)
#                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
#                        mentionees = mention['MENTIONEES']
#                        lists = []
#                        for mention in mentionees:
#                            if clMID in mention["M"]:
#                                if settings["detectMention"] == True:
#                                    contact = cl.getContact(sender)
#                                    sendMessageWithMention(to, contact.mid)
##                                    cl.sendMessage(to, "幹你娘標三小")
#                                break
#            try:
#                msg = op.message
#                if settings["reread"] == True:
#                    if msg.toType == 0:
#                        cl.log("[%s]"%(msg._from)+msg.text)
#                    else:
#                        cl.log("[%s]"%(msg.to)+msg.text)
#                    if msg.contentType == 0:
#                        msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
#                    elif msg.contentType == 7:
#                        stk_id = msg.contentMetadata['STKID']
#                        msg_dict[msg.id] = {"text":"貼圖id:"+str(stk_id),"from":msg._from,"createdTime":msg.createdTime}
#                else:
#                    pass
#            except Exception as e:
#                print(e)
#
#==============================================================================#
        if op.type == 65:
            print ("[ 65 ] REREAD")
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            timeNow = datetime.now()
                            timE = datetime.strftime(timeNow,"(%y-%m-%d %H:%M:%S)")
                            try:
                                strt = int(3)
                                akh = int(3)
                                akh = akh + 8
                                aa = """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(msg_dict[msg_id]["from"])+"},"""
                                aa = (aa[:int(len(aa)-1)])
                                cl.sendMessage(at, "收回訊息者 @wanping ", contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                            except Exception as e:
                                print(str(e))
                            cl.sendMessage(at,"[收回訊息者]\n%s\n[訊息內容]\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                            cl.sendMessage(at,"/n發送時間/n"+strftime("%y-%m-%d %H:%M:%S")+"/n收回時間/n"+timE)
                            
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print (e)
#==============================================================================#
        if op.type == 55:
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
            try:
                if op.param1 in wait2['readPoint']:
                    Name = cl.getContact(op.param2).displayName
                    Mid = cl.getContact(op.param2).mid
                    if Name in wait2['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += "\n[※]" + Name
                        wait2['ROM'][op.param1][op.param2] = "[※]" + Name
                        cl.sendMessage(op.param1, "紀錄" + Name)
                        cl.sendContact(op.param1, Mid)
                        print (time.time() + name)
                else:
                    pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
#==============================================================================#
               
