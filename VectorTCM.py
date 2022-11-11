# %%
from collections import Counter
import copy as cp
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import font as tkFont
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import font_manager
import matplotlib as mpl
from regex import R
from sklearn import decomposition as dcp
mpl.use("TkAgg")
from matplotlib import backends as mpb
btk = mpb.backend_tkagg
import seaborn as sns
import altair as alt

import os
import pandas as pd
import numpy as np
import gensim
import sys
sys.setrecursionlimit(1000000)

font = font_manager.FontProperties(fname='simhei.ttf',size=10)
parameters = {'xtick.labelsize': 17,
              'ytick.labelsize': 17,
              'font.family':'SimHei',
              'axes.unicode_minus':False}
plt.rcParams.update(parameters)
plt.style.use('ggplot')
#--------------------------------------------------------------
# %%
# UI界面
root = tk.Tk()
root.title("Vector-TCM")
root.geometry("1200x800")
root.resizable(True, True)
root.configure(bg='#aed0ee')
root.iconbitmap("i.ico")
# 缺省值
fontsty = tkFont.Font(family='Arial', size=14, weight=tkFont.BOLD,slant='roman')
fonttip  = tkFont.Font(family='Arial', size=12, weight=tkFont.NORMAL,slant='roman')
fontsmall  = tkFont.Font(family='Arial', size=9, weight=tkFont.NORMAL,slant='roman')
fontresult = tkFont.Font(family='Arial', size=12, weight=tkFont.BOLD,slant='roman')
fontplot = font_manager.FontProperties(fname='simhei.ttf')
fontplotsize = 14
button_width = 12
long_button_width = 50
entry_width = 70

button_height = 1
framecolor='#f6f9e4'

# 数据与字符串容器
df = pd.DataFrame()
data = pd.DataFrame()
filename = tk.StringVar()
filepath = tk.StringVar()
class openfile:
    def __init__(self):
        self.path = filedialog.askopenfilename(title='选择Excel文件', filetypes=[('Excel', '*.xlsx')])
        filename.set(self.path)
        filepath.set('File path: ' + self.path)
        if filename !='':
            global df
            df = pd.read_excel(filename.get())
            global data
            data = pd.DataFrame(df)  
            label_load.configure(text='Please load the selected file')
        else:
            pass
def clear_data():
    global data
    global filename
    global filepath
    global opted_list
    global list_box1
    global list_box2
    global listToBeSelected
    global tab4_button3
    global tab4_button4
    global tab4_savepath1
    global tab4_savepath2
    global pres_df
    global herb_df
    global tab5_button3
    global tab5_button4
    global tab5_savepath1
    global tab5_savepath2
    global ldia_pres_df
    global ldia_herb_df
    global toolbar1
    global toolbar2
    global toolbar3
    global toolbar4
    global toolbar5
    
    filename = tk.StringVar()
    filepath = tk.StringVar()
    data = pd.DataFrame()
    list_box1.delete(0, 'end')
    list_box2.delete(0, 'end')
    opted_list=[]
    listToBeSelected=[]
    label_load.configure(text='Please select a file to open')
    Label1.configure(textvariable=filepath)
    tab3_table1.delete(*tab3_table1.get_children())
    try:
        canvas1.get_tk_widget().place_forget()
        canvas1.get_tk_widget().destroy()
    except:
        pass
    try:
        canvas2.get_tk_widget().place_forget()
        canvas2.get_tk_widget().destroy()
    except:
        pass
    try:
        canvas3.get_tk_widget().place_forget()
        canvas3.get_tk_widget().destroy()
    except:
        pass
    try:
        canvas4.get_tk_widget().place_forget()
        canvas4.get_tk_widget().destroy()
    except:
        pass
    try:
        canvas5.get_tk_widget().place_forget()
        canvas5.get_tk_widget().destroy()
    except:
        pass
    try:
        tab4_button3.destroy()
    except:
        pass
    try:
        tab4_button4.destroy()
    except:
        pass
    tab4_savepath1.set('')
    tab4_savepath2.set('')
    pres_df = pd.DataFrame()
    herb_df = pd.DataFrame()
    try:
        tab5_button3.destroy()
    except:
        pass
    try:
        tab5_button4.destroy()
    except:
        pass
    tab5_savepath1.set('')
    tab5_savepath2.set('')
    ldia_pres_df = pd.DataFrame()
    ldia_herb_df = pd.DataFrame()
    try:
        toolbar1.destroy()
    except:
        pass
    try:
        toolbar2.destroy()
    except:
        pass
    try:
        toolbar3.destroy()
    except:
        pass
    try:
        toolbar4.destroy()
    except:
        pass
    try:
        toolbar5.destroy()
    except:
        pass
    
    
    
    
    
    
button1=tk.Button(root,text="Open file",command=lambda:openfile(),width=button_width, )
button1.place(x=17,y=39)
Label1 = tk.Label(root, textvariable=filepath, font=fontsty,bg='#aed0ee')
Label1.place(x=300,y=10)

button3 = tk.Button(root, text='All Clear', command=lambda:clear_data(), width=button_width)
button3.place(x=1060,y=7)

button2=tk.Button(root,text="Start load",command=lambda:StartExecution.excute(),width=button_width, )
button2.place(x=17,y=79)




class download_exmplr:
    def exmp():
        Exmp = pd.read_excel('English example.xlsx')
        path = tk.StringVar()
        savepath = filedialog.asksaveasfilename(title='Save as', initialfile='English example.xlsx', filetypes=[('Excel', '*.xlsx')])
        path.set(savepath)
        #Exmp.to_excel(path.get()+'.xlsx', index=False)
        Exmp.to_excel(path.get(), index=False)
    def cxmp():
        Cxmp = pd.read_excel('Chinese example.xlsx')
        path = tk.StringVar()
        savepath = filedialog.asksaveasfilename(title='Save as', initialfile='Chinese example.xlsx', filetypes=[('Excel', '*.xlsx')])
        path.set(savepath)
        #Cxmp.to_excel(path.get()+'.xlsx', index=False)
        Cxmp.to_excel(path.get(), index=False)

button4 = tk.Button(root, text='Example data', command=lambda:download_exmplr.exmp(), width=button_width)
button4.place(x=17,y=179)

button5 = tk.Button(root, text='示例数据', command=lambda:download_exmplr.cxmp(), width=button_width)
button5.place(x=17,y=219)





# 读取数据与预处理
herb_list = []
file_dict = dict()
list_vect = []
class PreProcessing:
    def data_pre():
        global data
        col = data.columns
        data = data.set_index(col[0])
        global herb_list
        global file_dict
        global list_vect
        # herb_list
        sentence = ""
        for index, row in data.iterrows():
            for sen in row:
                sentence = sentence + sen + ','
        herb_list = sentence.split(sep=',')
    
        # feil_dict
        file_dict = dict()
        for index, row in data.iterrows():
            for sen in row:
                per_vect = []
                ws = sen.split(sep=',')
                for herb in ws:
                    per_vect.append(herb)
                file_dict[index] = per_vect
        
        # list_vect
        list_vect = []
        for index, row in data.iterrows():
            for sen in row:
                sen_row = []
                sent = sen.split(sep=',')
                ','.join(sent)
                for herb in sent:
                    sen_row.append(herb)
                list_vect.append(sen_row)
        
