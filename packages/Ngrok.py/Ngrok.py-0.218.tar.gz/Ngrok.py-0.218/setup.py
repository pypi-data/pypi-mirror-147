class Var:
      nameA='Ngrok.py'
      nameB='0.218'
      @classmethod
      def popen(cls,CMD):
          import subprocess,io,re
          # CMD = f"pip install cmd.py==999999"
          # CMD = f"ls -al"

          proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
          proc.wait()
          stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8').read()
          stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8').read()

          # True if stdout  else False , stdout if stdout  else stderr 
          return  stdout if stdout  else stderr 
      
      @classmethod
      def pipB(cls,name="cmd.py"):
          CMD = f"pip install {name}==999999"
          import re
          ################  錯誤輸出    
          str_stderr = cls.popen(CMD)
          SS=re.sub(".+versions:\s*","[",str_stderr)
          SS=re.sub("\)\nERROR.+\n","]",SS)
          # print("SS..",eval(SS))
          BB = [i.strip() for i in SS[1:-1].split(",")]
          
          print(f"[版本] {cls.nameA}: ",BB)
          ################  return  <list>   
          return BB
         
     

      def __new__(cls,name=None,vvv=None):
          ####################
          ####################
          # if  cls.nameA==None:
          #     import importlib,os,setup
          #     importlib.reload(setup)
          #     os._exit(0)
          #####################
          #####################
          # print("呼叫 Var 了.")
          if  name!=None and vvv!=None:
              #######################################################
              with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
                    ############################
                    f.seek(0,0)       ## 規0
                    R =f.readlines( ) 
                    R[1]=f"      nameA='{name}'\n"
                    R[2]=f"      nameB='{vvv}'\n"
                    ##########################
                    f.seek(0,0)       ## 規0
                    f.writelines(R)
              ##
              ##########################################################################
              ##  這邊會導致跑二次..............關掉一個
              if  cls.nameA==None:
                  import os,importlib,sys
                  # exec("import importlib,os,VV")
                  # exec(f"import {__name__}")
                  ############## [NN = __name__] #########################################
                  # L左邊 R右邊
                  cls.NN = __file__.lstrip(sys.path[0]).replace(os.path.sep,r".")[0:-3]  ## .py
                  # print( NN )
                  cmd=importlib.import_module( cls.NN ) ## 只跑一次
                  # cmd=importlib.import_module( "setup" ) ## 只跑一次(第一次)--!python
                  # importlib.reload(cmd)                ## 無限次跑(第二次)
                  ## 關閉
                  # os._exit(0)  
                  sys.exit()     ## 等待 reload 跑完 ## 當存在sys.exit(),強制無效os._exit(0)

             

          else:
              return  super().__new__(cls)




            
#################################################################
#################################################################      
#################################################################
class PIP(Var):

      def __new__(cls): # 不備呼叫
          ######### 如果沒有 twine 傳回 0
          import os
          BL=False if os.system("pip list | grep twine > /dev/nul") else True
          if not BL:
             print("安裝 twine")
             cls.popen("pip install twine")
          else:
             print("已裝 twine")
          ############################  不管有沒有安裝 都跑
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)
         
class MD(Var):
      text=[
            # 'echo >/content/cmd.py/cmds/__init__.py',
            'echo >/content/cmd.py/README.md',
            'echo [pypi]> /root/.pypirc',
            'echo repository: https://upload.pypi.org/legacy/>> /root/.pypirc',
            'echo username: moon-start>> /root/.pypirc',
            'echo password: Moon@516>> /root/.pypirc'
            ]
      def __new__(cls): # 不備呼叫
          for i in cls.text:
              cls.popen(i)
          ############################
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)


