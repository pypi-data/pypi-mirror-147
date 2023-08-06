'''
Author: BDFD
Date: 2022-03-01 17:28:34
LastEditTime: 2022-04-20 12:27:07
LastEditors: BDFD
Description: 
FilePath: \5.2-PyPi-WES_Calculation\WES_Calculation\greenampt.py
'''

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
import numpy as np
from numpy import *
import statistics
import io
import base64

# Effective Rainfall Generation   
# # Primary Inputs (required)
# # thetar = float(request.form["thetar"]) # Residual soil moisture content (It can be assumed to be zero, if no actual value is avaiulable.)
# thetai = float(request.form["thetai"] )# Initial soil moisture content
# thetas = float(request.form["thetas"] )# Soil moisture content at saturation (i.e. porosity)
# Psi = float(request.form["psi"]) # Suction head (m)
# K = float(request.form["k"]) # Saturated hydraulic conductivity (cm/h)
# tol = 0.00001
# toln= 0.00001
# dti= float(request.form["dti"]) #6 time interval in the analysis, normally that used in hyetograph (min)
# nin= int(request.form["nin"])# The number of time intervals to be considered in the anlysis
# iyesno = int(request.form["iyesno"]) # Whether to generate an effective hyetograph (0: No; 1: Yes)
# # test1 = request.form["thetar"]
# test2 = request.form["thetai"]
# test3 = request.form["thetas"]
# test4 = request.form["psi"]
# test5 = request.form["k"]
# # test6 = request.form["tol"]
# test7 = request.form["dti"]
# test8 = request.form["nin"]
# test9 = None
# test10 = None
# yesono = request.form["iyesno"]
# if iyesno == 1:
#     test9 = request.form["dd"]
#     test10 = request.form["i"]
#     dd = float(request.form["dd"])# Depression depth used in generating an effective hyetograph (mm), which has to be zero when iyesno=0.
#     result = request.form["i"] # Hyetograph (mm/h) (The first value covers the period between time 0 and time 0+dti.)
#     res = result.split(",")
#     i = list(map(float, res))
#     #if sum(i)*dti/60<dd: # (20121226)
#         #print('说明：') # (20121226)
#         #print('1. 降雨量不足以蓄满地表的坑洼，故没有净雨产生，也不会有下渗产生。') # (20121226)
#         #sys.exit(0) # (20121226)
    
# if iyesno==0:
#     i=[0 for k in range(nin)]# Hyetograph (mm/h) (The first value covers the period between time 0 and time 0+dti.)
#     dd=0                