process1 = ttk.Progressbar(root, length=100, mode='indeterminate',value=0, max=100)
process1.place(x=13,y=119)
label_load = tk.Label(root, text='Please select a file to open', font=fontsty,bg='#aed0ee')
label_load.place(x=17,y=10)

class StartExecution(PreProcessing):
    global data
    def excute():
        if filename.get() !='':
            process1.step(50)
            process1.update()
            process1.start('idle')
            PreProcessing.data_pre()
            displayIndex()
            label_load.configure(text='File loaded successfully')
            process1.stop()
        else:
            tk.Messagebox.showinfo(title='Warning', message='Please select a file to open')
    
    

    
# tab1------------------------------------------------------------------------
MultiGroupTab=ttk.Notebook(root)
tab1 = tk.Frame(bg=framecolor,relief='ridge',borderwidth=2)
ta1_button4 = tk.Button(tab1,text="Descriptive statistical results",command=lambda:DescriptiveStatistics.herb_count(),width=long_button_width, )
ta1_button4.pack(side='top', anchor='nw',padx=5, pady=5)
Illustrate1 = tk.Label(tab1, text='1.The total number of different herbs:____', font=fontsty,bg=framecolor)
Illustrate1.pack(side='top', anchor='nw',padx=5, pady=5)
Illustrate2 = tk.Label(tab1, text='2.The total number of herbs:____', font=fontsty,bg=framecolor)
Illustrate2.pack(side='top', anchor='nw',padx=5, pady=5)
Illustrate3 = tk.Label(tab1, text='3.The average number of herbs in each prescription:____', font=fontsty,bg=framecolor)
Illustrate3.pack(side='top', anchor='nw',padx=5, pady=5)
Illustrate4 = tk.Label(tab1, text='4.The most common herb', font=fontsty,bg=framecolor)
Illustrate4.pack(side='top', anchor='nw',padx=5, pady=5)
Illustrate5 = tk.Label(tab1, text='How many herbs do you need to display by frequency?', font=fonttip,bg=framecolor)
Illustrate5.pack(side='top', anchor='nw',padx=5, pady=5)


#  位置需要调整
SpinBar = tk.Spinbox(tab1, from_=0, to=20, width=button_width,increment=5,bg=framecolor)
SpinBar.pack(side='top', anchor='nw',padx=5, pady=5,after=Illustrate5)


# 描述性统计类

class DescriptiveStatistics: 
    def herb_count():
        global herb_list
        total_herb_list = len(Counter(herb_list))
        Illustrate1.config(text='1.The total number of different herbs: {}'.format(total_herb_list))
        
        total_herb_word_list = len(herb_list)
        Illustrate2.config(text='2.The total number of herbs: {}'.format(total_herb_word_list))
        
        global file_dict
        len_herb_list = 0
        for index in file_dict.keys():
            local_herb_list = file_dict.get(index)
            local_herb_list = list(set(local_herb_list))
            len_list = len(local_herb_list)
            len_herb_list = len_herb_list + len_list
        avg_len = len_herb_list / (len(file_dict.keys()))
        Illustrate3.config(text='3.The average number of herbs in each prescription: {}'.format(round(avg_len, 0)))
    def most_common_herb():  
        global herb_list
        global most_common_herb1
        Counter_every_herb = Counter(herb_list)
        most_common_herb2 = Counter_every_herb.most_common(int(SpinBar.get()))
        most_common_herb1 = pd.DataFrame(most_common_herb2, columns=['herb', 'count'])
        fig1, ax1 = plt.subplots()
        x = most_common_herb1['herb']
        y = most_common_herb1['count']
        y = list(y)
        y.reverse()  # 倒序
        ax1.barh(x, y, align='center', color='dodgerblue', tick_label=list(x))
        ax1.margins(y=.01, x=.01)
        ax1.ignore_existing_data_limits = True
        ax1.autoscale_view(tight=False, scalex=False, scaley=True)
        for a,b in zip(x,y):
            plt.text(b+0.1,a,b,ha = 'center',va = 'center',fontsize=14)
            plt.ylabel('herbs', fontsize=fontplotsize, fontproperties=fontplot)
            plt.yticks(x,fontsize=fontplotsize,fontproperties=fontplot)
        global canvas1
        canvas1 = btk.FigureCanvasTkAgg(fig1, master=tab1)  # A tk.DrawingArea.
        canvas1.draw()
        global toolbar1
        toolbar1 = btk.NavigationToolbar2Tk(canvas1, root)
        toolbar1.update()
        canvas1.get_tk_widget().pack(side='bottom', anchor='s',padx=0, pady=30,fill='both',expand=True)
        
    def forget_plot():
        global canvas1
        global toolbar1
        global most_common_herb1
        if most_common_herb1.empty==True and canvas1.figure==None:
            tk.messagebox.showinfo('Tips', 'Please choose how many herbs you need to display first.')
        else:
            most_common_herb1=pd.DataFrame()
            try:
                canvas1.get_tk_widget().place_forget()
                canvas1.get_tk_widget().destroy()  
            except:
                pass
            try:
                toolbar1.destroy()
            except:
                pass    
            
            
    def Descript_save():
        global herb_list
        Counter_every_herb = Counter(herb_list)
        full_common_data = Counter_every_herb.most_common()
        full_common_data = pd.DataFrame(full_common_data,columns=['herb', 'count'])
        save_path=tk.StringVar()
        path = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[('Excel', '*.xlsx')], initialdir=(os.path.expanduser('~/Desktop')))
        save_path.set(path)
        full_common_data.to_excel(save_path.get()+'.xlsx',index=True)
        
        
tab1_button1=tk.Button(tab1,text="Display",command=lambda:DescriptiveStatistics.most_common_herb(),width=button_width, )  
tab1_button1.place(x=115,y=225)
tab1_button2=tk.Button(tab1,text="Clear",command=lambda:DescriptiveStatistics.forget_plot(),width=button_width, )
tab1_button2.place(x=225,y=225)
tips = tk.Label(tab1, text='Tips: Please clear the canvas before each redraw', font=fonttip,bg=framecolor)
tips.place(x=325,y=225)
tab1_button3=tk.Button(tab1,text="Download herbal frequency data",command=lambda:DescriptiveStatistics.Descript_save(),width=long_button_width,)
tab1_button3.place(x=400,y=5)

tab1_label1_tip=tk.Label(tab1,text='A toolbar will appear at the bottom when drawing, which can be used to adjust or save the image. Before redrawing, please click "Clear" to clear the old image and toolbar',font=fonttip,bg=framecolor,wraplength=1050,justify='left')
tab1_label1_tip.place(relx=0.0, rely=0.94)

# tab2 ---------------------------------------------------------------------
tab2 = tk.Frame(bg=framecolor,relief='ridge', borderwidth=2)

# 已选定的列表
opted_list = []
# 展示函数（该函数调用在button-"Start analysis"）
def displayIndex():
    global data
    global listToBeSelected
    listToBeSelected=data.index
    for pres in listToBeSelected:
        list_box1.insert('end', pres)
        
def PlusAndDecrease():
    global list_box1
    if list_box1.curselection()==():
        pass
    else:
        global opted_list
        global listToBeSelected
        for herb in list_box1.curselection():
            list_box2.insert('end', list_box1.get(herb))
            opted_list.append(list_box1.get(herb))
            list_box1.delete(herb)



