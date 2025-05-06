from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from PIL import Image,ImageTk
import mysql.connector as sql
from tkinter import messagebox
from datetime import date
from time import strftime


db=sql.connect(host='localhost',user='root',passwd='')
cursor=db.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS BILLING_SOFTWARE')
cursor.execute('use billing_software')
cursor.execute('create table if not exists mg(mg_id int,name varchar(20),password varchar(20),dob char(10))')
cursor.execute('create table if not exists product_details(item_id int primary key auto_increment,item_name varchar(20),price float)')
cursor.execute('create table if not exists customer_details(cust_id int primary key auto_increment,cust_name varchar(20),cust_phone bigint)')
cursor.execute('create table if not exists bill(bill_id int,cust_id int,item_id int,qty int,bill_date date,amount float)')

q=0
def phcheck(ph):
        t=True
        while t:
            if ph.isdigit():
                x=str(ph)
                l=['6','7','8','9']
                if len(x)==10 and x[0] in l:
                    t=False
                    global q
                    q=1
                    
                else:
                    #messagebox.showerror('Phone Number','Phone Number is Invalid')
                    t=False
            else:
                #messagebox.showerror('Phone Number','Phone Number is Invalid')
                t=False



    
def bill_win():
        mgr.destroy()
        def newcuswin():
                def newcussub():
                        if nlen.get()=='' or plen.get()=='':
                                messagebox.showwarning('FIELD','EMPTY FIELDS ARE NOT ALLOWED')
                        elif nlen.get().isalpha() and plen.get().isdigit():
                                phcheck(plen.get())
                                if q==1:
                                        cursor.execute('insert into customer_details (cust_name,cust_phone) values (%s,%s)',(nlen.get(),plen.get()))
                                        db.commit()
                                        newcus.destroy()
                                else:
                                        messagebox.showerror('PH_NO','INVALID PHONE NUMBER')
                        else:
                                messagebox.showerror('INVALID','INVALID DATA')
                        
                
                newcus=Tk()
                newcus.geometry('600x400')
                newcus.resizable(True,True)
                newcus.title('NEW CUSTOMER')
                newcus.attributes('-fullscreen',True)
                o=Label(newcus,text='CUSTOMER DETAILS',font=('stencil',25,'bold'),fg='red',pady=30,bg='#76b5c5')
                o.pack(fill=X)
                nl=Label(newcus,text='CUSTOMER NAME  :',font=('arial',15),padx=10,pady=8)
                nl.place(x=50,y=160)
                pl=Label(newcus,text='PHONE NUMBER  :',font=('arial',15),padx=10,pady=8)
                pl.place(x=65,y=220)
                nlen=Entry(newcus,width=15,font=('arial',14,'bold'))
                nlen.place(x=280,y=168)
                plen=Entry(newcus,width=15,font=('arial',14,'bold'))
                plen.place(x=280,y=228)
                subbtn=Button(newcus,text='SUBMIT',bg='green',fg='white',activeforeground='black',activebackground='white',padx=20,pady=5,command=newcussub)
                subbtn.place(x=240,y=290)
        billwin=Tk()
        billwin.title('BILLING')
        billwin.state('zoomed')
        billwin.attributes('-fullscreen',True)
        l=Label(billwin,text='XYZ SUPERMARKET',font=('stencil',25,'bold'),fg='red',pady=50,bg='#76b5c5')
        l.pack(fill=X)
        pidl=Label(billwin,text='P_ID     :',font=('arial',15),padx=10,pady=8)
        pidl.place(x=230,y=250)
        qtyl=Label(billwin,text='QTY     :',font=('arial',15),padx=10,pady=8)
        qtyl.place(x=231,y=320)
        global netamount
        netamount=0
        def updttrv():
                global netamount
                cursor.execute('select * from product_details')
                vl=cursor.fetchall()
                if pidbill.get()=='' or qtybill.get()=='':
                        messagebox.showerror('FIELD','EMPTY FIELDS ARE NOT ALLOWED')
                elif pidbill.get().isalpha() or qtybill.get().isalpha():
                        messagebox.showerror('INVALID','INVALID DATA')
                elif (qtybill.get())==str(0):
                        messagebox.showerror('INVALID','QTY CANT"T BE ZERO')
                else:
                        cursor.execute('select * from product_Details where item_id=%s',(pidbill.get(),))
                        vl=cursor.fetchall()
                        if vl==[]:
                                messagebox.showerror('INVALID','P_ID NOT FOUND IN THE DATABASE')
                        else:
                                iname,mrp=vl[0][1],vl[0][2]
                                amount=mrp*int(qtybill.get())
                                netamount+=amount
                                rowv=(pidbill.get(),iname,mrp,qtybill.get(),amount)
                                billtrv.insert('',END,values=rowv)
                                ntamt()
        
        
        def ntamt():
                        ntam.config(text=netamount)
                        
        
        def get_valuebill(event):
                curs=billtrv.focus()
                item=billtrv.item(curs)
                row=item['values']
                pidt.set(row[0])
                
        def get_valuepro(event):
                curs=probilltrv.focus()
                item=probilltrv.item(curs)
                row=item['values']
                pidt.set(row[0])
        pidt=IntVar()
        pidbill=Entry(billwin,width=10,font=('arial',14,'bold'),textvariable=pidt)
        pidbill.place(x=350,y=259)
        pidbill.delete(0,END)
        qtybill=Entry(billwin,width=10,font=('arial',14,'bold'))
        qtybill.place(x=350,y=329)
        global searchicon

        searchicon=Image.open('./images/searchicon.png')
        searchicon=searchicon.resize((22,22))
        searchicon=ImageTk.PhotoImage(searchicon)
        searchiconbtn=Button(billwin,image=searchicon,bd=3,relief='groove')
        searchiconbtn.place(x=500,y=260)
        #product treeview
        global probilltrv
        th=ttk.Style()
        th.theme_use('clam')
        th.configure('Treeview.Heading',background='green3')
        cols=('P_ID','P_NAME','PRICE')
        probilltrv=ttk.Treeview(billwin,columns=cols,show='headings')
        probilltrv.heading('P_ID',text='P_ID')
        probilltrv.heading('P_NAME',text='P_NAME')
        probilltrv.heading('PRICE',text='PRICE')
        probilltrv.column('P_ID',width=80)
        probilltrv.column('PRICE',width=80)
        probilltrv.place(x=800,y=200)
        probilltrv.bind('<Double-Button-1>',get_valuepro)
        cursor.execute('select * from product_Details')
        dt=cursor.fetchall()
        for i in dt:
                 probilltrv.insert('',END,values=i)
        probillbar=ttk.Scrollbar(billwin,orient=VERTICAL,command=probilltrv.yview)
        probilltrv.configure(yscrollcommand=probillbar.set)
        probillbar.place(x=1164,y=200,height=229)

        qtyaddbtn=Button(billwin,text='ADD',bg='green',fg='white',activeforeground='black',activebackground='white',padx=5,pady=3,command=updttrv)
        qtyaddbtn.place(x=496,y=329)

        th=ttk.Style()
        th.theme_use('clam')
        th.configure('Treeview.Heading',background='green3')
        cols=('P_ID','P_NAME','MRP','QTY','AMOUNT')
        global billtrv
        billtrv=ttk.Treeview(billwin,columns=cols,show='headings')
        billtrv.heading('P_ID',text='P_ID')
        billtrv.heading('P_NAME',text='P_NAME')
        billtrv.heading('MRP',text='MRP')
        billtrv.heading('QTY',text='QTY')
        billtrv.heading('AMOUNT',text='AMOUNT')
        billtrv.column('P_ID',width=80)
        billtrv.column('QTY',width=80)
        billtrv.column('MRP',width=80)
        #billtrv.bind('<Double-Button-1>',get_valuebill)
        billtrv.place(x=140,y=450)
        billbar=ttk.Scrollbar(billwin,orient=VERTICAL,command=billtrv.yview)
        billtrv.configure(yscrollcommand=billbar.set)
        billbar.place(x=785,y=450,height=229)

        ntamtl=Label(billwin,text='NET AMOUNT  =',font=('arial',15),padx=10,pady=8)
        ntamtl.place(x=880,y=520)
        
        ntam=Label(billwin,text='0',fg='red',font=('stencil',25,'bold'),padx=10)
        ntam.place(x=1090,y=520)

        def billtrvcheck():
                blst=[]
                for child in billtrv.get_children():
                        blst=billtrv.item(child)['values']
                if blst==[]:
                        messagebox.showerror('','error')
                else:
                        genbill()
                        
        def billsql():
                
                def last_bill_no():
                    cursor.execute('select max(bill_id) from bill')
                    record = cursor.fetchone()
                    return record
                bill_no = last_bill_no()
                if bill_no[0]==None:
                   bill_no =1
                else:
                   bill_no = bill_no[0]+1
                today = date.today()
                if cen.get()=='':
                        messagebox.showwarning('FIELD','EMPTY FIELDS ARE NOT ALLOWED')
                elif cen.get().isdigit():
                        cursor.execute('select * from customer_details where cust_phone=%s',(int(cen.get()),))
                        j=cursor.fetchall()
                        if j==[]:
                                messagebox.showerror('NOT FOUND','ID NOT FOUND IN THE DATABASE')
                        else:
                                ci=j[0][0]
                                for child in billtrv.get_children():
                                        billlist=billtrv.item(child)['values']
                                        
                                        sql=('insert into bill values (%s,%s,%s,%s,%s,%s)')
                                        val=(bill_no,ci,billlist[0],billlist[3],today,billlist[4])
                                        cursor.execute(sql,val)
                                db.commit()
                                gb.destroy()
                                for i in billtrv.get_children():
                                        billtrv.delete(i)
                                pidbill.delete(0,END)
                                qtybill.delete(0,END)
                                ntam.config(text='0')
                                
                                
                else:
                        messagebox.showerror('INVALID','INVALID DATA')

        def genbill():

                def custinput():
                        if cen.get()=='':
                                messagebox.showwarning('INVALID','EMPTY FIELDS ARE NOT ALLOWED')
                        elif cen.get().isdigit():
                                
                                cidg=int(cen.get())
                                cursor.execute('select * from customer_details where cust_phone=%s',(cidg,))
                                det=cursor.fetchall()
                                if det==[]:
                                        messagebox.showinfo('INFO','CUST_PH.NO NOT FOUND IN THE DATABASE')
                                else:
                                        cn=det[0][1]
                                        cntext.set(cn)
                                
                        else:
                                messagebox.showerror("INVALID",'INVALID PHONE NUMBER')

                global cen
                global gb
                gb=Toplevel()
                gb.geometry('600x600')
                gb.resizable(True,True)
                gb.title('GENERATE BILL')
                gb.attributes('-fullscreen',True)
                cid=Label(gb,text='CUSTOMER_PH.NO  :',font=('arial',15),padx=10,pady=8)
                cid.place(x=30,y=100)
                cntext=StringVar()
                cphtext=StringVar()
                cen=Entry(gb,width=15,font=('arial',14,'bold'))
                cen.place(x=280,y=107)
                global cuss
                cuss=Image.open('./images/searchicon.png')
                cuss=cuss.resize((21,21))
                cuss=ImageTk.PhotoImage(cuss)
                sbtn=Button(gb,image=cuss,bd=5,relief='groove',command=custinput)
                sbtn.place(x=458,y=106)
                cnamel=Label(gb,text='CUSTOMER_NAME  :',font=('arial',15),padx=10,pady=8)
                cnamel.place(x=32,y=180)
                cnameen=Entry(gb,width=12,font=('arial',14,'bold'),state='readonly',textvariable=cntext)
                cnameen.place(x=280,y=190)
                sqlbtn=Button(gb,text='SUBMIT',bg='green',fg='white',activeforeground='black',activebackground='white',padx=20,pady=5,command=billsql)
                sqlbtn.place(x=250,y=350)
                newcusbtn=Button(gb,text='NEW CUSTOMER',fg='red',font=(10),command=newcuswin)
                newcusbtn.place(x=230,y=430)
                                        
                
        
        genbillbtn=Button(billwin,text='GENERATE BILL',bg='green',fg='white',activeforeground='black',activebackground='white',font=(8),padx=10,pady=3,command=billtrvcheck)
        genbillbtn.place(x=980,y=600)

        def billback_():
                billwin.destroy()
                mgrwin()
                

        global billbackimg
        billback=Image.open('./images/backarrowicon.png')
        billback=billback.resize((35,30))
        billbackimg=ImageTk.PhotoImage(billback)
        billbackbtn=Button(billwin,image=billbackimg,borderwidth=0,cursor='hand2',command=billback_)
        billbackbtn.place(x=30,y=100)        