def greenampt(thetai, thetas, Psi, K, dti, nin, dd, i):
    tol = 0.00001
    toln= 0.00001   
    Tpu=10000 # an imaginary ponding time when i = 0 (min)
    nini=len(i)
    if nin>nini:
        i=np.concatenate((i,[0 for k in range(nin-nini)])) # Extend i with zero intensities 

    fpo=[0 for k in range(len(i)+2)] # Theoretical potential infiltration rate (m/h)
    fpu=[0 for k in range(len(i)+1)] # Updated potential infiltration rate (m/h)
    f=[0 for k in range(len(i)+1)] # Actual infiltration rate (m/h)
    Fpo=[0 for k in range(len(i)+2)] # Theoretical potential infiltration quantity (m)
    F=[0 for k in range(len(i)+1)] # Actual infiltration quantity (m)
    
    dtheta=thetas-thetai
    if dtheta==0: # (20211227)  
        ddtheta=dtheta+tol # a dummy dtheta to be used as denominator when dtheta = 0 (20211227)  
        fpo[0]=K/100 # (20211227)  
        fpu[0]=fpo[0] # (20211227)  
    else:
        ddtheta=dtheta # simply dtheta to be used as denominator when dtheta is not equal to 0 (20211227) 
        fpo[0]='Inf' # (20211227)  
        fpu[0]='Inf' # (20211227)  
            
    #fpo[0]='Inf'
    #fpu[0]='Inf'

    # 1. Hyetograph

    t1=np.linspace(0,dti*(len(i)-1),len(i))
    ie=[0 for k in range(len(i))] # Effective hyetograph (mm/h)

    fig,ax1 = plt.subplots()
    if max(i)>0:
        #ax1.bar(t1,i,width=dti,label="Hyetograph",color="lightblue",align='edge')
        ax1.bar(t1,i,width=dti,label=u"降雨强度过程",color="lightblue",align='edge')

    #ax1.set_xlabel("Time (min)")
    ax1.set_xlabel(u"时间 (minutes)")
    ax1.set_ylabel("Rates (mm/h)") 
    #ax1.set_ylabel("数值 (mm/h)") 

    # 2. Depression Storage
    j=0
    Td=0 # The time to meet the depression depth (min)

    if dd>0:
        dda=0 # An assumed depression depth (mm)
        
        while dda<dd:
            if j==0:
                #ax1.bar(t1[j],i[j],width=dti,label="Depression Rate",color="darkgrey",hatch='/',align='edge',alpha=1)
                ax1.bar(t1[j],i[j],width=dti,label="地表坑洼的充填速率",color="darkgrey",hatch='/',align='edge',alpha=1)
            else:
                ax1.bar(t1[j],i[j],width=dti,color="darkgrey",hatch='/',align='edge',alpha=1)
    
            if dtheta==0: # (20211227)  
                fpo[j]=K/100 # (20211227)  
                fpu[j]=fpo[0] # (20211227)  
            else:
                fpo[j]='Inf' # (20211227)  
                fpu[j]='Inf' # (20211227)  

            Fpo[j]=0
            ie[j]=0
            dda=dda+i[j]*dti/60 # Updated dda (mm)
            j=j+1
        
        Td=dti*j-60*(dda-dd)/i[j-1] # Updated Td (min) (revised on 20211226)
        
        ax1.bar(Td,i[j-1],width=60*(dda-dd)/i[j-1],color="lightblue",align='edge')
        ax1.axvline(Td,ls="--",color="black",linewidth=0.5)
        extraticks=[Td]
        plt.xticks(list(plt.xticks()[0]) + extraticks)

        if dda>dd:
            j=j-1 # Index will return to the beginning of the terminal period of the depression when Td is not at a time node
                # Otherwise, Index will stay at the time node when dd is met
        #else:
            #fpo[j]='inf'
            #fpu[j]='inf'#

    # 3. Infiltration  

    # 3.1 During the time interval where the depression terminates  

    Fa=K*0.01*(dti*(j+1)-Td)/60 # An assumed value for F (m)
    Fc=K*0.01*(dti*(j+1)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # An iterated value for F (m) (revised on 20121226)

    while (abs(Fa-Fc)>tol):
        Fa=0.5*(Fa+Fc) # Updated Fa in iteration (m)
        Fc=K*0.01*(dti*(j+1)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # Updated Fc in iteration (m) (revised on 20121226)
    
    Fpo[j+1]=Fc
    fpo[j+1]=K*0.01*(1+Psi*dtheta/Fc)

    f[j]=(dtheta>0)*i[j]/1000+(dtheta==0)*K/100 #20211226  
    # Under the unbsaturated condition, since the initial infiltration rate is infinite, the first rainfall intensity is used as the actual infiltration rate.
    # Under the saturated condition, the actual infiltration rate simply equals the saturated hydraulic conductivity.
    # This f[j] is intended for the time node at Td, which may be later than the time node corresponding to j.
    F[j]=0#f[j-1]*(dti*j-Td)/60

    if i[j]>0:
        Tp=60*(K*10*Psi*1000*dtheta/(i[j]-K*10)-1000*F[j])/i[j] # Ponding time (min)
    else:
        Tp=Tpu
    
    if Tp>=(dti*(j+1)-Td):
        F[j+1]=f[j]*(dti*(j+1)-Td)/60
        if F[j+1]>0:
            fpu[j+1]=K*0.01*(1+Psi*dtheta/F[j+1])
        else:
            fpu[j+1]=fpo[j+1]
            
    else:
        FTt=f[j]*Tp/60
        timertt=60*(FTt-Psi*dtheta*np.log(1+FTt/Psi/ddtheta))/K/0.01 # equivalent spent time to reach the turning point since the infiltration beginning (revised on 20121226)
        Fc=K*0.01*(timertt+dti-Tp)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # An iterated value for F (m)(revised on 20121226)
        while (abs(Fa-Fc)>tol):
            Fa=0.5*(Fa+Fc) # Updated Fa in iteration (m)
            Fc=K*0.01*(timertt+dti-Tp)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # Updated Fc in iteration (m)(revised on 20121226)
        F[j+1]=Fc    #?
        ietx,iety=[Td+Tp,dti*(j+1),dti*(j+1),Td+Tp],[i[j],i[j]-2*(dti*(j+1)-Td)*(i[j]-1000*60*(F[j+1]-F[j])/(dti*(j+1)-Td))/(dti*(j+1)-Td-Tp),i[j],i[j]]#A triangle for net rainfall (2022.03.10)
        plt.fill(ietx,iety,color="lightblue",linewidth=0.5,zorder=3)#2022.03.10   

        if F[j+1]>0:
            fpu[j+1]=K*0.01*(1+Psi*dtheta/F[j+1])
        else:
            fpu[j+1]=fpo[j+1]
    
    tin=60*(F[j+1]-Psi*dtheta*np.log(1+F[j+1]/Psi/ddtheta))/K/0.01 # a timer for subsequent infiltration calculation (min) (revised on 20121226)

    #ie[j]=i[j]-1000*f[j]
    ie[j]=i[j]-1000*60*(F[j+1]-F[j])/(dti*(j+1)-Td) 
    if abs(ie[j])<toln: # 2022.03.10
        ie[j]=0 # 2022.03.10

    if max(i)>0:
        #ax1.bar(Td,1000*f[j],width=(dti*(1+j)-Td),label="Actual Infiltration Rate",color="sandybrown",align='edge',alpha=.5)
        ax1.bar(Td,1000*f[j],width=(dti*(1+j)-Td),label="实际入渗率",color="sandybrown",align='edge',alpha=.5)
    data=()
    if dd==0:
        data+=((str(j*dti),str(round(ie[j],2))),)
    else:
        data+=(('0','0'),)
        if dda>dd:   
            data+=((str(round(Td,1)),str(round(ie[j],2))),)
        else:  
            data+=((str(j*dti),str(round(ie[j],2))),)
    
    # 3.2 During every following time interval
    
    for l in range(j+1,len(i)):
            
        f[l]=min(fpu[l],i[l]/1000)
            
        Fc=K*0.01*(dti*(l+1)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)      
        while (abs(Fa-Fc)>tol):
            Fa=0.5*(Fa+Fc)
            Fc=K*0.01*(dti*(l+1)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226) 
        fc=K*0.01*(1+Psi*dtheta/Fc)
        Fpo[l+1]=Fc
        fpo[l+1]=fc #m/h
        
        tin=tin+dti
        
        if fpu[l]<=i[l]/1000:##???
            Fc=K*0.01*tin/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)
            while (abs(Fa-Fc)>tol):
                Fa=0.5*(Fa+Fc)
                Fc=K*0.01*tin/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)
            fc=K*0.01*(1+Psi*dtheta/Fc)    
            F[l+1]=Fc
            fpu[l+1]=fc
            
        else: 
    
            if i[l]>0:
                Tp=60*(K*10*Psi*1000*dtheta/(i[l]-K*10)-1000*F[l])/i[l]
            else:
                Tp=Tpu
        
            if Tp>=dti:
                F[l+1]=i[l]*dti/60/1000+F[l]
                
            else: # this part addresses the scenario where a rainfall intensity goes across the infiltration potential curve 
                
                FTt=i[l]*Tp/60/1000+F[l]
                timertt=60*(FTt-Psi*dtheta*np.log(1+FTt/Psi/ddtheta))/K/0.01 # equivalent spent time to reach the turning point since the infiltration beginning #(revised on 20121226)
                Fc=K*0.01*(timertt+dti-Tp)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # An iterated value for F (m) #(revised on 20121226)
                while (abs(Fa-Fc)>tol):
                    Fa=0.5*(Fa+Fc) # Updated Fa in iteration (m)
                    Fc=K*0.01*(timertt+dti-Tp)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)
                F[l+1]=Fc  
                ietx,iety=[dti*l+Tp,dti*(l+1),dti*(l+1),dti*l+Tp],[i[l],i[l]-2*dti*(i[l]-1000*60*(F[l+1]-F[l])/dti)/(dti-Tp),i[l],i[l]]#A triangle for net rainfall (2022.03.10)
                plt.fill(ietx,iety,color="lightblue",linewidth=0.5,zorder=3)#2022.03.10         

            if F[l+1]>0:
                fpu[l+1]=K*0.01*(1+Psi*dtheta/F[l+1])
            else:
                fpu[l+1]=fpo[l+1]
    
            tin=60*(F[l+1]-Psi*dtheta*np.log(1+F[l+1]/Psi/ddtheta))/K/0.01 # Uptated tin #(revised on 20121226)
    
        #ie[l]=i[l]-1000*f[l]
        ie[l]=i[l]-1000*60*(F[l+1]-F[l])/dti
        if abs(ie[l])<toln: # 2022.03.10
            ie[l]=0 # 2022.03.10

        if max(i)>0:
            ax1.bar(t1[l],1000*f[l],width=dti,color="sandybrown",align='edge',alpha=.5)
        data += ((str(l*dti),str(round(ie[l],2))),)
        
    # Plotting

    Fc=K*0.01*(dti*(l+2)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)     
    while (abs(Fa-Fc)>tol):
        Fa=0.5*(Fa+Fc)
        Fc=K*0.01*(dti*(l+2)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)
    fc=K*0.01*(1+Psi*dtheta/Fc)
    Fpo[l+2]=Fc
    fpo[l+2]=fc  

    #ax1.plot(np.linspace(t1[j+1],dti*(l+1),l-j+1),1000*np.array(fpo[j+1:l+2]),label="Theoretical Infiltration Potential",ls="--",color="green",linewidth=1)
    ax1.plot(np.linspace(t1[j+1],dti*(l+1),l-j+1),1000*np.array(fpo[j+1:l+2]),label="理论入渗率",ls="--",color="green",linewidth=1)
    if max(i)>0:
        #ax1.plot(np.linspace(t1[j+1],dti*(l+1),l-j+1),1000*np.array(fpu[j+1:l+2]),label="Updated Infiltration Potential",color="red",linewidth=1)
        ax1.plot(np.linspace(t1[j+1],dti*(l+1),l-j+1),1000*np.array(fpu[j+1:l+2]),label="修正后的理论入渗率",color="red",linewidth=1)
    if dtheta==0: # (20211227)  
        ax1.hlines(1000*fpo[j],Td,t1[j+1],ls="--",color="green",linewidth=1) # (20211227)  
        if max(i)>0:# (20211227)  
            ax1.hlines(1000*fpu[j],Td,t1[j+1],color="red",linewidth=1)# (20211227)        
    
    plt.xlim(0,dti*len(i))
    ax1.legend()
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams["font.family"]="sans-serif"
    #plt.rcParams['axes.unicode_minus'] = False
    #mpl.rcParams['axes.unicode_minus'] = False
    #matplotlib.rc('font', family='FangSong')
    #mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei'] 
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    interval = str(dti)
    sminute = str(round(Td,1))
    eminute = str((j+1)*dti)
    #eff = "---Effective Rainfall Generated by Green-Ampt Infiltration Method---"
    eff = "---按Green-Ampt下渗模型生成的净雨过程---"
    #str1 = "2. Unless noted otherwise, an intensity lasts for a full time interval (= "+interval+" minutues), starting from the corresponding time moment."
    str1 = "2. 除非特殊说明，一个降雨强度值从对应的时刻开始，会持续整个时间步长 (= "+interval+" minutes)。"
    #note = ["Notes:","1. The lightblue portion in the figure shows the effective rainfall.",str1]
    note = ["说明:","1. 为与降雨强度过程相比较，下渗率按柱状图表示，某时刻的下渗率会显示在接下来的整个时间步长内。",str1]
    if dtheta==0:
        note2 = ["说明:","1. 理论入渗率等于土体的渗透系数。"]
    else:     
        #note2 = ["Notes:","1. The theoretical infiltration potential is infinite at time zero."]
        note2 = ["说明:","1. 在时间零点处理论入渗率为无限大。"]
        #note2 = ["说明:","1. 在时间零点处理论入渗率为无限大。","2.????"]

    if Td>0:
        #str2 = "3. The depression storage is completely filled at the "+ sminute +"th minute, and no effective rainfall has occurred prior to the moment"
        str2 = "3. 地表坑洼在第 "+ sminute +" minutes 被蓄满, 之前没有净雨产生。"
        if dtheta==0: # (20211227) 
            str4 = "4. 下渗在第 "+ sminute +" minutes 开始。"# (20211227) 
        else:# (20211227) 
            str4 = "4. 下渗在第 "+ sminute +" minutes 开始，理论入渗率和修正后的理论入渗率在这一时刻均为无限大。"
        note.append(str2)
        note.append(str4)
        if dda>dd:
            #str3 = " 4. If applicable, the intensity starting at the "+sminute+"th minute ends at the "+eminute+"th minute."
            str3 = " 5. 起始于第 "+sminute+" minutes 的净雨强度值在第 "+eminute+" minutes 结束。"
            note.append(str3)
    return plot_url,data,eff,note,note2