# 相似度计算
class similarity:
    global file_dict
    global opted_list
    global herb_list
    def __init__(self) :
        herb_dense_dataframe = pd.DataFrame(columns=['pres_name', 'herb_name'])
        for pres_name in file_dict.keys():
            temp_simi_herb_list = file_dict.get(pres_name)
            pres_name = [pres_name]
            pres_name = pd.DataFrame(pres_name, columns=['pres_name'])
            herb_dense_dataframe = pd.concat([herb_dense_dataframe, pres_name], axis=0, join='outer')
            for herb in temp_simi_herb_list:
                herb_df = pd.DataFrame(columns=['herb_name'])
                herb = [herb]
                herb = pd.DataFrame(herb, columns=['herb_name'])
                herb_df = pd.concat([herb_df, herb], axis=0, join='outer')
                herb_dense_dataframe = pd.concat([herb_dense_dataframe, herb_df], axis=0, join='outer')
        herb_dense_dataframe['count'] = 1
        herb_dense_dataframe['pres_name'] = herb_dense_dataframe['pres_name'].fillna(method='ffill')
        herb_dense_dataframe.dropna(subset=['herb_name'], axis=0, inplace=True, how="any")
        herb_dense_dataframe = herb_dense_dataframe.pivot_table(
            'count', index=herb_dense_dataframe['pres_name'], columns=['herb_name']).fillna(0)
        herb_dense_dataframe = herb_dense_dataframe.astype('int')
        self.df = herb_dense_dataframe
    def dot_cos(self):
        dot_df = pd.DataFrame()
        cos_df = pd.DataFrame()
        for res1 in opted_list:
            dot_matrix = pd.DataFrame()
            cos_matrix = pd.DataFrame()
            for res2 in opted_list:
                vec1 = self.df.loc[res1]
                vec2 = self.df.loc[res2]
                dot = np.dot(vec1, vec2)
                cos = dot / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
                dot_matrix = dot_matrix.join(pd.DataFrame(dot,columns=[res2],index=[res1]), how='right')
                cos_matrix = cos_matrix.join(pd.DataFrame(cos,columns=[res2],index=[res1]), how='right')
            dot_df = pd.concat([dot_df, dot_matrix], axis=0, join="outer")
            cos_df = pd.concat([cos_df, cos_matrix], axis=0, join="outer")
        return dot_df, cos_df
    def dot(self):
        dot_df = pd.DataFrame()
        for index1, row1 in self.df.iterrows():
            dot_matrix = pd.DataFrame()
            series1 = np.array(self.df.loc[index1])
            for index2, row2 in self.df.iterrows():
                series2 = np.array(self.df.loc[index2])
                series1_2_dot = np.dot(series1, series2)
                dot_matrix = dot_matrix.join(pd.DataFrame([series1_2_dot], columns=[index2], index=[index1]), how='right')   
            dot_df = pd.concat([dot_df, dot_matrix], axis=0, join="outer")
        return dot_df
    def cos(self):
        cos_df = pd.DataFrame()
        for index1, row1 in self.df.iterrows():
            cos_matrix = pd.DataFrame()
            series1 = np.array(self.df.loc[index1])
            for index2, row2 in self.df.iterrows():
                series2 = np.array(self.df.loc[index2])
                series1_2_cos = np.dot(series1, series2) / \
                         (np.linalg.norm(series1) * np.linalg.norm(series2))
                cos_matrix = cos_matrix.join(pd.DataFrame([series1_2_cos], columns=[index2], index=[index1]), how='right')                             
            cos_df = pd.concat([cos_df, cos_matrix], axis=0, join="outer")
        return cos_df
    
    
    
    
canvas2 = btk.FigureCanvasTkAgg(master=tab2)
canvas3 = btk.FigureCanvasTkAgg(master=tab2)
def cal_dot():
    global font
    cal=similarity()
    dot=(cal.dot_cos())[0]
    fig2, ax2 = plt.subplots(1,1,figsize=(5,4))
    sns.heatmap(dot, annot=True, fmt=".2g", linewidths=.5, cmap='YlOrRd')
    ax2.set_title('Dot product')
    plt.xticks(font=font, rotation=45)
    plt.yticks(font=font, rotation=45)
    global canvas2
    canvas2 = btk.FigureCanvasTkAgg(fig2, master=tab2)  # A tk.DrawingArea.
    canvas2.draw()
    global toolbar2
    toolbar2 = btk.NavigationToolbar2Tk(canvas2, tab2)
    toolbar2.update()
    canvas2.get_tk_widget().place(x=20,y=250)
    
def cal_cos():
    global font
    cal=similarity()
    cos=(cal.dot_cos())[1] 
    fig3, ax3 = plt.subplots(1,1,figsize=(5,4))
    sns.heatmap(cos, annot=True, fmt=".2g", linewidths=.5, cmap='YlGnBu')
    ax3.set_title('Cosine similarity')
    plt.xticks(font=font, rotation=45)
    plt.yticks(font=font, rotation=45)
    global canvas3
    canvas3 = btk.FigureCanvasTkAgg(fig3, master=tab2)  # A tk.DrawingArea.
    canvas3.draw()
    global toolbar3
    toolbar3 = btk.NavigationToolbar2Tk(canvas3, tab2)
    toolbar3.update()
    canvas3.get_tk_widget().place(x=550,y=250)
    
tab2_box1 = tk.LabelFrame(tab2,relief='groove',bg=framecolor)
tab2_box1.place(x=460,y=77,width=600,height=165)

tab2_label1 = tk.Label(tab2_box1, text="The button on the below is used to calculate the dot value and cos value between the prescriptions of the entire dataset, it will take a long time, please perform this task when you are idle.", font=fonttip,wraplength=600,bg=framecolor,justify='left')
tab2_label1.place(x=0,y=0)




tab2_button5 = tk.Button(tab2_box1, text="Calculate dot matrix for all prescriptions", command=lambda:excute_dot(),width=35)
tab2_button6 = tk.Button(tab2_box1, text="Calculate cos matrix for all prescriptions", command=lambda:excute_cos(),width=35)
tab2_button5.place(x=0,y=70)
tab2_button6.place(x=270,y=70)
tab2_button7 = tk.Button(tab2_box1, text="Download dot", command=lambda:save_dot())
tab2_button8 = tk.Button(tab2_box1, text="Download cos", command=lambda:save_cos())

def cal_all_dot():
    all_cal = similarity()
    dot = all_cal.dot()
    return dot
    
def cal_all_cos():
    all_cal = similarity()
    cos = all_cal.cos()
    return cos


dot_matrix = pd.DataFrame()
def excute_dot():
    process1.step(50)
    process1.update()
    process1.start('idle')
    dot_m = cal_all_dot()
    global dot_matrix
    dot_matrix = dot_m
    process1.stop()
    tab2_button7.place(x=0,y=120)
    
    
cos_matrix = pd.DataFrame()
def excute_cos():
    process1.step(50)
    process1.update()
    process1.start('idle')
    cos_m = cal_all_cos()
    global cos_matrix
    cos_matrix = cos_m
    process1.stop()
    tab2_button8.place(x=270,y=120)
    
def save_dot():
    global dot_matrix
    path = tk.StringVar()
    savep = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[('CSV', '*.csv')], initialdir=(os.path.expanduser('~/Desktop')))
    path.set(savep)
    dot_matrix.to_csv(path.get()+'.csv',index=True)
def save_cos():
    global cos_matrix
    path = tk.StringVar()
    savep = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[('CSV', '*.csv')], initialdir=(os.path.expanduser('~/Desktop')))
    path.set(savep)
    cos_matrix.to_csv(path.get()+'.csv',index=True)