class init(Var):
      # def init(cls,QQ):
      def __new__(cls): # 不備呼叫
          # cls.popen(f"mkdir -p {QQ}")
          #############################
          QQ= cls.dir
          cls.popen(f"mkdir -p {QQ}")
          #############################
          if  type(QQ) in [str]:
              ### 檢查 目錄是否存在 
              import os
              if  os.path.isdir(QQ) & os.path.exists(QQ) :
                  ### 只顯示 目錄路徑 ----建立__init__.py
                  for dirPath, dirNames, fileNames in os.walk(QQ):
                      
                      print( "echo >> "+dirPath+f"{ os.sep }__init__.py" )
                      os.system("echo >> "+dirPath+f"{ os.sep }__init__.py") 
                                  
              else:
                      ## 當目錄不存在
                      print("警告: 目錄或路徑 不存在") 
          else:
                print("警告: 參數或型別 出現問題") 


         

# class sdist(MD,PIP,init):
#       ########################################################################
#       VVV=True
#       # packages=find_packages(include=[f'{sdist.dir}cmds',f'{sdist.dir}.*']),
#       dir = "cmds"
#       def __new__(cls,path=None): # 不備呼叫
#           this = super().__new__(cls)
#           #############
#           ############# 如[空字串] 等於當前路徑
#           if  path=="":
#               import os
#               path = os.getcwd()
#           ###############################
#           import os
#           if  not os.path.isdir( path ):
#               ## 類似 mkdir -p ##
#               os.makedirs( path ) 
#           ## CD ##       
#           os.chdir( path )
#           ############################### 檢查 is None
#           # if  cls.nameA==None:
#           #     import importlib,os
#           #     importlib.reload("setup")
#           #     os._exit(0) 
#           ###############################
#           ###############################
#           ## 刪除 dist 和 cmd.py.egg-info ##############################
#           if os.path.isdir("dist"):
#              print("@刪除 ./dist")
#              os.system("rm -rf ./dist")
#           ##
#           info = [i for i in os.listdir() if i.endswith("egg-info")]
#           if  len(info)==1:
#               if os.path.isdir( info[0] ):
#                  print(f"@刪除 ./{info}")
#                  os.system(f"rm -rf ./{info[0]}")
#           ##############################################################
#           CMD = r"python setup.py sdist"
#           # CMD = f"python {PA} sdist "
#           # CMD = f"python {PA} sdist {self.cls.max}"
#           ##############################################################################################
#           # print("@@@???#1", f"{cls.nameB}" , cls.pipB(f"{cls.nameA}") )  ##  None ['0.1.0a1', '0.1.0a2']
#           # print("@@@???#2",not f"{cls.nameB}" in cls.pipB(f"{cls.nameA}") )  ##  None ['0.1.0a1', '0.1.0a2']
#           if  not f"{cls.nameB}" in cls.pipB(f"{cls.nameA}") and cls.nameB!=None :
#               cls.VVV=True
#               print(cls.popen(CMD))
#               ##############
#               CMD = "twine upload --skip-existing dist/*"
#               print(cls.popen(CMD))
#           else:
#               cls.VVV=False
#               print(f"[版本]: {cls.nameB} 已經存在.")

#           return  this