def custinfo():
        mgr.destroy()
        def clear_all():
                for item in custrv.get_children():
                        custrv.delete(item)
        def phtreecust():
                
                if phonen.get().isdigit() and len(phonen.get())==10:
                        cursor.execute('select * from customer_details where cust_phone=%s',(phonen.get(),))
                        dt=cursor.fetchall()
                        phonen.delete(0,END)
                        if dt==[]:
                                messagebox.showerror('NOT FOUNT','PHONE NO NOT FOUND IN THE DATABASE')
                        else:
                                clear_all()
                                for i in dt:
                                        custrv.insert('',END,values=i)
                elif phonen.get()=='':
                        messagebox.showwarning('FIELD','EMPTY FIELDS ARE NOT ALLOWED')
                else:
                        messagebox.showerror('INVALID','INVALID PHONE NUMBER')
                        
        def treecust():
                
                if custid.get().isdigit():
                        custidd=int(custid.get())
                        custid.delete(0,END)
                        cursor.execute('select * from customer_details where cust_id=%s',(custidd,))
                        dt=cursor.fetchall()
                        if dt==[]:
                                messagebox.showerror('NOT FOUND','ID NOT FOUND IN THE DATABSE')
                        else:
                                def clear_all():
                                        for item in custrv.get_children():
                                                custrv.delete(item)
                                clear_all()
                                for i in dt:
                                        custrv.insert('',END,values=i)
                                
                                                
                elif custid.get()=='':
                         messagebox.showwarning('EMPTY FIELD','EMPTY FIELDS ARE NOT ALLOWED')
                else:
                        messagebox.showerror('INVALID','INVALID ID')
                         
        global cust1
        global backimg
        cus=Tk()
        cus.state('zoomed')
        cus.title('CUSTOMER INFO')
        cus.attributes('-fullscreen',True)
        idl=Label(cus,text='CUSTOMER ID     :',font=('arial',12,'bold'))
        idl.place(x=100,y=250) 
        global custid
        custid=Entry(cus,font=('arial',15,'bold'),width=15)
        custid.place(x=270,y=250)
        cust=Image.open('./images/searchicon.png')
        custr=cust.resize((25,25))
        cust1=ImageTk.PhotoImage(custr)
        idsearchbtn=Button(cus,image=cust1,command=treecust,cursor='hand2')
        idsearchbtn.place(x=480,y=250)
        phonel=Label(cus,text='PHONE_NO     :',font=('arial',12,'bold'))
        phonel.place(x=122,y=320)
        phonen=Entry(cus,font=('arial',15,'bold'),width=15)
        phonen.place(x=270,y=320)
        phsearchbtn=Button(cus,image=cust1,command=phtreecust,cursor='hand2')
        phsearchbtn.place(x=480,y=320)

        def destroy():
                cus.destroy()
                mgrwin()
       
        l=Label(cus,text='XYZ SUPERMARKET',font=('stencil',25,'bold'),fg='red',pady=80,bg='#76b5c5')
        l.pack(fill=X)
        back=Image.open('./images/backarrowicon.png')
        back=back.resize((35,30))
        backimg=ImageTk.PhotoImage(back)
        backbtn=Button(cus,image=backimg,command=destroy,borderwidth=0,cursor='hand2')
        backbtn.place(x=30,y=100)

        def cusclear():
                custid2.delete(0,END)
                phoneen2.delete(0,END)
                nameen2.delete(0,END)
        def cusupdt():
                if custid2.get()=='' or phoneen2.get()=='':
                        messagebox.showerror('FIELD','EMPTY FIELDS ARE NOT ALLOWED')
                elif custtext.get()==0 or phonetext==0:
                        messagebox.showerror('FIELD','EMPTY FIELDS ARE NOT ALLOWED')
                else:
                        a=custid2.get()
                        c=phoneen2.get()
                        x=str(c)
                        l=['6','7','8','9']
                        if len(x)==10 and x[0] in l:
                                cursor.execute('update customer_details set cust_phone=%s where cust_id=%s',(c,a))
                                db.commit()
                                cus.after(1000,showtrv)
                                custid2.delete(0,END)
                                phoneen2.delete(0,END)
                                nameen2.delete(0,END)                                    
                        else:
                            messagebox.showerror('PH_NO','INVALID PHONE NUMBER')


        

        #global custtext
        global phonetext
        custtext=IntVar()
        nametext=StringVar()
        phonetext=IntVar()
        ul=Label(cus,text='UPDATE PHONE NO',font=('arial',18,'bold'),bg='red')
        ul.place(x=920,y=205)
        id2=Label(cus,text='CUSTOMER ID     :',font=('arial',12,'bold'))
        id2.place(x=850,y=260) 
        custid2=Entry(cus,font=('arial',15,'bold'),width=15,textvariable=custtext,state='readonly')
        custid2.place(x=1020,y=260)
        namel2=Label(cus,text='CUSTOMER NAME     :',font=('arial',12,'bold'))
        namel2.place(x=818,y=320)
        phonel2=Label(cus,text='PHONE_NO     :',font=('arial',12,'bold'))
        phonel2.place(x=870,y=380)
        nameen2=Entry(cus,font=('arial',15,'bold'),width=15,textvariable=nametext,state='readonly')
        nameen2.place(x=1020,y=320)
        phoneen2=Entry(cus,font=('arial',15,'bold'),width=15,textvariable=phonetext)
        phoneen2.place(x=1020,y=380)


        clearbtn=Button(cus,text='CLEAR',bg='orange',fg='white',font='bold',bd=5,relief='groove',padx=10,command=cusclear)
        clearbtn.place(x=880,y=450)
        editbtn=Button(cus,text='UPDATE',bg='green',fg='white',font='bold',bd=4,relief='groove',command=cusupdt)
        editbtn.place(x=1220,y=379)

        
        def getvalue(event):
                curs=custrv.focus()
                item=custrv.item(curs)
                row=item['values']
                custtext.set(row[0])
                nametext.set(row[1])
                phonetext.set(row[2])


        def showtrv():
                custid.delete(0,END)
                phonen.delete(0,END)
                global custrv
                th=ttk.Style()
                th.theme_use('clam')
                th.configure('Treeview.Heading',background='green3')
                cols=('CUST_ID','CUST_NAME','PH_NO')
                custrv=ttk.Treeview(cus,columns=cols,show='headings')
                custrv.heading('CUST_ID',text='CUST_ID')
                custrv.heading('CUST_NAME',text='CUST_NAME')
                custrv.heading('PH_NO',text='PH_NO')
                custrv.column('CUST_ID',width=80)
                custrv.place(x=55,y=473)
                custrv.bind('<Double-Button-1>',getvalue)
                cursor.execute('select * from customer_Details')
                dt=cursor.fetchall()
                for i in dt:
                        custrv.insert('',END,values=i)
                cvbar=ttk.Scrollbar(cus,orient=VERTICAL,command=custrv.yview)
                custrv.configure(yscrollcommand=cvbar.set)
                cvbar.place(x=540,y=473,height=228)
        shal=Button(cus,text='SHOW ALL RECORDS',bg='#e28743',font='bold',bd=5,relief='groove',padx=15,command=showtrv)
        shal.place(x=230,y=422)
        showtrv()

        
