from pylab import *
import os
import numpy as np
import pandas as pd
import caffe

"""
This file was created by Melody Wolk and modified by Birgit Hausmann. 
Image recognition was performed at separate computer with higher computing power.
"""

path_to_caffe='/home/mwakanosya/caffe/'

model_file = path_to_caffe + 'models/Birgit/placesCNN/places205CNN_deploy.prototxt'
pretrained = path_to_caffe + 'models/Birgit/placesCNN/places205CNN_iter_300000.caffemodel'
mean_file = path_to_caffe + 'python/caffe/imagenet/ilsvrc_2012_mean.npy'

#style=['Detailed','Pastel','Melancholy','Noir','HDR','Vintage','Long Exposure','Horror','Sunny','Bright','Hazy','Bokeh','Serene','Texture','Ethereal', 'Macro','Depth of Field', 'Geometric Composition', 'Minimal','Romantic']


net = caffe.Classifier(model_file, pretrained,
                       mean=np.load(mean_file),
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=[256, 256])
net.set_phase_test()
net.set_mode_gpu()

print "Loaded network!"
predict_style=[] 
directory = '/home/mwakanosya/Desktop/Birgit/images/airbnb_dicts/paris_view_view/'

imgs = [x for x in sort(os.listdir(directory)) if '.jpg' in x]
print imgs[0:5]


name=[]
style1=[]
style2=[]
style3=[]
style4=[]
style5=[]
sval1=[]
sval2=[]
sval3=[]
sval4=[]
sval5=[]

for i,f in enumerate(imgs):
    print "%d out of %d" % (i,len(imgs))
    input_image = caffe.io.load_image(directory+f)
    prediction = net.predict([input_image])[0]
    print(prediction)
    classif_array_top5 = prediction.argsort()[-5:][::-1]
    classif_array = prediction[classif_array_top5]
    style1.append(classif_array_top5[0]),
    sval1.append(classif_array[0])
    style2.append(classif_array_top5[1]),
    sval2.append(classif_array[1])
    style3.append(classif_array_top5[2]),
    sval3.append(classif_array[2])
    style4.append(classif_array_top5[3]),
    sval4.append(classif_array[3])
    style5.append(classif_array_top5[4]),
    sval5.append(classif_array[4]),
    name.append(f)
	

mydata = pd.DataFrame(style1, columns=['style1'])
mydata['style2']=style2
mydata['style3']=style3
mydata['style4']=style4
mydata['style5']=style5
mydata['sval1']=sval1
mydata['sval2']=sval2
mydata['sval3']=sval3
mydata['sval4']=sval4
mydata['sval5']=sval5
mydata['ID']=name

mydata.to_csv('205CNN_paris_view_view.csv')