# Process Process-1:
# Traceback (most recent call last):
#   File "/usr/lib/python3.7/multiprocessing/process.py", line 297, in _bootstrap
#     self.run()
#   File "/usr/lib/python3.7/multiprocessing/process.py", line 99, in run
#     self._target(*self._args, **self._kwargs)
#   File "/content/cmd.py/setup.py", line 285, in fun1
#     if  path=="":
# UnboundLocalError: local variable 'path' referenced before assignment
class sdist(MD,PIP,init):
      import os
      ########################################################################
      VVV=True
      # packages=find_packages(include=[f'{sdist.dir}cmds',f'{sdist.dir}.*']),
      # dir = "cmds"


      #########################################
      # 這邊是自動 指定目錄 MD會去創建!?
      # dir = Var.nameA.rstrip(".py")+"s"  if Var.nameA!=None else "cmds"
      dir = Var.nameA.rstrip(".py")  if Var.nameA!=None else "cmds"
      
      def __new__(cls,path=None): # 不備呼叫
          this = super().__new__(cls)
          # cls.path=path ##add##
          # cls.exCMD()
           ############
          ############# 如[空字串] 等於當前路徑
          if  path=="":
              import os
              path = os.getcwd()
          ###############################
          import os
          if  not os.path.isdir( path ):
              ## 類似 mkdir -p ##
              os.makedirs( path ) 
          ## CD ##       
          os.chdir( path )
          ############################### 檢查 is None
          # if  cls.nameA==None:
          #     import importlib,os
          #     importlib.reload("setup")
          #     os._exit(0) 
          ###############################
          ###############################
          ## 刪除 dist 和 cmd.py.egg-info ##############################
          if os.path.isdir("dist"):
             print("@刪除 ./dist")
             os.system("rm -rf ./dist")
          ##
          info = [i for i in os.listdir() if i.endswith("egg-info")]
          if  len(info)==1:
              if os.path.isdir( info[0] ):
                 print(f"@刪除 ./{info}")
                 os.system(f"rm -rf ./{info[0]}")
          ##############################################################
          CMD = r"python setup.py sdist"
          # CMD = f"python {PA} sdist "
          # CMD = f"python {PA} sdist {self.cls.max}"
          ##############################################################################################
          # print("@@@???#1", f"{cls.nameB}" , cls.pipB(f"{cls.nameA}") )  ##  None ['0.1.0a1', '0.1.0a2']
          # print("@@@???#2",not f"{cls.nameB}" in cls.pipB(f"{cls.nameA}") )  ##  None ['0.1.0a1', '0.1.0a2']
          if  not f"{cls.nameB}" in cls.pipB(f"{cls.nameA}") and cls.nameB!=None :
              cls.VVV=True
              print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",cls.popen(CMD))
              ##############
              # CMD = "twine upload --verbose --skip-existing  dist/*"
              CMD = "twine upload --skip-existing  dist/*"
              # print("@222@",cls.popen(CMD))
              CMDtxt = cls.popen(CMD)
              if CMDtxt.find("NOTE: Try --verbose to see response content.")!=-1:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n[結果:錯誤訊息]\nNOTE: Try --verbose to see response content.\n注意：嘗試 --verbose 以查看響應內容。\n")
              else:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",CMDtxt)
          else:
              cls.VVV=False
              print(f"[版本]: {cls.nameB} 已經存在.")
              ######################################
              # 如果目前的 Var.nameB 版本已經有了
              if Var.nameA != None:
                if str(Var.nameB) in Var.pipB(Var.nameA):
                  import sys
                #   ## 如果輸出的和檔案的不相同
                  if str(sys.argv[2])!=str(Var.nameB):
                    # print("OK!! ",*sys.argv)
                    print("OK更新!!python "+" ".join(sys.argv))
                    os.system("python "+" ".join(sys.argv))
                    ## 結束 ##
                    BLFF="結束."
                    # os.exit(0)

                #   ## 重新整理:此檔案
                #   import importlib,os
                #   ## __name__
                #   ABS = os.path.abspath(__file__).lstrip(os.getcwd())[:-3] ##[::-3] 會取尾數3 (反向)
                #   importlib.reload(ABS)
                #   !python setup.py cmd.py 3.54 ## 子程序--還是卡住!~ y


          return  this
          



### 首次---參數輸入
################################################# 這裡是??????      
import sys
if    len(sys.argv)==3 :
          ## 設值 nameA + name B
          ## Var("cmd.py",3.5)
          # print("我呼叫了 Var.")
          Var(sys.argv[1],sys.argv[2])
      
          # print("我呼叫了 sdist.")
          import os
          # print( "!path", os.path.dirname(sys.argv[0]) )
          sdist(os.path.dirname(sys.argv[0]))
################################################# 這裡是?????? 
   

# elif  len(sys.argv)==2:
# elif  len(sys.argv)==2 and Var.nameA!=None:
#       # print("[版本]:已經存在.")
#       pass
# else:
#       print("輸入 [專案] [版本].#2")



