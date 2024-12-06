from kcweb.common import *
from kcwebplus import config
kcwebpluspath=(os.path.split(os.path.realpath(__file__))[0]).replace('\\','/')[:-7] #框架目录
class systekcwebplus:
    def getbanddomain(addtype='system'):
        """获取绑定域名
        """
        if os.path.isfile('app/intapp/controller/soft/nginx.py'):
            nginx=getfunction('app.intapp.controller.soft.nginx')
            status,lists,count=nginx.weblist(pagenow=1,pagesize=1,kw='kcwebplus域名映射',addtype=addtype)
            if not status:
                return False,lists
            else:
                if len(lists):
                    webitem=lists[0]
                else:
                    webitem={}
                return True,webitem
        else:
            return False,'需要先在插件管理中安装“软件管理”'
    def banddomainall(domain,proxy_pass=[],addtype='system'):
        """绑定域名/修改多个代理
        
        domain 域名 必填 该方法生次使用时必填

        proxy_pass 代理信息 格式：[{'types':'http','rule':'/','url':''}]
        """
        if os.path.isfile('app/intapp/controller/soft/nginx.py'):
            nginx=getfunction('app.intapp.controller.soft.nginx')
            status,lists,count=nginx.weblist(pagenow=1,pagesize=1,kw='kcwebplus域名映射',addtype=addtype)
            if not status:
                return False,lists
            webitem={
                'id':'','log_switch':0,'domain':domain,'port':'80','title':'kcwebplus域名映射',
                'describes':'','path':'','webtpl':'balancing','client_max_body_size':20,
                'balancing':[{'ip':'127.0.0.1','port':'39001','type':'weight','val':1}],
                'proxy_set_header':[],'header':[],'aliaslists':[],'ssl':'','key':'','pem':'',
                'rewrite':'','ssl_certificate':'','ssl_certificate_key':'','other':{'phppath':'','proxy_pass':proxy_pass},'cusconfdata':'','denylist':[]
            }
            if len(lists):
                webitem=lists[0]
                if domain:
                    webitem['domain']=domain
                    webitem['other']={'phppath':'','proxy_pass':proxy_pass}
            status,msg=nginx.funadd_web(data=webitem,addtype=addtype)
            return status,msg
        else:
            return False,'需要先在插件管理中安装“软件管理”'
    def banddomain(proxyitem,domain='',addtype='system'):
        """绑定域名/增加代理
        
        proxyitem 代理信息 必填 格式：{'types':'http','rule':'/','url':''} 

        domain 域名 非必填 该方法生次使用时必填
        """
        if os.path.isfile('app/intapp/controller/soft/nginx.py'):
            nginx=getfunction('app.intapp.controller.soft.nginx')
            status,lists,count=nginx.weblist(pagenow=1,pagesize=1,kw='kcwebplus域名映射',addtype=addtype)
            if not status:
                return False,lists
            if not len(lists):
                if not domain:
                    return False,'请绑定域名'
            webitem={
                'id':'','log_switch':0,'domain':domain,'port':'80','title':'kcwebplus域名映射',
                'describes':'','path':'','webtpl':'balancing','client_max_body_size':20,
                'balancing':[{'ip':'127.0.0.1','port':'39001','type':'weight','val':1}],
                'proxy_set_header':[],'header':[],'aliaslists':[],'ssl':'','key':'','pem':'',
                'rewrite':'','ssl_certificate':'','ssl_certificate_key':'','other':{'phppath':'','proxy_pass':[proxyitem]},'cusconfdata':'','denylist':[]
            }
            if len(lists):
                webitem=lists[0]
                if domain:
                    webitem['domain']=domain
                    if proxyitem not in webitem['other']['proxy_pass']:
                        webitem['other']['proxy_pass'].append(proxyitem)
            status,msg=nginx.funadd_web(data=webitem,addtype=addtype)
            return status,msg
        else:
            return False,'需要先在插件管理中安装“软件管理”'
    def delproxy(proxyitem,addtype='system'):
        """删除指定代理
        
        proxyitem 代理信息 必填 格式：{'types':'http','rule':'/','url':''}
        """
        if os.path.isfile('app/intapp/controller/soft/nginx.py'):
            nginx=getfunction('app.intapp.controller.soft.nginx')
            status,lists,count=nginx.weblist(pagenow=1,pagesize=1,kw='kcwebplus域名映射',addtype=addtype)
            if not status:
                return False,lists
            if len(lists):
                webitem=lists[0]
                proxy_pass=webitem['other']['proxy_pass']
                proxy_passarr=[]
                for k in webitem['other']['proxy_pass']:
                    if k!=proxyitem:
                        proxy_passarr.append(k)
                webitem['other']['proxy_pass']=proxy_passarr
                status,msg=nginx.funadd_web(data=webitem,addtype=addtype)
                return status,msg
            else:
                return False,'未绑定域名'
        else:
            return False,'需要先在插件管理中安装“软件管理”'