#product window
def product_info():
        mgr.destroy()
        def progetvalue(event):
                 curs=trv.focus()
                 row=trv.item(curs)
                 val=row['values']
                 dbi.set(val[0])
                 pnen.set(val[1])
                 pren.set(val[2])      
        def editbtn():
                
                def updb():
                        if pidenn.get()=='' or priceen.get()=='':
                                messagebox.showwarning('WARNING','ALL FIELDS ARE REQUIRED')
                        elif pren.get()==0:
                                messagebox.showwarning('INVALID','PRICE CAN"T BE ZERO')
                        elif priceen.get().isdigit() :
                                pid=pidenn.get()
                                pr=priceen.get()
                                sql=('update product_details set price =%s where item_id=%s')
                                val=(pr,pid)
                                cursor.execute(sql,val)
                                db.commit()
                                trv.destroy()
                                pidenn.delete(0,END)
                                pnameen.delete(0,END)
                                priceen.delete(0,END)
                                pro.after(1000,protrv(55,360,540,360,228))
                        else:
                                messagebox.showerror('INVALID','INVALID DATA')
                
                def progetvalue():
                        curs=trv.focus()
                        row=trv.items(curs)
                        val=row['values']
                        dbi.set(val[0])
                        pnen.set(val[1])
                        pren.set(val[2])
                        
                def editdestroy():
                        pro.destroy()
                        prowin()

                def prodelete():
                        if pidenn.get()=='':
                                messagebox.showwarning('WARNING','ALL FIELDS ARE REQUIRED')
                        else:
                                def ask():
                                        ask=messagebox.askquestion('DELETE','DO YOU WANT TO DELETE')
                                        if ask=='yes':
                                                cursor.execute('delete from product_details where item_id=%s',(pidenn.get(),))
                                                pidenn.delete(0,END)
                                                pnameen.delete(0,END)
                                                priceen.delete(0,END)
                                                pro.after(1000,protrv(55,360,540,360,228))
                                                
                                ask()                                
                                        
                                
                proframe.destroy()
                trv.place(x=55,y=360)
                vbar.place(x=540,y=360,height=228)
                global proeditbackimg
                
                proeditback=Image.open('./images/backarrowicon.png')
                proeditback=proeditback.resize((35,30))
                proeditbackimg=ImageTk.PhotoImage(proeditback)
                editbackbtn=Button(pro,image=proeditbackimg,command=editdestroy,cursor='hand2')
                editbackbtn.place(x=30,y=100)

                el=Label(pro,text='EDIT DETAILS',font=('arial',18,'bold'),bg='red')
                el.place(x=920,y=215)
                pid=Label(pro,text='PRODUCT_ID     :',font=('arial',15,'bold'))
                pid.place(x=833,y=300)
                pname=Label(pro,text='PRODUCT NAME     :',font=('arial',15,'bold'))
                pname.place(x=800,y=370)
                price=Label(pro,text='PRICE     :',font=('arial',15,'bold'))
                price.place(x=902,y=440)
                global pnen
                global pren
                global dbi
                global pidenn
                global priceen
                dbi=StringVar()
                pnen=StringVar()
                pren=IntVar()
                pidenn=Entry(pro,font=('arial',15,'bold'),width=15,textvariable=dbi,state='readonly')
                pidenn.place(x=1040,y=302)
                pnameen=Entry(pro,font=('arial',15,'bold'),width=15,textvariable=pnen,state='readonly')
                pnameen.place(x=1040,y=372)
                priceen=Entry(pro,font=('arial',15,'bold'),width=15,textvariable=pren)
                priceen.place(x=1040,y=442)

                updbtn=Button(pro,text='UPDATE',bg='green',fg='white',font='bold',bd=4,relief='groove',command=updb)
                updbtn.place(x=960,y=570)
                delbtn=Button(pro,text='DELETE',bg='red',fg='white',font='bold',bd=4,relief='groove',command=prodelete)
                delbtn.place(x=1070,y=570)
                

                
        
        def addbtn():
                mbackbtn.destroy()
                proframe.destroy()
                trv.destroy()
                vbar.destroy()
                
                
                def addprodb():
                        if pen.get()=='' or pren.get()=='':
                                messagebox.showerror('EMPTY FIELD','EMPTY FIELDS ARE NOT ALLOWED')
                        elif pren.get()==0 :
                                messagebox.showerror('EMPTY FIELD','PRICE CAN''T BE ZERO')
                        else:
                                sql='insert into product_details (item_name,price) values (%s,%s)'
                                val=(pen.get(),pren.get())
                                cursor.execute(sql,val)
                                db.commit()
                                messagebox.showinfo("UPLOADED","Data successfully added")
                                pen.delete(0,END)
                                priceen.delete(0,END)
                                
                def probackc():
                        pro.destroy()

                        prowin()
                global proaddbackimg      
                
                proaddback=Image.open('./images/backarrowicon.png')
                proaddback=proaddback.resize((35,30))
                proaddbackimg=ImageTk.PhotoImage(proaddback)
                addbackbtn=Button(pro,image=proaddbackimg,command=probackc,cursor='hand2')
                addbackbtn.place(x=30,y=100)
                l=Label(pro,text='ADD NEW PRODUCT',font=('stencil',25,'bold'),fg='green3')
                l.pack()
                pname=Label(pro,text='PRODUCT NAME',font=('arial',15),padx=10,pady=8)
                pname.place(x=420,y=350)
                price=Label(pro,text='PRICE',font=('arial',15),padx=10,pady=8)
                price.place(x=515,y=400)
                penen=StringVar()
                pen=Entry(pro,font=('arial',15,'bold'),textvariable=penen)
                pen.place(x=650,y=356)
                pren=IntVar()
                priceen=Entry(pro,font=('arial',13,'bold'),width=10,textvariable=pren)
                priceen.place(x=650,y=406)

                subbtn=Button(pro,text='SUBMIT',bg='orange',font='bold',bd=5,relief='groove',padx=15,command=addprodb,cursor='hand2')
                subbtn.place(x=595,y=540)
        def prowin():
                
                global pro
                global prowbackimg

                pro=Tk()
                pro.title('PRODUCT INFO')
                pro.state('zoomed')
                pro.attributes('-fullscreen',True)
                l=Label(pro,text='XYZ SUPERMARKET',font=('stencil',25,'bold'),fg='red',pady=80,bg='#76b5c5')
                l.pack(fill=X)
                def prodestroy():
                        pro.destroy()
                        mgrwin()
                global proframe
                global mbackbtn
                proframe=LabelFrame(pro,bg='#eab676',highlightbackground='black',highlightthickness=2,pady=90,padx=30)
                proframe.place(x=40,y=300)
                addpbtn=Button(proframe,text='ADD PRODUCT',bg='orange',font='bold',bd=5,relief='groove',command=addbtn)
                addpbtn.grid(row=0,column=0)
                editpbtn=Button(proframe,text='EDIT DETAILS',bg='#a34523',font='bold',bd=5,relief='groove',command=editbtn)
                editpbtn.grid(row=1,column=0,pady=15)
                prowback=Image.open('./images/backarrowicon.png')
                prowback=prowback.resize((35,30))
                prowbackimg=ImageTk.PhotoImage(prowback)
                mbackbtn=Button(pro,image=prowbackimg,command=prodestroy,cursor='hand2')
                mbackbtn.place(x=30,y=100)
                global protrv
                def protrv(m,n,o,p,q):
                        global trv
                        global vbar
                        th=ttk.Style()
                        th.theme_use('clam')
                        th.configure('Treeview.Heading',background='green3')
                        cols=('P_ID','P_NAME','PRICE')
                        trv=ttk.Treeview(pro,columns=cols,show='headings')
                        trv.heading('P_ID',text='P_ID')
                        trv.heading('P_NAME',text='P_NAME')
                        trv.heading('PRICE',text='PRICE')
                        trv.column('P_ID',width=80)
                        trv.place(x=m,y=n)
                        trv.bind('<Double-Button-1>',progetvalue)
                        cursor.execute('select * from product_Details')
                        dt=cursor.fetchall()
                        for i in dt:
                                trv.insert('',END,values=i)
                        vbar=ttk.Scrollbar(pro,orient=VERTICAL,command=trv.yview)
                        trv.configure(yscrollcommand=vbar.set)
                        vbar.place(x=o,y=p,height=q)
                protrv(430,365,913,365,228)
        prowin()