def tab2_clear():
    global opted_list
    global canvas2
    global canvas3
    global dot_matrix
    global cos_matrix
    dot_matrix = pd.DataFrame()
    cos_matrix = pd.DataFrame()
    if opted_list==[] and canvas2.figure == None and canvas3.figure == None:
        tk.messagebox.showinfo('Tips', 'Please select a prescription first')
    else:
        opted_list = []
        list_box2.delete(0, tk.END)
        for herb in opted_list:
            list_box1.insert(tk.END, herb)
        try:
            canvas2.get_tk_widget().place_forget()
            canvas2.get_tk_widget().destroy()
            canvas2.figure = None
        except:
            pass
        try:
            canvas3.get_tk_widget().place_forget()
            canvas3.get_tk_widget().destroy()
            canvas3.figure = None
        except:
            pass
        try:
            toolbar2.destroy()
        except:
            pass
        try:
            toolbar3.destroy()
        except:
            pass  
    try:
        tab2_button7.destroy()
    except:
        pass
    try:
        tab2_button8.destroy()
    except:
        pass
        
#tab2的选择栏和说明栏

tab2_illustrate1 = tk.Label(tab2, text='Focus on dot product and cosine similarity for a specific prescription', font=fontsty,bg=framecolor)
tab2_illustrate1.pack(side='top', anchor='nw',padx=5, pady=5)

tab2_illustrate2 = tk.Label(tab2, text='Please select the prescription you want to analyze,choose at least 2 or more.', font=fonttip,bg=framecolor)
tab2_illustrate2.pack(side='top', anchor='nw',padx=5, pady=5)

list_box1=tk.Listbox(tab2,selectmode='multiple',width=15,height=9,)
list_box1.pack(side='left', anchor='nw',padx=5, pady=5)

tab2_button1 = tk.Button(tab2, text='Add to', command=lambda:PlusAndDecrease(), width=button_width)
tab2_button1.pack(side='left', anchor='nw',padx=5, pady=5)

list_box2=tk.Listbox(tab2,selectmode='multiple',width=15,height=9,)
list_box2.pack(side='left', anchor='nw',padx=5, pady=5)

tab2_button2 = tk.Button(tab2, text="Calculate cos", command=cal_cos,width=button_width)
tab2_button2.pack(side='top', anchor='nw',padx=5, pady=5,after=list_box2)

tab2_button3 = tk.Button(tab2, text="Calculate dot", command=cal_dot,width=button_width)
tab2_button3.pack(side='top', anchor='nw',padx=5, pady=5,after=list_box2)

# tab2的清屏按钮
    
tab2_button4 = tk.Button(tab2, text="Clear", command=tab2_clear,width=button_width)
tab2_button4.pack(side='top', anchor='nw',padx=5, pady=5,after=tab2_button2)

tab2_label_tip=tk.Label(tab2,text='The program will pop up a window when drawing, you can adjust or save the image through this window, when you want to redraw, you must first close the pop-up window',font=fonttip,bg=framecolor,wraplength=1050,justify='left')
tab2_label_tip.place(relx=0.0, rely=0.94)

# --------------------------------------------------------------------------------------
# tab3开始

tab3=tk.Frame(bg=framecolor,relief='ridge', borderwidth=2)


def tf_idf():   
    global herb_list
    global file_dict
    global list_vect
    tf_idf_dict = dict()
    lexicon=sorted(set(herb_list))
    for tf_pres_name in file_dict.keys():
        ini_tf_vect = dict()
        herbs = file_dict.get(tf_pres_name)
        herbs_counts = Counter(herbs)
        for index, value in herbs_counts.items():
            docs_contain_key = 0
            for herb_row in list_vect:
                if (index in herb_row) == True:
                    docs_contain_key = docs_contain_key + 1
            tf = value / len(lexicon)
            if docs_contain_key != 0:
                idf = len(file_dict.keys()) / docs_contain_key
            else:
                idf = 0
            ini_tf_vect[index] = tf * idf
        tf_idf_dict[tf_pres_name] = ini_tf_vect
    tf_idf_dataframe = pd.DataFrame(columns=['pres_name', 'herb_name'])
    for pres_name in tf_idf_dict.keys():
        herb_tf_idf_dict = tf_idf_dict.get(pres_name)
        pres_name = [pres_name]
        pres_name = pd.DataFrame(pres_name, columns=['pres_name'])
        tf_idf_dataframe = pd.concat([tf_idf_dataframe, pres_name], axis=0, join='outer')
        for herb_name in herb_tf_idf_dict:
            herb_df = pd.DataFrame(columns=['herb_name', 'herb_tf_idf_value'])
            herb_tf_value = herb_tf_idf_dict.get(herb_name)
            herb_name = [herb_name]
            herb_name = pd.DataFrame(herb_name, columns=['herb_name'])
            herb_df = pd.concat([herb_df, herb_name], axis=0, join='outer')
            herb_tf_value = round(herb_tf_value, 3)
            herb_tf_value = [herb_tf_value]
            herb_tf_value = pd.DataFrame(herb_tf_value, columns=['herb_tf_idf_value'])
            herb_df = pd.concat([herb_df, herb_tf_value], axis=0, join='outer')
            tf_idf_dataframe = pd.concat([tf_idf_dataframe, herb_df], axis=0, join='outer')
    idf_df = cp.copy(tf_idf_dataframe)
    idf_df['pres_name'] = idf_df['pres_name'].fillna(method='ffill')
    idf_df['herb_name'] = idf_df['herb_name'].fillna(method='ffill')
    idf_df.dropna(subset=['herb_tf_idf_value'], axis=0, inplace=True, how="any")
    idf_df = idf_df.pivot_table('herb_tf_idf_value', index=['pres_name'], columns=['herb_name']).fillna(round(0, 3))
    idf_df['tf_idf_sum'] = idf_df.apply(lambda x: x.sum(),axis=1)
    sum_table=pd.DataFrame(idf_df['tf_idf_sum'])
    tf_idf_sort_dict=dict()
    for index, row in sum_table.iterrows():
        for i in row:
            temp_tfidf_herb_list = file_dict.get(index)
            len_pres = len(temp_tfidf_herb_list)
            mean_tf_idf = i / len_pres
            tf_idf_sort_dict[index] = mean_tf_idf
    tf_idf_mean_value=pd.DataFrame.from_dict(tf_idf_sort_dict, orient='index')
    tf_idf_mean_value.columns=['tf_idf_mean']
    global data
    tf_idf_herb_list=data
    tf_idf_mean_value_herb_list=pd.concat([tf_idf_mean_value, tf_idf_herb_list], axis=1)
    tf_idf_sort = tf_idf_mean_value_herb_list.sort_values(by=['tf_idf_mean'], ascending=False)
    return tf_idf_sort, idf_df,tf_idf_dict