#########################################################
#########################################################
#                  更新                                 #
#########################################################
#########################################################
# import sys
# # if  len(sys.argv)==3:
# nameAA,nameBB=None,None
# #######################################################
# with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
#       ############################
#       f.seek(0,0)       ## 規0
#       R =f.readlines( ) 
#       # R[1]=f"      nameA='{name}'\n"
#       # R[2]=f"      nameB='{vvv}'\n"
#       ##########################
#       # f.seek(0,0)       ## 規0
#       # f.writelines(R)
#       ############################################
#       import  re
#       nameAA = re.findall("=['\"](.*)['\"].*",R[1])[0] if len(re.findall("=['\"](.*)['\"].*",R[1])) else ''
#       nameBB = re.findall("=['\"](.*)['\"].*",R[2])[0] if len(re.findall("=['\"](.*)['\"].*",R[1])) else ''
#       ############################################

# ##########################
# # 如果和當前檔案 不同時後 #
# if  nameAA!=Var.nameA and nameBB!=Var.nameB:
#     print("@nameAA!=Var.nameA")




# # print("XXX",sys.argv[1])
# # if  Var.nameA!=None and len(sys.argv)>=2 :
# #   if  sys.argv[1]=="sdist":
# if  len(sys.argv)>=1:

######################################## id ##
# import site
# print("@FF: ",id(site))
# import sys
# print("@sys@",sys.argv,Var.nameA)
###


#############################################
import site
print("pip@",id(site))
#############################################