def reportwin():
        mgr.destroy()
        def reportfetch():
                cursor.execute('select sum(amount) from bill where bill_date between %s and %s',(fromdt.get(),todt.get()))
                amount=cursor.fetchall()
                amountl.config(text=amount)
        
        report=Tk()
        report.title('REPORT MENU')
        report.state('zoomed')
        report.attributes('-fullscreen',True)
        l=Label(report,text='XYZ SUPERMARKET',font=('stencil',25,'bold'),fg='red',pady=80,bg='#76b5c5')
        l.pack(fill=X)
        amtl=Label(report,text='AMOUNT COLLECTED',font=('stencil',25,'bold'),fg='red')
        amtl.place(x=490,y=250)
        froml=Label(report,text='FROM',font=('arial',15,'bold'),fg='blue')
        froml.place(x=365,y=350)
        tol=Label(report,text='TO',font=('arial',15,'bold'),fg='blue')
        tol.place(x=770,y=350)
        fromdt=Entry(report,font=('arial',14,'bold'),width=15)
        fromdt.place(x=330,y=390)
        todt=Entry(report,font=('arial',14,'bold'),width=15)
        todt.place(x=700,y=390)
        subbtn=Button(report,text='SUBMIT',bg='green',fg='white',font='bold',bd=4,relief='groove',command=reportfetch)
        subbtn.place(x=570,y=440)
        amtcl=Label(report,text='AMOUNT COLLECTED     :',font=('stencil',25,'bold'),fg='red')
        amtcl.place(x=230,y=550)
        global amountl
        amountl=Label(report,text='0',fg='red',font=('stencil',22,'bold'),padx=10)
        amountl.place(x=700,y=553)
        def reportdes():
                report.destroy()
                mgrwin()
        global rebackimg
        reback=Image.open('./images/backarrowicon.png')
        reback=reback.resize((35,30))
        rebackimg=ImageTk.PhotoImage(reback)
        rebackbtn=Button(report,image=rebackimg,command=reportdes,cursor='hand2')
        rebackbtn.place(x=30,y=100)

    