tab3_radio=tk.IntVar()
def tf_idf_diplay(tab3_num):
    if filename.get()!="":
        if tab3_table1.get_children() != ():  # 如果表格存在数据，清空
            for item in tab3_table1.get_children():
                tab3_table1.delete(item)
        sort_table = tf_idf()[0]
        sort_table = sort_table.round({'tf_idf_mean':3})
        if tab3_radio.get()==1:
            sort_head = sort_table.head(tab3_num)
            sort_head = sort_head.astype(str)
            for pres,row in sort_head.iterrows():
                tf=sort_head.loc[pres]['tf_idf_mean']
                col_0=sort_head.columns[1]
                herb = sort_head.loc[pres][col_0]
                value = (pres,tf,herb)
                tab3_table1.insert('', 'end', values=value)
        elif tab3_radio.get()==2:
            sort_tail = sort_table.tail(tab3_num)
            sort_tail = sort_tail.astype(str)
            for pres,row in sort_tail.iterrows():
                tf=sort_tail.loc[pres]['tf_idf_mean']
                col_0=sort_tail.columns[1]
                herb = sort_tail.loc[pres][col_0]
                value = (pres,tf,herb)
                tab3_table1.insert('', 'end', values=value)
        else:
            tk.messagebox.showinfo("Tips","Please select the sorting method")
    else:
         tk.messagebox.showinfo("Tips","Please select a file to open")
    
def download_tf_idf():
    if filename.get()!="":
        sort_table = tf_idf()[0]
        sort_table = sort_table.round({'tf_idf_mean':3})
        
        save_path=tk.StringVar()
        path = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[('Excel', '*.xlsx')], initialdir=(os.path.expanduser('~/Desktop')))
        save_path.set(path)
        sort_table.to_excel(save_path.get()+'.xlsx',index=True)
    else:
        tk.messagebox.showinfo("Tips","Please select a file to open")
        
        
        
    
    

tab3_label1 = tk.Label(tab3,text='TF-IDF value calculation has been completed in the background.', font=fontsty,bg=framecolor)
tab3_label1.pack(side='top', anchor='nw',padx=5, pady=5)

tab3_label2 = tk.Label(tab3,text='please select the number of prescriptions you want to display.', font=fonttip,bg=framecolor)
tab3_label2.pack(side='top', anchor='nw',padx=5, pady=5)

tab3_spinbox = tk.Spinbox(tab3, from_=1, to=50, width=5)
tab3_spinbox.pack(side='left', anchor='nw',padx=5, pady=5)

tab3_ratio1 = tk.Radiobutton(tab3, text='General herbal prescription', variable=tab3_radio, value=1,bg=framecolor)
tab3_ratio2 = tk.Radiobutton(tab3, text='Rare herbal prescription', variable=tab3_radio, value=2,bg=framecolor)
tab3_ratio1.pack(side='left', anchor='nw',padx=5, pady=5)
tab3_ratio2.pack(side='left', anchor='nw',padx=5, pady=5,after=tab3_ratio1)

tab3_button1 = tk.Button(tab3, text='Display', command=lambda:tf_idf_diplay(tab3_num=int(tab3_spinbox.get())), width=button_width)
tab3_button1.pack(side='left', anchor='nw',padx=5, pady=5)

tab3_button2 = tk.Button(tab3, text='Clear', command=lambda:tab3_table1.delete(*tab3_table1.get_children()), width=button_width)
tab3_button2.pack(side='left', anchor='nw',padx=5, pady=5)

tab3_button3 = tk.Button(tab3,text='Download the full form', command=lambda:download_tf_idf(), width=long_button_width)
tab3_button3.pack(side='left', anchor='nw',padx=5, pady=5)



tab3_table1 = ttk.Treeview(tab3, columns=('head Prescription', 'Average TF-IDF', 'herbal composition'), show='headings')
tab3_table1.heading('head Prescription', text='head Prescription')
tab3_table1.heading('Average TF-IDF', text='Average TF-IDF')
tab3_table1.heading('herbal composition', text='herbal composition')
tab3_table1.place(x=0, y=120, relwidth=1, relheight=0.83)

# ---------------------------------------------------------------------------
# tab4开始

tab4=tk.Frame(bg=framecolor,relief='ridge', borderwidth=2)

tab4_label1 = tk.Label(tab4,text='Topic classification based on Latent Semantic Analysis (LSA)', font=fontsty,bg=framecolor)
tab4_label1.pack(side='top', anchor='nw',padx=5, pady=5)

tab4_label2 = tk.Label(tab4,text='Please select the number of topics you want to classify.', font=fonttip,bg=framecolor)
tab4_label2.pack(side='top', anchor='nw',padx=5, pady=5)

tab4_spinbox = tk.Spinbox(tab4, from_=1, to=500, width=long_button_width)
tab4_spinbox.pack(side='left', anchor='nw',padx=5, pady=5)

canvas4 = btk.FigureCanvasTkAgg()
pres_df=pd.DataFrame()
herb_df=pd.DataFrame()
class lsa_display():
    def __init__(self):
        self.idf = tf_idf()[1]
        self.num = int(tab4_spinbox.get())
    def svd_plot(self):
        self.idf.drop(['tf_idf_sum'], axis=1, inplace=True)
        self.idf = self.idf.T
        svd = dcp.TruncatedSVD(n_components=self.num, n_iter=10,random_state=123)
        svd_model = svd.fit(self.idf)
        svd_topic = svd.transform(self.idf)
        explvara_list = list(svd.explained_variance_ratio_)
        sing = svd_model.singular_values_
        expl_cum = np.cumsum(explvara_list)
        lsa_topic = pd.DataFrame(
            {'topic': range(1, self.num + 1), 'explained_variance': explvara_list, 'cumulative_explained_variance': expl_cum,
             'singular_values': sing})
        lsa_topic = lsa_topic.set_index('topic')
        fig4=plt.figure(figsize=(8, 5))
        plt.subplot2grid((6,10),(0,0),colspan=5,rowspan=6)
        plt.plot(expl_cum,color='red')
        plt.xlabel('Number of components',fontsize=fontplotsize)
        plt.xticks(fontsize=fontplotsize)
        plt.ylabel('Cumulative explained variance',fontsize=fontplotsize)
        plt.yticks(fontsize=fontplotsize)
        plt.subplot2grid((6,8),(0,5),colspan=4,rowspan=3)
        plt.plot(sing,color='blue')
        plt.ylabel('Singular values',fontsize=fontplotsize)
        plt.yticks(fontsize=fontplotsize)
        plt.xticks([])
        plt.subplot2grid((6,8),(3,5),colspan=4,rowspan=3)
        plt.plot(explvara_list,color='green')
        plt.xlabel('Number of components',fontsize=fontplotsize)
        plt.xticks(fontsize=fontplotsize)
        plt.ylabel('Explained variance',fontsize=fontplotsize)
        plt.yticks(fontsize=fontplotsize)
        global canvas4
        canvas4 = btk.FigureCanvasTkAgg(fig4, master=tab4)  # A tk.DrawingArea.
        canvas4.draw()
        global toolbar4
        toolbar4 = btk.NavigationToolbar2Tk(canvas4, root)
        toolbar4.update()
        canvas4.get_tk_widget().place(x=0,y=120)
    def lsa_confirm(self):
        self.idf.drop(['tf_idf_sum'], axis=1, inplace=True)
        self.idf = self.idf.T
        svd = dcp.TruncatedSVD(n_components=self.num, n_iter=10, random_state=123)
        svd = svd.fit(self.idf)
        svd_topic = svd.transform(self.idf)
        columns = ['topic{}'.format(i) for i in range(svd.n_components)]
        pres_svd_topic = pd.DataFrame(svd_topic, columns=columns, index=self.idf.index)
        herb_svd_weight = pd.DataFrame(svd.components_, columns=self.idf.columns,
                                       index=columns)
        herb_svd_weight = herb_svd_weight.T
        global tab4_button3
        global tab4_button4
        tab4_button3 = tk.Button(tab4, text='Download prescription classification data', command=lambda:lsa_pres_download(), width=35)
        tab4_button3.place(x=800, y=120)
        tab4_button4 = tk.Button(tab4, text='Download herb classification data', command=lambda:lsa_herb_download(), width=35)
        tab4_button4.place(x=800, y=160)
        global pres_df
        global herb_df
        pres_df = pres_svd_topic
        herb_df = herb_svd_weight
        
    
