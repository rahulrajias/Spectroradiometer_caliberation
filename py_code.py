import os
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from string import ascii_letters
import math
import random
import pickle
import codecs
import random

folder_folders = os.walk("/home/alone/Documents/Spectroradiometer_caliberation/find_straight_line")
folder_list = []
folder_names = []
for root, dirs, files in os.walk("/home/alone/Documents/Spectroradiometer_caliberation/find_straight_line", topdown=False):
    for name in dirs:
        if not os.path.isfile(os.path.join(root, name)):
            folder_list.append(os.path.join(root, name))
            folder_names.append(name)
            print (os.path.join(root, name))
# print(folder_list)
print(folder_names)

all_data_dict = {}
for k in range(len(folder_list)):
    all_data = pd.DataFrame(columns=["Lambda"])
    file_list = os.listdir(folder_list[k])
    for j in range(len(file_list)):
        raw_data = open(os.path.join(folder_list[k],file_list[j]), "r")
        f = raw_data.readlines()
        usable_part = f[78:459]
        usable_part = [i.split("  ") for i in usable_part]
        data = pd.DataFrame(usable_part)
        for index,rows in data.iterrows():
            re_pattern = r"(.*)\n"
            data.set_value(index, 2, re.search(re_pattern, rows[2]).group(1))
        data.columns=["Lambda","target","ref"]
        data.ref=pd.to_numeric(data.ref)
        data.target=pd.to_numeric(data.target)
        Reflectance=(data.target)/(data.ref)
        data=data.drop("ref",1)
        data=data.drop("target",1)
        if all_data["Lambda"].empty:
            all_data["Lambda"] = data["Lambda"]
        all_data["R"+str(j+1)]=Reflectance
    all_data_dict [folder_names[k]] = all_data

print("All_data_dict is a dictionary where key is folder name and stored values are dataFrame consists of reflectance values of that folder ")

pure=all_data_dict["pure_part"]
print(pure.head())
plt.plot(pure.Lambda,pure.R1,color='g',linewidth=1)
ax=plt.gca()
# print(ax)
ax.set_ylim([0,1.2])
ax.set_xlim([400.35,998.65])
plt.tight_layout()
plt.xticks(np.arange(400.35, 998.65,16.4))
plt.show()
# plt.show()