#manager window               
def mgrwin():

    def logout():
            o=messagebox.askquestion('LOGOUT','Are you sure to Logout',icon='question')
            if o=='yes':
                    mgr.destroy()
                    #window.mainloop()
    global mgr
    global logimgr
    mgr=Tk()
    mgr.title('MANAGER')
    mgr.state('zoomed')
    mgr.attributes('-fullscreen',True)
    #textt='logined by',mgname
    l=Label(mgr,text='XYZ SUPERMARKET',font=('stencil',25,'bold'),fg='red',pady=80,bg='#76b5c5')
    l.pack(fill=X)
    #lg=Label(mgr,text=textt,font=('arial',15),fg='red')
    #lg.place(x=600,y=130)
    logimg=Image.open('./images/LOGOUT.jpg')
    logimg=logimg.resize((40,45))
    logimgr=ImageTk.PhotoImage(logimg)
    logout=Button(mgr,image=logimgr,command=logout)
    logout.place(x=1310,y=210)
    #time frame
    def time():
        t=strftime('%I:%M:%S %p')
        tt.config(text=t)
        tt.after(1000,time)
    tt=Label(mgr,fg='red',font=('stencil',25,'bold'),padx=10)
    tt.pack(anchor='center')
    time()
    def destroyframe():
            optframe.destroy()

    #mgr option frame
    optframe=LabelFrame(mgr,text='Options Menu',bg='light green',highlightbackground='black',highlightthickness=2,pady=20,padx=120)
    optframe.place(x=100,y=300)
    
    custimg=Image.open('./images/customericon.jpg')
    custimg=custimg.resize((60,55))
    custimg=ImageTk.PhotoImage(custimg)
    custbtn=Button(optframe,image=custimg,command=custinfo,cursor='hand2')
    custbtn.grid(row=0,column=0,pady=15)
    custl=Label(optframe,text='CUSTOMER INFO',font=('times',15,'bold'))
    custl.grid(row=2,column=0)


    proimg=Image.open('./images/product icon.png')
    proimg=proimg.resize((60,55))
    proimg=ImageTk.PhotoImage(proimg)
    probtn=Button(optframe,image=proimg,command=product_info,cursor='hand2')
    probtn.grid(row=0,column=1,pady=15)
    productl=Label(optframe,text='PRODUCT DETAILS',font=('times',15,'bold'))
    productl.grid(row=2,column=1,padx=150)

    reportimg=Image.open('./images/reporticon.png')
    reportimg=reportimg.resize((60,55))
    reportimg=ImageTk.PhotoImage(reportimg)
    reportbtn=Button(optframe,image=reportimg,cursor='hand2',command=reportwin)
    reportbtn.grid(row=0,column=2,pady=15)
    reportl=Label(optframe,text='REPORT',font=('times',15,'bold'))
    reportl.grid(row=2,column=2,padx=20)

    bill=Image.open('./images/billicon.png')
    bill=bill.resize((60,55))
    billimg=ImageTk.PhotoImage(bill)
    billbtn=Button(optframe,image=billimg,font=('times',15,'bold'),command=bill_win,cursor='hand2')
    billbtn.grid(row=5,column=0,pady=15)
    billlabel=Label(optframe,text='BILL',font=('times',15,'bold'))
    billlabel.grid(row=6,column=0)


    mgr.mainloop()