def excute_lsa():
    global canvas4
    try:
        canvas4.get_tk_widget().place_forget()
        canvas4.get_tk_widget().destroy()
    except:
        pass
    if filename == '':
        tk.messagebox.showinfo('Warning', 'Please upload the data first!')
    else:
        if int(tab4_spinbox.get())<len(data.index):
            lsa = lsa_display()
            lsa.svd_plot()
        else:
            tk.messagebox.showinfo('Warning', 'The number of topics is too large!')

def confirm_lsa():
    if filename == '':
        tk.messagebox.showinfo('Warning', 'Please upload the data first!')
    else:
        lsa = lsa_display()
        lsa.lsa_confirm()
        
tab4_savepath1 = tk.StringVar()

def lsa_pres_download():
    global pres_df
    global tab4_savepath1
    path = filedialog.asksaveasfilename(title='Save file', filetypes=[('Excel', '*.xlsx')])
    tab4_savepath1.set(path)
    pres_df.to_excel(tab4_savepath1.get()+'.xlsx',index=True)

tab4_savepath2 = tk.StringVar()

def lsa_herb_download():
    global herb_df
    global tab4_savepath2
    path = filedialog.asksaveasfilename(title='Save file', filetypes=[('Excel', '*.xlsx')])
    tab4_savepath2.set(path)
    herb_df.to_excel(tab4_savepath2.get()+'.xlsx',index=True)
    
def lsa_clear():
    global canvas4
    global tab4_button3
    global tab4_button4
    global tab4_savepath1
    global tab4_savepath2
    global pres_df
    global herb_df
    pres_df=pd.DataFrame()
    herb_df=pd.DataFrame()
    tab4_savepath1.set('')
    tab4_savepath2.set('')
    try:
        tab4_button3.destroy()
        tab4_button4.destroy()
    except:
        pass
    try:
        canvas4.get_tk_widget().place_forget()
        canvas4.get_tk_widget().destroy()
        canvas4.figure = None
    except:
        pass
    try:
        toolbar4.destroy()
    except:
        pass
            
    
tab4_button1 = tk.Button(tab4, text='Classification', command=lambda:excute_lsa(), width=button_width)
tab4_button1.pack(side='left', anchor='nw',padx=5, pady=5)

tab4_button2 = tk.Button(tab4, text='Confirm the classification results', command=lambda:confirm_lsa(), width=long_button_width)
tab4_button2.pack(side='left', anchor='nw',padx=5, pady=5)

tab4_button5 = tk.Button(tab4, text='Clear', command=lambda:lsa_clear(), width=button_width)
tab4_button5.pack(side='left', anchor='nw',padx=5, pady=5)

tab4_label_tip=tk.Label(tab4,text='The program will pop up a window when drawing, you can adjust or save the image through this window, when you want to redraw, you must first close the pop-up window',font=fonttip,bg=framecolor,wraplength=1050,justify='left')
tab4_label_tip.place(relx=0.0, rely=0.94)
# -------------------------------------------------------------------------------------------------
# tab5
tab5=tk.Frame(bg=framecolor,relief='ridge', borderwidth=2)


tab5_label1 = tk.Label(tab5,text='Topic classification based on Latent Dirichlet Distribution (LDiA)', font=fontsty,bg=framecolor)
tab5_label1.pack(side='top', anchor='nw',padx=5, pady=5)


tab5_label2 = tk.Label(tab5,text='Please select the number of topics you want to classify.', font=fonttip,bg=framecolor)
tab5_label2.pack(side='top', anchor='nw',padx=5, pady=5)

tab5_spinbox = tk.Spinbox(tab5, from_=1, to=500, width=long_button_width)
tab5_spinbox.pack(side='left', anchor='nw',padx=5, pady=5)

ldia_pres_df=pd.DataFrame()
ldia_herb_df=pd.DataFrame()
class ldia_display(similarity):
    def __init__(self):
        self.num = int(tab5_spinbox.get())
        similarity.__init__(self)
    def ldia_plot(self):
        x = []
        y = []
        for i in range(1, self.num + 1):
            ldia = dcp.LatentDirichletAllocation(n_components=i, learning_method='batch', evaluate_every=1, verbose=1, max_iter=50,random_state=123)
            ldia = ldia.fit(self.df)
            plex = ldia.perplexity(self.df)
            x.append(i)
            y.append(plex)
        ldia_topic = pd.DataFrame(y, columns=['perplexity'], index=x)
        fig5 = plt.figure(figsize=(8, 5))
        plt.plot(ldia_topic)
        plt.xlabel('Number of components',fontsize=fontplotsize)
        plt.xticks(fontsize=fontplotsize)
        plt.ylabel('Perplexity',fontsize=fontplotsize)
        plt.yticks(fontsize=fontplotsize)
        global canvas5
        canvas5 = btk.FigureCanvasTkAgg(fig5, tab5)
        canvas5.draw()
        global toolbar5
        toolbar5 = btk.NavigationToolbar2Tk(canvas5, root)
        toolbar5.update()
        canvas5.get_tk_widget().place(x=0, y=120)
        
    def ldia_confirm(self):
        ldia = dcp.LatentDirichletAllocation(n_components=self.num, learning_method='batch', evaluate_every=1, verbose=1, max_iter=50,random_state=123)
        ldia = ldia.fit(self.df)
        columns = ['topic{}'.format(i) for i in range(ldia.n_components)]
        components_herb = pd.DataFrame(ldia.components_.T, index=self.df.columns, columns=columns)
        components_pres = ldia.transform(self.df)
        components_pres = pd.DataFrame(components_pres, index=self.df.index, columns=columns)
        global tab5_button3
        global tab5_button4
        tab5_button3 = tk.Button(tab5, text='Download prescription classification data', command=lambda:ldia_pres_download(), width=35)
        tab5_button4 = tk.Button(tab5, text='Download herb classification data', command=lambda:ldia_herb_download(), width=35)
        tab5_button3.place(x=800,y=120)
        tab5_button4.place(x=800,y=160)
        global ldia_pres_df
        global ldia_herb_df
        ldia_pres_df = components_pres
        ldia_herb_df = components_herb
        
def excute_ldia():
    global canvas5
    try:
        canvas5.get_tk_widget().place_forget()
        canvas5.get_tk_widget().destroy()
    except:
        pass
    if filename == '':
        tk.messagebox.showinfo('Warning', 'Please upload the data first!')
    else:
        ldia = ldia_display()
        ldia.ldia_plot()

def confirm_ldia():
    if filename == '':
        tk.messagebox.showinfo('Warning', 'Please upload the data first!')
    else:
        ldia = ldia_display()
        ldia.ldia_confirm()

tab5_savepath1 = tk.StringVar()
def ldia_pres_download():
    global ldia_pres_df
    global tab5_savepath1
    path = filedialog.asksaveasfilename(title='Save file', filetypes=[('Excel', '*.xlsx')])
    tab5_savepath1.set(path)
    ldia_pres_df.to_excel(tab5_savepath1.get()+'.xlsx',index=True)