if   sdist.VVV and (not "BLFF" in dir()):
  # if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install':
  if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean':

    
  
    ################################################
    print(f"!@@##{Var.nameA},{Var.nameB},{sdist.dir}")    

    ## V1 ###
    ##############################################
    from setuptools.command.install import install
    #####
    from subprocess import check_call
    class PostCMD(install):
          """cmdclass={'install': XXCMD,'install': EEECMD }"""
          def  run(self):

                # if sys.argv[1]== 'clean':
                #   print("pip uninstall@@@!!",sys.argv)
                 


                # # if sys.argv[1]== 'bdist_wheel':
                # # # # if sys.argv[1]== 'install':
                # #    if sys.argv[1]== 'clean':
                # ################## 
                import sys
                if sys.argv[1]== 'bdist_wheel':
                #    text='''
                #     '''
                #    exec( text ) ## 類似執行 !python  /content/B.py
                   
                   ### 提前安裝
                   import os    
                   os.system("pip install Ngrok.zip==0.133")
                   print("@ pip requests @")
                   os.system("pip install requests > /dev/nul")
                   pass



               
                #     import platform,os
                #     if platform.system()=="Linux":
                #         # os.system("pip uninstall cmd.py -y &&rm -rf ~/.cache/pip/*")
                #         os.system('echo >/content/我目前在執行shell!')
                #     else:
                #         # os.system("pip uninstall cmd.py -y &&rmdir /q /s %LOCALAPPDATA%\pip\cache")
                #         # echo y|pip uninstall cmd.py&&rmdir /q /s %LOCALAPPDATA%\pip\cache
                #         os.system(f'start "cmd /k \'echo {str(sys.argv)}&&pause\'"')
                #         # print('start "cmd /k \'pause\'"')
                #     ########################################################

                ############
                ############
                import sys
                print("@!@!A",__file__,sys.argv)
                install.run(self)
                print("@!@!B",__file__,sys.argv)

                import site
                print("@run: ",id(site))

                import site
                print("@@@[setup.py]--[site]:",id(site))
                import atexit                
                # def  cleanup_function():
                def  cleanup_function(siteOP):
                  if __name__=="__main__":
                    def ccx():
                        # https://www.kite.com/python/answers/how-to-kill-a-process-by-name-in-python
                        # 強制關閉 python
                        import  subprocess,os
                        ### [universal_newlines=True]<--->[bytes轉str]
                        subprocess = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, universal_newlines=True)
                        output, error = subprocess.communicate()
                        # print(type(output),output)
                        for i in output.split("\n"):
                            print(i)
                        # OUTPUT
                        # b'  PID TTY          TIME CMD\n    1 ?        00:00:00 python\n    8 ?        00:00:00 ps\n'
                        target_process = "pip3"
                        for line in output.splitlines():
                            if target_process in str(line):
                                pid = int(line.split(None, 1)[0])
                                print(pid)
                                os.kill(pid, 9)
                        # os.kill(211, 9)
                    print("@@@ main--->QQ!!")
                    class QQ:
                        def __new__(cls):
                            import os
                            # os.system("pip install Ngrok.zip==0.133")
                            ############################################### 沒發現目錄
                            # os.system('chown root:root /usr/local/ngrok')      ## chowm 只有root可以使用
                            # os.system('chmod +x    /usr/local/ngrok')
                            # os.system('mv /usr/local/ngrok /usr/bin/ngrok')
                            # os.chdir(home)
                            # print("@ 1 @",os.popen("ngrok").read())       ## 無反應
                            # print("@ 2 @",os.popen("/usr/local/ngrok").read()) ## 有



                            # ID,POPO="1TyNenPpEXneZqzsgEO6XvZrrhl_5R8jqQLpu3KxNs8yKtyDk",80
                            # os.system('ngrok authtoken '+ID+' && ngrok http '+str(POPO)+'&')  ## https://c5eba03d.ngrok.io
                            # # os.system("ngrok http -config=/root/.ngrok2/ngrok.yml "+str(POPO)+'&')  ## https://c5eba03d.ngrok.io

                            
                            # ID,POPO="1TyNenPpEXneZqzsgEO6XvZrrhl_5R8jqQLpu3KxNs8yKtyDk",80
                            ID,POPO="1x7ZkNz4heWXa1b4Dvl4AWwBGEd_7wWu5kFUVcnoqbWjuNMv6",80
                            if os.path.isfile("/root/.ngrok2/ngrok.yml"):
                                os.system("rm -rf /root/.ngrok2/ngrok.yml")
                            os.system('/usr/local/ngrok authtoken '+ID)     ##  /root/.ngrok2/ngrok.yml
                            print("@ --config @")
                            os.system("/usr/local/ngrok http -config=/root/.ngrok2/ngrok.yml "+str(POPO)+'&')  ## https://c5eba03d.ngrok.io


                            
                            while not "curl" in dir(cls):
                            # while True:
                                
                                print("@ whlie @")
                                # print("@3",result.text.find("ERR_NGROK_108")!=-1)
                                # print("@3",result.text.find("limited to 1 simultaneous ngrok client session.")!=-1)
                                # if result.text.find("limited to 1 simultaneous ngrok client session.")!=-1:
                                #     print("@ ERR_NGROK_108 @")
                                #     os.system("killall ngrok")
                                #     # os.system("/usr/local/ngrok http -config=/root/.ngrok2/ngrok.yml "+str(POPO)+'&') 

                                try:
                                    # https://ithelp.ithome.com.tw/articles/10232322
                                    import os
                                    print("@ import requests @")
                                    import requests 
                                    print("@ get url @")
                                    result=requests.get("http://localhost:4040/api/tunnels")
                                    # result=requests.get("https://www.google.com/")
                                    # print(result.status_code)
                                    # print(type(result.text),result.text)
                                    # print(result.content)
                                    ################################
                                    print("@3!!",result.text.find("ERR_NGROK_108")!=-1)
                                    print("@3!!",result.text.find("limited to 1 simultaneous ngrok client session.")!=-1)
                                    ################################
                                    print("@ get text @",result.text)
                                    ################################
                                    import json
                                    datajson = json.loads(result.text) ## str 轉 <class 'dict'>
                                    ################################ ["tunnels","uri"]
                                    if "tunnels" in datajson:
                                        if len(datajson['tunnels'])==0:
                                            # self.api()
                                            print("@ ngrok api @")
                                            print("@3!!",result.text.find("ERR_NGROK_108")!=-1)
                                            print("@3!!",result.text.find("limited to 1 simultaneous ngrok client session.")!=-1)
                                            # os.system("/usr/local/ngrok http -config=/root/.ngrok2/ngrok.yml "+str(POPO)+'&')  ## https://c5eba03d.ngrok.io
                                            os.system("/usr/local/ngrok http -config=/root/.ngrok2/ngrok.yml 80 &")  ## https://c5eba03d.ngrok.io
                                            os.system("/usr/local/ngrok https -config=/root/.ngrok2/ngrok.yml 443 &")  ## https://c5eba03d.ngrok.io

                                        else:
                                        
                                           
                                            print("@ ngrok curl @:")
                                            # print(len(datajson['tunnels']))
                                            curl= datajson['tunnels'][0]['public_url']
                                         
                                            if POPO!=80:
                                                curl+=":"+str(POPO)
                                                print("@ A curl @:",curl)
                                            if curl.startswith("http"):
                                                # print("@@@",curl)
                                                print("@ B curl @:",curl)
                                                import os
                                                os.system(f'git config --global Ngrok.py "{curl}" ')
                                                # raise SystemExit
                                                ############# 無效果
                                                # os._exit(0)
                                                cls.curl=curl
                                                
                                                ###
                                                # 要停止正在运行的程序，请使用CTRL + C终止该过程。
                                                # 要在python中以编程方式处理它，请导入sys模块，并在要终止程序的位置使用sys.exit()。
                                                # import sys
                                                # sys.exit()
                                                
                                                # break 
                                                ccx()

                                            #     os.system(f'git config --global Ngrok.py "{curl}" ')
                                            #     # print(os.popen("git config --global Ngrok.py").read() )  
                                            #     # return curl 

                                            # if  os.popen("git config --global Ngrok.py").read().startswith("http"):
                                            #     print(os.popen("git config --global Ngrok.py").read())
                                            # else:
                                            #     print("@@@空")
                                            #     # break 
                                                

                                except Exception:
                                    print("@ Exception @")       
                                    import os
                                    if not os.popen("curl -s http://localhost:4040/api/tunnels").read().find('{"tunnels":[],"uri":"/api/tunnels"}')!=-1:
                                      os.system("killall ngrok")
                
                                    # import os,time
                                    import os
                                    # os.system('ngrok authtoken '+ID+' && ngrok http '+str(POPO)+'&')  ## https://c5eba03d.ngrok.io
                            
                                    # time.sleep(3)
                            return cls.curl

                    import os
                    if __name__=="__main__":
                        QQ()
                    # # print(QQ())

                    # os.system(f'git config --global Ngrok.py "{QQ()}" ')  
                    # os._exit(0)
                    
                           

        

                        
                
                import site
                atexit.register(cleanup_function,site)
                #################################
                
            

    

            



    ################################################
    # with open("/content/QQ/README.md", "r") as fh:
    with open("README.md", "r") as fh:
              long_description = fh.read()


    ##############
    import site,os
    siteD =  os.path.dirname(site.__file__)
    # +os.sep+"siteR.py"
    print("@siteD: ",siteD)
    #### setup.py ################################
    from setuptools import setup, find_packages
    setup(
          name  =   f"{Var.nameA}"  ,
          version=  f"{Var.nameB}"  ,
          description="My CMD 模組",

          
          #long_description=long_description,
          long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
          long_description_content_type="text/markdown",
          # author="moon-start",
          # author_email="login0516mp4@gmail.com",
          # url="https://gitlab.com/moon-start/cmd.py",
          license="LGPL",
          ####################### 宣告目錄 #### 使用 __init__.py
          ## 1 ################################################ 
          # packages=find_packages(include=['cmds','cmds.*']),


          ###
          ### %mkdir -p /content/cmd.py/Ngrok
          packages=find_packages(include=[f'{sdist.dir}',f'{sdist.dir}.*']),    
          ## 2 ###############################################
        
          # ],
          ################################
          cmdclass={
                'install': PostCMD
                # 'develop':  PostCMD
          }
          #########################
    )
   

### B版
# 6-13