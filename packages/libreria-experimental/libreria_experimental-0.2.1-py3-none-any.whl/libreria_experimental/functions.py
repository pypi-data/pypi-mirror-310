from sympy import *
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean, pstdev
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from numpy import e
import math as math
def ajuste_linear(x,y,errorx=0,errory=0,xlabel='',ylabel='',titulo=''):
    n=len(x)
    xm=np.mean(x)
    ym=np.mean(y)
    sx=np.sum(x)
    sy=np.sum(y)
    sxy=np.sum(x*y)
    sx2=np.sum(x**2)
    sy2=np.sum(y**2)
    m=(n*sxy-sx*sy)/(n*sx2-sx**2)
    b=(sx2*sy-sx*sxy)/(n*sx2-sx**2)
    xi=symbols('xi')
    f=b+m*xi
    fx=lambdify(xi,f)
    fi=fx(x)
    numerador=n*sxy-sx*sy
    raiz1=np.sqrt(n*sx2-sx**2)
    raiz2=np.sqrt(n*sy2-sy**2)
    r=numerador/(raiz1*raiz2)
    r2=r**2
    r2_porcentaje=np.around(r2*100,2)
    sigma=(sum((y-m*x-b)**2)/(len(x)-2))**(1/2)
    errorm=(((len(x)*sigma**2)/(len(x)*sum(x**2)-(sum(x))**2)))**(1/2)
    errorn=((sigma**2*sum(x**2))/(len(x)*sum(x**2)-(sum(x))**2))**(1/2)
    m1='m='+str(m)+'+/-'+str(errorm)
    b1='n='+str(b)+'+/-'+str(errorn)
    plt.plot(x,y,'o',label='Datos')
    plt.plot(x,fi,color='orange',label='Ajuste')
    plt.errorbar(x,y,color="black",yerr=errory,fmt='.')
    plt.errorbar(x,y,color="black",xerr=errorx,fmt='.')
    for i in range(0,n,1):
        y0=np.min([y[i],fi[i]])
        y1=np.max([y[i],fi[i]])
        plt.vlines(x[i],y0,y1, color='red',
            linestyle ='dotted')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.show
    f1='f='+str(f)
    r21='r^2='+str(r2)
    return f1,m1,b1,r21
def ajuste_magico(x,y,parametros,xerror=0,yerror=0,xlabel='',ylabel='',titulo=''):
    popt,pcov=curve_fit(funcion,x,y)
    x_ajuste=np.linspace(1,10,1000)
    plt.figure()
    plt.plot(x,y,'o',label='Datos')
    plt.plot(x_ajuste,funcion(x_ajuste,*popt),'r-',label='Ajuste')
    plt.errorbar(x,y,color="black",yerr=yerror,fmt='.')
    plt.errorbar(x,y,color="black",xerr=xerror,fmt='.')
    plt.legend(loc='best')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.tight_layout()
    pstd=np.sqrt(np.diag(pcov))
    nombres_de_param=parametros
    print('Parámetros:')
    for i, param in enumerate(popt):
        print('{:s}={:5.3f}+-{:5.3f}'.format(nombres_de_param[i],param,pstd[i]/2))
def properrores(variables,f,errores,valores1):
    ecuacion=0
    errorindirecto1=[]
    listav=eval(variables)
    valores=valores1.T
    for i in range(len(listav)):
        ecuacion+=abs(diff(f,listav[i]))*errores[i]
    for j in range(len(valores)):
        errorindirecto2=ecuacion.subs(dict(zip(listav,valores[j])))
        errorindirecto1.append(errorindirecto2)
    return np.array(errorindirecto1)