tab5_savepath2 = tk.StringVar()
def ldia_herb_download():
    global ldia_herb_df
    global tab5_savepath2
    path = filedialog.asksaveasfilename(title='Save file', filetypes=[('Excel', '*.xlsx')])
    tab5_savepath2.set(path)
    ldia_herb_df.to_excel(tab5_savepath2.get()+'.xlsx',index=True)

def ldia_clear():
    global canvas5
    global tab5_button3
    global tab5_button4
    global tab5_savepath1
    global tab5_savepath2
    global ldia_pres_df
    global ldia_herb_df
    if canvas5.figure != None:
        ldia_pres_df=pd.DataFrame()
        ldia_herb_df=pd.DataFrame()
        tab5_savepath1.set('')
        tab5_savepath2.set('')
        tab5_button3.destroy()
        tab5_button4.destroy()
        try:
            canvas5.get_tk_widget().place_forget()
            canvas5.get_tk_widget().destroy()
            canvas5.figure = None
        except:
            pass
tab5_button1 = tk.Button(tab5, text='Classification', command=lambda:excute_ldia(), width=button_width)
tab5_button1.pack(side='left', anchor='nw',padx=5, pady=5)

tab5_button2 = tk.Button(tab5, text='Confirm the classification results', command=lambda:confirm_ldia(), width=long_button_width)
tab5_button2.pack(side='left', anchor='nw',padx=5, pady=5)

tab5_button5 = tk.Button(tab5, text='Clear', command=lambda:ldia_clear(), width=button_width)
tab5_button5.pack(side='left', anchor='nw',padx=5, pady=5)

tab5_label_tip=tk.Label(tab5,text='The program will pop up a window when drawing, you can adjust or save the image through this window, when you want to redraw, you must first close the pop-up window',font=fonttip,bg=framecolor,wraplength=1050,justify='left')
tab5_label_tip.place(relx=0.0, rely=0.94)
# ----------------------------------------------------------------
# tab6
tab6 = tk.Frame(bg=framecolor,relief='ridge', borderwidth=2)

tab6_label1 = tk.Label(tab6, text='Please select the functions you wish to implement through the Word2Vec model')
tab6_label1.pack(side='top', anchor='nw',padx=5, pady=5)

class word2vec():
    global file_dict
    global list_vect
    def __init__(self):
        len_herb_list = 0
        for index in file_dict.keys():
            local_herb_list = file_dict.get(index)
            local_herb_list = list(set(local_herb_list))
            len_list = len(local_herb_list)
            len_herb_list = len_herb_list + len_list
        avg_len = len_herb_list / (len(file_dict.keys()))
        self.avg=avg_len
        self.list=list_vect
    def w2v_model(self):
        model = gensim.models.Word2Vec(self.list, sg=0, min_count=1, vector_size=100, window=self.avg)
        return model
    def full_common(self):
        global herb_list
        Counter_every_herb = Counter(herb_list)
        full_common = Counter_every_herb.most_common(int(SpinBar.get()))
        full_common_data = pd.DataFrame(full_common, columns=['herb', 'count'])
        return full_common_data

class w2v_matrix(word2vec):
    def __init__(self):
        super().__init__()
        self.model = self.w2v_model()
        self.full_common_data = self.full_common()
    def w2v_matr(self):
        a = pd.DataFrame(self.model.wv.index_to_key, columns=['name'])
        b = pd.DataFrame(self.model.wv.vectors, index=a['name'])
        pca = dcp.PCA(n_components=2, random_state=123)
        pca = pca.fit(b)
        pca_vectr = pca.transform(b)
        full_common_data = self.full_common_data.set_index('herb')
        columns = ['topic{}'.format(i) for i in range(pca.n_components)]
        pca_topic = pd.DataFrame(pca_vectr, columns=columns, index=b.index)
        pca_matrix = pca_topic.round(3)
        pca_matrix = pca_matrix.join(full_common_data)
        pca_matrix = pca_matrix.reset_index()
        pca_matrix.rename(columns={'topic0':'Vector 1','topic1':'Vector 2'},inplace=True)
        return pca_matrix

class w2v_plot(w2v_matrix):
    def __init__(self):
        super().__init__()
        self.pca_matrix = self.w2v_matr()
    def w2v_plot(self):
        w2v_data = alt.Chart(self.pca_matrix).mark_circle().encode(
        x='Vector 1', y='Vector 2', size='count', color='count', tooltip=['name', 'count']).interactive()
        canvas6 = tk.Canvas(tab6, width=150, height=150, bg=framecolor)
        img = tk.PhotoImage(file=(w2v_data.save('w2v_plot.png')))
        canvas6.create_image(0, 0, anchor='nw', image=img)
        canvas6.pack(side='left', anchor='nw',padx=5, pady=5)
        

    
    
    
tab6_radio=tk.IntVar()
herb1 = tk.StringVar()
herb2 = tk.StringVar()
herb3 = tk.StringVar()
tab6_ratio1 = tk.Radiobutton(tab6, text='Similar herbal search', variable=tab6_radio, value=1,bg=framecolor,command=lambda:w2v_calculation.simi())
tab6_ratio2 = tk.Radiobutton(tab6, text='Herbal analogy', variable=tab6_radio, value=2,bg=framecolor,command=lambda:w2v_calculation.analogy())
tab6_ratio3 = tk.Radiobutton(tab6, text='Compatibility assessment', variable=tab6_radio, value=3,bg=framecolor,command=lambda:w2v_calculation.comp())
tab6_ratio1.pack(side='top', anchor='nw',padx=5, pady=5)
tab6_ratio2.pack(side='top', anchor='nw',padx=5, pady=5)
tab6_ratio3.pack(side='top', anchor='nw',padx=5, pady=5)


box = tk.Frame(tab6,width = 1000,height = 600,bg = framecolor)
box.pack(side='top', anchor='nw',padx=5, pady=5)

box1 = tk.Frame(tab6,bg = framecolor)
box1.place(relx=0.5,rely=0.2,relwidth=0.499,relheight=0.78)

tab6_button2 = tk.Button(tab6, text='Start calculation', command=lambda:start(), width=15)
tab6_button3 = tk.Button(tab6, text='Clear',command=lambda:tab6_clear(),width=15)

