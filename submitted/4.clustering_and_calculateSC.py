
import xlwt
import xlsxwriter
import numbers
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn import metrics
from sklearn.metrics import classification_report
from scipy import stats

np.set_printoptions(threshold=np.inf)
filePath = r'Table S2. DTW matrix of 3,880 growth curves.xlsx'#

filePath01 = r'Table S3. DDTW matrix of 3,880 growth curves.xlsx'

filePath03 = r'LABEL.xlsx'
data = pd.read_excel(filePath)
data01 = pd.read_excel(filePath01)
data03 = pd.read_excel(filePath03)
filePath02 = r'LABEL_TYPE.xlsx'

filePath04 = r'Table S2. DTW matrix of 3,880 growth curves.xlsx'#


data2 = pd.read_excel(filePath02)
data04 = pd.read_excel(filePath04)

inddd = data2.iloc[0]


# nn=data.columns
data = np.array(data)

hh = data03.iloc[0]
data01 = np.array(data01)


def add(x, y, a):
    c = 1 - a
    z = c * x + a * y
    return (z)


α = np.arange(0,1.1,0.1)
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheetSC_list = book.add_sheet('SC_list', cell_overwrite_ok=True)
sheetARI_list = book.add_sheet('ARI_list', cell_overwrite_ok=True)
sheetami_lsit = book.add_sheet('ami_lsit', cell_overwrite_ok=True)
sheetCHI_list = book.add_sheet('CHI_list', cell_overwrite_ok=True)
sheetVmeasure_list = book.add_sheet('Vmeasure_list', cell_overwrite_ok=True)
sheetpre = book.add_sheet('pre', cell_overwrite_ok=True)
book2 = xlwt.Workbook(encoding='utf-8', style_compression=0)
sftotal_list = book2.add_sheet('total', cell_overwrite_ok=True)
h = 1
h_sumaary=1
#固定0
def defo(gg,listname):
    type_name = ['c', 'cp', 'd', 'e', 'f', 'h', 'l', 'lp', 'm', 'n', 'o', 'pc', 'pe', 'pf', 'ph', 'pm', 'pr', 'ps',
                 'pt', 'r', 's', 'su', 't']
    for defo1 in type_name:
        listname.write(type_name.index(defo1)+1,2 * (gg + 1) - 1,defo1)
        listname.write(type_name.index(defo1)+1, 2 * (gg + 1), 0)
def sumarry(h,sf,gg,times):
    sftotal_list.write(times+26*(h-1), 2+gg, sf)
# print(data)
# print(data01)
# print(data03)
def pllot(pre, nums,h):
    for gg in range(nums):
        index = []
        index_types = []
        gene_name = []
        for ind, num in enumerate(pre):  # 前面是位置，后面是值
            if num == gg:
                index.append(ind)
        # lambda1 = [0.05, 0.1, 0.2, 0.5, 0.6]
        # print(gg,index)
        for ming in index:
            gene_name.append(data04.columns[ming])
        for type in index:
            index_types.append(inddd[type])
        dict_num=all_list(index_types)
        defo(gg,genename_list)
        defo(gg, genenamesf_list)
        for hhh, a in enumerate(dict_num):
            type_name=['c','cp','d','e','f','h','l','lp','m','n','o','pc','pe','pf','ph','pm','pr','ps','pt','r','s','su','t']#可以改进
            type_number=[71,39,141,923,116,223,11,44,42,0,457,42,383,58,9,202,162,37,250,232,45,71,322]
            #print(len(type_name),len(type_number))
            for hhhh in type_name :
                if a==hhhh:
                    type_location=type_name.index(hhhh)
                    genename_list.write(type_location+1, 2 * (gg + 1) - 1, a)
                    genename_list.write(type_location+1, 2 * (gg + 1), dict_num[a])
                    sf = stats.hypergeom.sf(dict_num[a]-1, 3880, type_number[type_location], len(gene_name))
                    genenamesf_list.write(type_location+1, 2 * (gg + 1) , sf)
                    sumarry(h_sumaary,sf,gg,type_location+1)
        genenamesf_list.write(26, 2 * (gg + 1) - 1, gg)
        genenamesf_list.write(26, 2 * (gg + 1), len(gene_name))
        for hhh, a in enumerate(gene_name):
            genename_list.write(hhh + 27, 2 * (gg + 1) - 1, a)
        genename_list.write(26, 2 * (gg + 1) - 1, gg)
        genename_list.write(26,2 * (gg + 1),len(gene_name))
        for hhh, a in enumerate(index_types):
            genename_list.write(hhh + 27, 2 * (gg + 1), a)
        # for hhh, a in enumerate(index):无队列版本
        #   genename_list.write(hhh+2,2*nums+10+gg,a)
        # genename_list.write(1, 2*nums+10+gg, gg)
def all_list(list1):

    result = {}

    for i in set(list1):
        #print(i)

        result[i]=list1.count(i)

    return result

for i in α:
    h += 1
    datasum = add(data, data01, i)
    # datasum=data
    SC_list = []
    ARI_list = []
    ami_lsit = []
    CHI_list = []
    Vmeasure_list = []
    for n in range(2, 10,1):
        h_sumaary+=1
        model = AgglomerativeClustering(n_clusters=n, distance_threshold=None, linkage='average',
                                        compute_distances=True)
        book1 = xlwt.Workbook(encoding='utf-8', style_compression=0)
        genename_list = book1.add_sheet('genename', cell_overwrite_ok=True)
        genenamesf_list=book1.add_sheet('genenamesf', cell_overwrite_ok=True)
        pre = model.fit_predict(datasum)
        pllot(pre, n,h)  # 胡萝卜色

        savePath = f'230418 M63  {i} genename{n} enrich.xls'

        book1.save(savePath)
        #model.fit(datasum)
        SC = silhouette_score(datasum, pre)
        SC_list.append(SC)
        CHI = metrics.calinski_harabasz_score(datasum, pre)
        CHI_list.append(CHI)
        ARI = metrics.adjusted_rand_score(hh, pre)
        ARI_list.append(ARI)
        AMI = metrics.adjusted_mutual_info_score(hh, pre)
        ami_lsit.append(AMI)
        Vmeasure = metrics.v_measure_score(hh, pre)
        Vmeasure_list.append(Vmeasure)

    for gg, a in enumerate(SC_list):
        sheetSC_list.write(gg + 2, h, a)
        sheetSC_list.write(gg + 2, 1, n)
        #sheetSC_list.write(1, h, np.float(i))

    # sheetSC_list.write(1,h,i)

    for gg, a in enumerate(ARI_list):
        sheetARI_list.write(gg + 2, h, a)
    # sheetARI_list.write(1, h, i)
    for gg, a in enumerate(ami_lsit):
        sheetami_lsit.write(gg + 2, h, a)
    # sheetami_lsit.write(1, h, i)
    for gg, a in enumerate(CHI_list):
        sheetCHI_list.write(gg + 2, h, a)
    # sheetCHI_list.write(1, h, i)
    for gg, a in enumerate(Vmeasure_list):
        sheetVmeasure_list.write(gg + 2, h, a)
    # sheetVmeasure_list.write(1, h, i)
    # for gg, a in enumerate(pre):
    #       sheetpre.write(gg + 1, h, a)

savePath = r'SC.xls'
book.save(savePath)
savePath2 = r'genecategory_enrich.xls'
book2.save(savePath2)

# print(datasum)
