# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:54:32 2023

@author: jorge aragão
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
import csv


class PrincipalRAD:
    def __init__(self, win):
        #components
        self.lblNome=tk.Label(win, text='Student Name:')
        self.lblNota1=tk.Label(win, text='Grade 1')
        self.lblNota2=tk.Label(win, text='Grade 2')
        self.lblMedia=tk.Label(win, text='Average')
        self.txtNome=tk.Entry(bd=3)
        self.txtNota1=tk.Entry()
        self.txtNota2=tk.Entry()        
        self.btnCalcular=tk.Button(win, text='Calculate Average', command=self.fCalcularMedia)        
        #----- TreeView --------------------------------------------
        self.dadosColunas = ("Student", "Grade1", "Grade2", "Average", "Situation")            
        
        
        self.treeMedias = ttk.Treeview(win, 
                                       columns=self.dadosColunas,
                                       selectmode='browse')
        
        self.verscrlbar = ttk.Scrollbar(win,
                                        orient="vertical",
                                        command=self.treeMedias.yview)
        
        self.verscrlbar.pack(side ='right', fill ='x')
                
        
        
        self.treeMedias.configure(yscrollcommand=self.verscrlbar.set)
        
        self.treeMedias.heading("Student", text="Student")
        self.treeMedias.heading("Grade1", text="Grade 1")
        self.treeMedias.heading("Grade2", text="Grade 2")
        self.treeMedias.heading("Average", text="Average")
        self.treeMedias.heading("Situation", text="Situation")
        

        self.treeMedias.column("Student",minwidth=0,width=100)
        self.treeMedias.column("Grade1",minwidth=0,width=100)
        self.treeMedias.column("Grade2",minwidth=0,width=100)
        self.treeMedias.column("Average",minwidth=0,width=100)
        self.treeMedias.column("Situation",minwidth=0,width=100)

        self.treeMedias.pack(padx=10, pady=10)
                
        #---------------------------------------------------------------------        
        # positioning of components in the window
        #---------------------------------------------------------------------        
        self.lblNome.place(x=100, y=50)
        self.txtNome.place(x=200, y=50)
        
        self.lblNota1.place(x=100, y=100)
        self.txtNota1.place(x=200, y=100)
        
        self.lblNota2.place(x=100, y=150)
        self.txtNota2.place(x=200, y=150)
               
        self.btnCalcular.place(x=100, y=200)
           
        self.treeMedias.place(x=100, y=300)
        self.verscrlbar.place(x=805, y=300, height=225)
        
        
        self.id = 0
        self.iid = 0
        
        self.carregarDadosIniciais()

#-----------------------------------------------------------------------------
    def carregarDadosIniciais(self):
        try:
          fsave = 'planilhaAlunos.csv'
          dados = pd.read_csv(fsave)
          print("************ data available ***********")        
          print(dados)
        
          u=dados.count()
          print('u:'+str(u))
          nn=len(dados['Student'])          
          for i in range(nn):                        
            nome = dados['Student'][i]
            nota1 = str(dados['Grade1'][i])
            nota2 = str(dados['Grade2'][i])
            media=str(dados['Average'][i])
            situacao=dados['Situation'][i]
                        
            self.treeMedias.insert('', 'end',
                                   iid=self.iid,                                   
                                   values=(nome,
                                           nota1,
                                           nota2,
                                           media,
                                           situacao))
            
            
            self.iid = self.iid + 1
            self.id = self.id + 1
        except:
          print('There is no data to load yet')
            
#-----------------------------------------------------------------------------
#Save data to an excel spreadsheet
#-----------------------------------------------------------------------------           
    def fSalvarDados(self):
      try:          
        fsave = 'planilhaAlunos.csv'
        dados=[]
        
        
        for line in self.treeMedias.get_children():
          lstDados=[]
          for value in self.treeMedias.item(line)['values']:
              lstDados.append(value)
              
          dados.append(lstDados)
          
        df = pd.DataFrame(data=dados,columns=self.dadosColunas)
        
        df.to_csv(fsave, index=False)                
        
        print('Saved data')
      except:
       print('Unable to save data')   
        
        
#-----------------------------------------------------------------------------
#calculates the average and checks the student's situation
#-----------------------------------------------------------------------------          
    def fVerificarSituacao(self,nota1, nota2):
          media=round((nota1+nota2)/2, 2)
          if(media>=7.0):
             situacao = 'Approved'
          elif(media>=5.0):
              situacao = 'In Recovery'
          else:   
             situacao = 'Disapproved'
         
          return media, situacao
        
#-----------------------------------------------------------------------------
#Print student data
#-----------------------------------------------------------------------------          
    def fCalcularMedia(self):
        try:
          nome = self.txtNome.get()
          nota1=float(self.txtNota1.get())
          nota2=float(self.txtNota2.get())
          media, situacao = self.fVerificarSituacao(nota1, nota2)
          media = round(media, 2)
                    
          
          self.treeMedias.insert('', 'end', 
                                 iid=self.iid,                                  
                                 values=(nome, 
                                         str(nota1),
                                         str(nota2),
                                         str(media),
                                         situacao))
          
          
          self.iid = self.iid + 1
          self.id = self.id + 1
          
          self.fSalvarDados()
        except ValueError:
          print('Input valid values!')        
        finally:
          self.txtNome.delete(0, 'end')
          self.txtNota1.delete(0, 'end')
          self.txtNota2.delete(0, 'end')

#-----------------------------------------------------------------------------
#Programa Principal
#-----------------------------------------------------------------------------          

janela=tk.Tk()
principal=PrincipalRAD(janela)
janela.title('Welcome to StudentSys')
janela.geometry("820x600+10+10")
janela.mainloop()