tab6_table = ttk.Treeview(box1, columns=('herb', 'similarity'), show='headings')
tab6_table.heading('herb', text='Herb')
tab6_table.heading('similarity', text='Smilarity')

    
class w2v_calculation():
    global box
    global tab6_radio
    global tab6_button2
    def simi():
        try:
            for widget in box.winfo_children():
                widget.destroy()
        except:
            pass
        w2v_label1 = tk.Label(box, text='Similar herbal search',font=fontsty,bg=framecolor)
        w2v_label1.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_label2 = tk.Label(box, text='Please enter the name of the herb you want to search',font=fonttip,bg=framecolor)
        w2v_label2.pack(side='top', anchor='nw',padx=5, pady=5)
        global w2v_entry1
        w2v_entry1 = tk.Entry(box, width=entry_width)
        w2v_entry1.pack(side='top', anchor='nw',padx=5, pady=5)
        tab6_button2.pack(side='top', anchor='nw',padx=5, pady=5)
        tab6_button3.pack(side='top', anchor='nw',padx=5, pady=5)
    def analogy():
        try:
            for widget in box.winfo_children():
                widget.destroy()
        except:
            pass
        w2v_label3 = tk.Label(box, text='Herbal analogy',font=fontsty,bg=framecolor)
        w2v_label3.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_label4 = tk.Label(box, text='Please enter the name of the herb you want to search',font=fonttip,bg=framecolor)
        w2v_label4.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_label5 = tk.Label(box, text='If you want to directly compare the similarity of two herbs, please enter the\n herb name in Herb 1 and Herb 2',font=fonttip,justify='left',bg=framecolor)
        w2v_label5.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_label6 = tk.Label(box, text='Herb 1',font=fonttip,bg=framecolor)
        w2v_label6.pack(side='top', anchor='nw',padx=5, pady=5)
        global w2v_entry2,w2v_entry3,w2v_entry4
        w2v_entry2 = tk.Entry(box, width=entry_width)
        w2v_entry2.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_label7 = tk.Label(box, text='Herb 2',font=fonttip,bg=framecolor)
        w2v_label7.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_entry3 = tk.Entry(box, width=entry_width)
        w2v_entry3.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_label8 = tk.Label(box, text='If you want to use the method of analogy to explore the law of paired\n combination of herbs, please also fill in Analogy Item',font=fonttip,justify='left',bg=framecolor)
        w2v_label8.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_label9 = tk.Label(box, text='Analogy Item',font=fonttip,bg=framecolor)
        w2v_label9.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_entry4 = tk.Entry(box, width=entry_width)
        w2v_entry4.pack(side='top', anchor='nw',padx=5, pady=5)
        tab6_button2.pack(side='top', anchor='nw',padx=5, pady=5)
        tab6_button3.pack(side='top', anchor='nw',padx=5, pady=5)
    def comp():
        try:
            for widget in box.winfo_children():
                widget.destroy()
        except:
            pass
        w2v_label10 = tk.Label(box, text='Compatibility assessment',font=fontsty,bg=framecolor)
        w2v_label10.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_label11 = tk.Label(box, text='Please enter the herb list you want to assessment',font=fonttip,bg=framecolor)
        w2v_label11.pack(side='top', anchor='nw',padx=5, pady=5)
        w2v_label12 = tk.Label(box, text='(Tips: Use "," (English format) to separate the herbs)',font=fonttip,bg=framecolor)
        w2v_label12.pack(side='top', anchor='nw',padx=5, pady=5)
        global w2v_entry5
        w2v_entry5 = tk.Entry(box, width=entry_width)
        w2v_entry5.pack(side='top', anchor='nw',padx=5, pady=5)
        tab6_button2.pack(side='top', anchor='nw',padx=5, pady=5)
        tab6_button3.pack(side='top', anchor='nw',padx=5, pady=5)
    def read_simi():
        global w2v_entry1
        str1 = w2v_entry1.get()
        return str1
    def read_analogy():
        global w2v_entry2,w2v_entry3,w2v_entry4
        p1 = w2v_entry2.get()
        n1 = w2v_entry3.get()
        p2 = w2v_entry4.get()
        return p1,n1,p2
    def read_comp():
        global w2v_entry5
        str5 = w2v_entry5.get()
        return str5
    
        

            
            
class w2v_frame():
    global herb1,herb2,herb3
    global tab6_table
    global box1
    def cal():
        w2v=word2vec()
        model = w2v.w2v_model()
        try:
            if tab6_table.get_children() != ():  # 如果表格存在数据，清空
                for item in tab6_table.get_children():
                    tab6_table.delete(item)
        except:
            pass
        
        
            
        if tab6_radio.get() == 1:
            
            feed=w2v_calculation.read_simi()
            #herb1.set(feed.get())
            feed_herb = model.wv.most_similar(positive=[feed], topn=10)
            feed_herb = pd.DataFrame(feed_herb, columns=['herb', 'similarity'])
            for index,row in feed_herb.iterrows():
                herb=feed_herb.loc[index]['herb']
                simi_value=feed_herb.loc[index]['similarity']
                value = (herb,simi_value)
                tab6_table.insert('', 'end', values=value) 
            tab6_table.place(x=0, y=55)
            cal_label_1 = tk.Label(box1, text='Herbs with vector similarity to {} in the dataset are as follows'.format(feed),font=fonttip,bg=framecolor)
            cal_label_1.place(x=0, y=15)
        elif tab6_radio.get() == 2:
            p2 = w2v_calculation.read_analogy()[2]
            if p2 == '':
                p1 = w2v_calculation.read_analogy()[0]
                n1 = w2v_calculation.read_analogy()[1]
                
                feed_herb = model.wv.similarity(p1, n1)
                cal_label1 = tk.Label(box1, text='The similarity of {} and {} is {}'.format(p1,n1,feed_herb),font=fonttip,bg=framecolor)
                cal_label1 .place(x=0, y=15)
            elif p2 != '':
                p1 = w2v_calculation.read_analogy()[0]
                n1 = w2v_calculation.read_analogy()[1]
                p2 = w2v_calculation.read_analogy()[2]
                
                feed_herb=model.wv.most_similar(positive=[p2,p1],negative=[n1],topn=10)
                feed_herb=pd.DataFrame(feed_herb,columns=['herb','vector_similarity'])
                feed_herb=feed_herb.sort_values(by='vector_similarity',ascending=False)
                for index,row in feed_herb.iterrows():
                    herb=feed_herb.loc[index]['herb']
                    simi_value=feed_herb.loc[index]['vector_similarity']
                    value = (herb,simi_value)
                    tab6_table.insert('', 'end', values=value)
                    
                tab6_table.place(x=0, y=125)
                best_match=feed_herb.iloc[0,0]
                cal_label2 = tk.Label(box1, text='Imitating the combination rule of {} and {}, {}is a more matching herb with {}'.format(p1,n1,best_match,p2),font=fonttip,wraplength=box1.winfo_width(),bg=framecolor,justify='left')
                cal_label2.place(x=0, y=15)
                cal_label3 = tk.Label(box1, text='Alternative herbs that can be paired with {} in the table below'.format(p2),font=fonttip,wraplength=box1.winfo_width(),justify='left',bg=framecolor)
                cal_label3.place(x=0, y=75)
        elif tab6_radio.get() == 3:
            input_herb = w2v_calculation.read_comp()
            input_herb_list = input_herb.split(',')
            feed_herb=model.wv.doesnt_match(input_herb_list)
            cal_label4 = tk.Label(box1, text='In this list of herbs, {} has the farthest vector distance from other herbs. Please evaluate whether the use of {} is reasonable in combination with the needs of clinical practice'.format(feed_herb,feed_herb),font=fonttip,wraplength=box1.winfo_width(),justify='left',bg=framecolor)
            cal_label4.place(x=0, y=25)

def start():
    
    if filename.get() != '':
        w2v_frame.cal()  
    else:
        tk.messagebox.showinfo(title='Tips', message='Please select the file')

def tab6_clear():
    try:
        for widget in box1.winfo_children():
                widget.destroy()
    except:
        pass
    



MultiGroupTab.add(tab1, text="Descriptive statistics")
MultiGroupTab.add(tab2, text="Prescription similarity")
MultiGroupTab.add(tab3, text="General analysis")
MultiGroupTab.add(tab4, text="LSA topic distribution")
MultiGroupTab.add(tab5, text="LDiA topic distribution")
MultiGroupTab.add(tab6, text="Word2Vec model")
MultiGroupTab.place(relx=0.099,rely=0.05,relwidth=0.89,relheight=0.93)
root.mainloop()


# %%
