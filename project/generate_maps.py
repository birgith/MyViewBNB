import folium
import json
import pandas
from geo_loc import *
# to display maps in ipython notebook:
#from IPython.display import IFrame
import sys
sys.path.append('../app/templates/')


"""
Generates map for those listings that were only evaluated on the cover image (see below for general case)
"""
def maps_cover(img_list, df, loc_string, zoom, city):

	### Using Google's geocoding api to get coordinates:
	loc = geo(loc_string)
	Lat = loc['lat']
	Lon = loc['lon']
	
	if city == 'Paris':
		avr_price = 111

	bmap = folium.Map(
		location=[Lat,Lon],
		zoom_start=zoom,
	)

	for i in range(len(img_list)):
		if df['Price'][i] >= avr_price:
				bmap.circle_marker(
				location=[df['Lat'][i], df['Lon'][i]],
				popup='<img src={url} width=300 height=300 <br> {text} <br> <a target="_blank" href={link}>Go to airbnb</a>'.format(url=img_list[i], text=str(int(df['Price'][i])) + '$', link = df['Url'][i]),
				fill_color='red',
				line_color='red',
				radius=50,
			)
		else:
				bmap.circle_marker(
				location=[df['Lat'][i], df['Lon'][i]],
				popup='<img src={url} width=300 height=300 <br> {text} <br> <a target="_blank" href={link}>Go to airbnb</a>'.format(url=img_list[i], text=str(int(df['Price'][i])) + '$', link = df['Url'][i]),
				fill_color='blue',
				line_color='blue',
				radius=50,
			)
	
	
	bmap.create_map(path='../app/templates/map_airbnb.html')
	### To display in ipython notebook:
	#IFrame('mapa_notre_view.html', 700, 450)
	
##########################################################################################
########## Map created from dictionary after image recognition
##########################################################################################

"""
General case: This map version works with the airbnb final_list that evaluates max probability for images per listing
"""

#loc = geo("Eiffel Tower, Paris")
#Lat = 48.8572
#Lon = 2.2884813


def dict_map(final_dict, df, loc_string, zoom):
	
	### Using Google's geocoding api to get coordinates:
	loc = geo(loc_string)
	Lat = loc['lat']
	Lon = loc['lon']
	
	#SF:
	#Lat = 37.7833 
	#Lon = -122.4183333 
	
	print final_dict
	print len(final_dict)
	avr_price = 180
	bmap = folium.Map(
		location=[Lat,Lon],
		zoom_start=zoom, 
		)
	
	for key in final_dict: 
		temp_out = df[(df.ListingID == key)]
		price = int(temp_out.Price.values[0])
		if price >= 180:
			bmap.circle_marker(
				location=[float(temp_out.Lat), float(temp_out.Lon)],
				popup='<img src={url} width=300 height=300 <br> {text} <br> <a target="_blank" href={link}>Go to airbnb</a>'.format(url=final_dict[key], text=str(int(temp_out.Price.values[0])) + '$', link = temp_out.Url.values[0]),
				fill_color='red',
				line_color='red',
				radius=200,
				)
		else:
			bmap.circle_marker(
				location=[float(temp_out.Lat), float(temp_out.Lon)],
				popup='<img src={url} width=300 height=300 <br> {text} <br> <a target="_blank" href={link}>Go to airbnb</a>'.format(url=final_dict[key], text=str(int(temp_out.Price.values[0])) + '$', link = temp_out.Url.values[0]),
				fill_color='blue',
				line_color='blue',
				radius=200,
				)
	bmap.create_map(path='../app/templates/map_airbnbsf.html')
    #return IFrame('testw.html', 700, 450)