def passtest1(p):
    v=0
    lc,uc,d,ss=0,0,0,0
    for i in p:
        if i.islower():
            lc+=1
        if i.isupper():
            uc+=1
        if i.isdigit():
            d+=1
        if i in ['@','#','*','_']:
            ss+=1

    if lc>=1 and uc>=1 and d>=1 and ss>=1:
        sql='update mg set password=%s where mg_id=%s'
        val=(newpas.get(),mgid)
        cursor.execute(sql,val)
        db.commit()
        messagebox.showinfo('OK','Passoword updated successfully')
        c.destroy()
        
    else:
        messagebox.showerror('Password','Password must ensure the condition')


def mgupdate():
        if newpas.get()=='':
                e=messagebox.showerror('Empty Field','Empty Fields are not allowed')
        else:
                passtest1(newpas.get())

def changepassmg():
        s=0
        global mgid
        cursor.execute('select * from mg')
        g=cursor.fetchall()
        if mgid.get()=='' or mgd.get()=='':
                messagebox.showerror('Error','All Fields are required')
        elif mgid.get().isdigit():
                
                mgid=int(mgid.get())
                for i in range(len(g)):
                        if mgid==g[i][0] and mgd.get()==g[i][-1]:
                                s+=1
                        else:
                                pass
                
                if s==1:
                        global c
                        mgf.destroy()
                        c=Tk()
                        c.title("NEW PASSWORD")
                        c.geometry('500x300')
                        l=Label(c,text='Enter your new Password',font=('arial',12,'bold'))
                        l.place(x=170,y=50)
                        l1=Label(c,text='PASSWORD MUST ENSURE THE CONDITION\n(ONE LC,ONE UC,ONE DIGIT,ONE SPECIAL SYMBOL)\n MINIMUM SIZE: 6',font=('arial',8),fg='red')
                        l1.place(x=140,y=140)
                        global newpas
                        newpas=Entry(c,font=('times',15,'bold'))
                        newpas.place(x=160,y=100)  
                        btn=Button(c,text='SUBMIT',padx=8,pady=4,bg='green',fg='black',command=mgupdate)
                        btn.place(x=220,y=200)

                else:
                        messagebox.showerror('DOB','Invalid DOB')
                
        else:
                messagebox.showerror('Error','Invalid ID')

def mgforgot():
        global mgf
        mgf=Tk()
        mgf.title('FORGOT PASSWORD')
        mgf.geometry('500x300')
        mgf.resizable(False,False)
        i=Label(mgf,text='Enter your ID:',font=('arial',12,'bold'))
        i.place(x=180,y=50)
        l=Label(mgf,text='Enter your DOB in the given format\ndd/mm/yyyy',font=('arial',12,'bold'))
        l.place(x=130,y=138)
        global mgid
        global mgd
        mgid=Entry(mgf,font=('times',15,'bold'))
        mgid.place(x=160,y=90)
        mgd=Entry(mgf,font=('times',15,'bold'))
        mgd.place(x=160,y=190)
        btn=Button(mgf,text='SUBMIT',padx=8,pady=4,bg='green',fg='black',command=changepassmg)
        btn.place(x=220,y=250)
        mgf.mainloop()



def mglogin():
        
    def checksubmit():
        if useren.get()=='':
            messagebox.showerror('Field','All Fields Are Required')
        
        elif useren.get().isdigit():
            submitfunc()
            pass
        else:
            messagebox.showerror("ID ERROR",'Invalid ID')

                
    def submitfunc():
            if passen.get()=='':
                messagebox.showerror("Error" , "All Fields Are Required")
            else:
                cursor.execute('select * from mg')
                a=cursor.fetchall()
    
                for i in range(len(a)):
                    if a[i][0]==int(useren.get()) and a[i][2]==str(passen.get()):
                        global mgname
                        mgname=a[i][1]
                        mglogin.destroy()
                        mgrwin()
                        
                        break
                else:
                        messagebox.showwarning('warning','User ID or Password is incorrect')

        
    #window.destroy()    
    mglogin=Tk()
    mglogin.state('zoomed')
    mglogin.attributes('-fullscreen',True)
    cname=Label(mglogin,text='XYZ SUPERMARKET',font=('algerian',30,'bold'),padx=20,pady=100,bg='blue')
    cname.pack(fill=X)
    t=Label(mglogin,text='LOGIN',font=('stencil',25,'bold'),fg='black',pady=10,padx=20)
    t.pack()
    
    userl=Label(mglogin,text='ID',font=('arial',15),padx=10,pady=8)
    userl.place(x=495,y=380)

    passl=Label(mglogin,text='PASSWORD',font=('arial',15),padx=10,pady=8)
    passl.place(x=400,y=450)

    useren=Entry(mglogin,font=('times',15,'bold'))
    useren.place(x=580,y=384)

    passen=Entry(mglogin,font=('times',15,'bold'),show='*')
    passen.place(x=580,y=454)

    subbtn=Button(mglogin,text='LOGIN',bg='green',activeforeground='black',padx=20,pady=10,command=checksubmit)
    subbtn.place(x=550,y=550)

    forgot=Button(mglogin,text='Forgot Password',fg='red',font=7,command=mgforgot)
    forgot.place(x=700,y=550)
    mglogin.mainloop()

mglogin()
