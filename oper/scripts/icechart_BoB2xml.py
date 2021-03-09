import shapefile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point
from shapely.geometry import Polygon
import os
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as Polygon_patch
from mpl_toolkits.basemap import Basemap
import glob


import sys  # argv
import osgeo
from osgeo import osr
from operator import itemgetter


### ICE CHART FILENAMES
if (len(sys.argv) > 1):
    list_SIGRIDfilenames = list()
    list_SIGRIDfilenames.append(sys.argv[1])
else:
    list_SIGRIDfilenames = glob.glob('./FMI_Sigrid-*/FMI_baltic*pl_a.shp')

save_icetypes = True

list_SIGRIDfilenames.sort()

### BALTIC SEA, SET UP MAP AND DEFINE COLORS

m = Basemap(llcrnrlat=53.2,llcrnrlon=9.2,urcrnrlon=31,urcrnrlat=66.5, resolution='h',projection='tmerc',lon_0=25, lat_0=61.666667)

# ice_color = (255/255.0,255/255.0,255/255.0)
# edge_color = (0, 0, 0)
# land_color = (216/255.0,231/255.0,242/255.0)
# sea_color = (203/255.0,241/255.0,245/255.0)
# int_fontsize = 20
# size_of_figure = [5,5]


def month_string_from_filename(str_filename):
    str_filename = os.path.basename(str_filename)
    if (len(str_filename) < 13):
        return "NO_MONTH"
    int_month = int(str_filename[-13:-11])
    if int_month == 1:
        return "January"
    elif int_month == 2:
        return "February"
    elif int_month == 3:
        return "March"
    elif int_month == 4:
        return "April"
    elif int_month == 5:
        return "May"
    elif int_month == 6:
        return "June"
    elif int_month == 7:
        return "July"
    elif int_month == 8:
        return "August"
    elif int_month == 9:
        return "September"
    elif int_month == 10:
        return "October"
    elif int_month == 11:
        return "November"
    elif int_month == 12:
        return "December"
    else:
        return "INVALID_MONTH"




### PARTY ON!
for str_filename in list_SIGRIDfilenames:

    print ("Now processing " + str_filename)

    if os.path.isfile(str_filename.replace('.shp', '.SPHysics.xml')):
        os.remove(str_filename.replace('.shp', '.SPHysics.xml'))

    sigrid = shapefile.Reader(str_filename)
    IC_polygons = sigrid.shapeRecords()
    N_polygons = len(IC_polygons)

    print ("Found ",N_polygons," polygons")

    source = osr.SpatialReference()  # Based on: https://gis.stackexchange.com/questions/295962/splitting-a-shapefile-based-off-coordinates-in-python-using-osgeo-ogr-or-pyshp
    source.ImportFromEPSGA(4326)     # GCS_WGS_1984
    target = osr.SpatialReference()  # HELP: https://spatialreference.org/ref/epsg/2079/
#    target.ImportFromEPSGA(2079)     # UTM zone 34N, https://spatialreference.org/ref/epsg/2079/
    target.ImportFromEPSG(25834)
    if (int(osgeo.__version__[0]) >= 3):    # This needed as https://github.com/OSGeo/gdal/issues/1546
        source.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)
        target.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)

    transform = osr.CoordinateTransformation(source,target)


    patches = list()
    map_patches = list()
    SA = list()
    icetypes = list() #set()
    icepolygons = list()

    for i in range(1,len(sigrid.fields)):     # List fields 
        print (i," : ",sigrid.fields[i])

    for j in np.arange(len(IC_polygons)):

        icechart_polygon = IC_polygons[j]
        P = Polygon(icechart_polygon.shape.points)

#JL        print (icechart_polygon.record)
        xmin, ymax, xmax, ymin = icechart_polygon.shape.bbox
        print ("X from ", xmin," to ",xmax,", Y from ",ymin," to ",ymax)
        xmin, ymin, zmin = transform.TransformPoint(xmin, ymin)
        xmax, ymax, zmax = transform.TransformPoint(xmax, ymax)
        print ("transformed X from ", xmin," to ",xmax,", Y from ",ymin," to ",ymax)

# gdalinfo landmask_BoB_100m.tiff
# Lower Left  (  319725.201, 6929895.990) ( 17d30'16.32"E, 62d27'22.81"N)
# Upper Right (  757325.201, 7328895.990) ( 26d40'13.95"E, 65d58'34.17"N)
        tgtxmin = 319725.201
        tgtxmax = 757325.201
        tgtymin = 6929895.990
        tgtymax = 7328895.990

        if (((tgtxmin < xmin < tgtxmax) or (tgtxmin < xmax < tgtxmax)) and
            ((tgtymin < ymin < tgtymax) or (tgtymin < ymax < tgtymax))):
            match = 1
        else:
            match = 0

        print (icechart_polygon.record[2:5], xmin, xmax, ymin, ymax)

        if icechart_polygon.record[2] == 'I' and match:     # If POLY_TYPE (record 2) is Ice, and in BoB
            print(icechart_polygon.record[2:5], end=" ")

            Px,Py = P.exterior.xy
            if len(Px) - len(np.unique(np.array(Px)+np.array(Py))) > 2:
                k = 1
                while np.logical_not(Px[k]*Py[k] == Px[0]*Py[0]):
                    k = k+1
                Px = Px[:k]
                Py = Py[:k]

            CT = icechart_polygon.record[3]     # Total concentration, 92 = 100% FAST ICE
            RN = icechart_polygon.record[13]    # Nature of topography feature
            RF = icechart_polygon.record[14]    # Frequency of topo feat. (eg RIDGE) per mile
            EM = icechart_polygon.record[15]    # Mean thickness level ice, cm
            EI = icechart_polygon.record[16]    # Ice thickness interval digits: MMMmmm (MAX, min)
            AM = icechart_polygon.record[17]    # Concentration of medium brash ice (1 - 2 m), 99 = no
            SM = icechart_polygon.record[18]    # Melt forms (not included?)

            # More on this in JCOMM-TR- ... pdf PAGE 31
            conc = int(CT)
            if (conc == 92):  # 92 means FAST ICE   (OR OPEN WATER)
                conc = 110
            if (conc == 98):  # Concentration 98 means open water (OR FAST ICE)
                conc = 0
            if (conc == 91):  # 91 means > 90 % concentration / Consolidated ice
                conc = 95     # Is this rounded up or down?

            conc = max(0, min(round(float(conc) / 10.0), 11))
            thic = max(0, min(round(float(EM) / 10.0), 9))

            CTnum = conc*10 + thic
            thic = 3    # Debug

            print ((CT, EM), end=" ")
            print ((CTnum, conc, thic))

            PFX = "                    "        # Prefix, indentation
            scale = 0.002                       # Map scaling

            if (conc == 11):
                mkvalue = 0     # Fast ice is first type

                with open(str_filename.replace('.shp', '.SPHysics.xml'), 'a+') as f:
                    print (PFX, "<setmkbound mk=\"10\" /> <!-- FAST ICE -->", file=f)
                    print (PFX, "<drawprism mask=\"0\">",  file=f)  # drawprism seems to fill better
                    for i in reversed(range(len(Px))):              # Reversed, to get filling right.
                        xtemp, ytemp, ztemp = transform.TransformPoint(Px[i], Py[i])
                        print (PFX, "    <point x=\"",(xtemp-tgtxmin)*scale,"\" y=\"0\" z=\"",(ytemp-tgtymin)*scale,"\" />",  file=f)
                    for i in reversed(range(len(Px))):
                        xtemp, ytemp, ztemp = transform.TransformPoint(Px[i], Py[i])
                        print (PFX, "    <point x=\"",(xtemp-tgtxmin)*scale,"\" y=\"2\" z=\"",(ytemp-tgtymin)*scale,"\" />",  file=f)
                    print (PFX, "</drawprism>",  file=f);

            else:               # Others in the order of appearance
                if ((conc, thic) not in icetypes):
                    icetypes.append((conc, thic))
                mkvalue=icetypes.index((conc,thic))

                #icetypes.add((CTnum, conc, thic))
                Mx, My = m(Px, Py)
                map_patches.append(Polygon_patch(list(zip(Mx,My))))
                SA.append(int(icechart_polygon.record[4]))

                with open(str_filename.replace('.shp', '.SPHysics.xml'), 'a+') as f:
                    print (PFX, "<setmkfluid mk=\"",mkvalue,"\" />", file=f)
                    print (PFX, "<drawprism mask=\"0\">",  file=f)  # drawprism seems to fill better
                    for i in reversed(range(len(Px))):              # Reversed, to get filling right.
                        xtemp, ytemp, ztemp = transform.TransformPoint(Px[i], Py[i])
                        print (PFX, "    <point x=\"",(xtemp-tgtxmin)*scale,"\" y=\"0\" z=\"",(ytemp-tgtymin)*scale,"\" />",  file=f)
                    for i in reversed(range(len(Px))):
                        xtemp, ytemp, ztemp = transform.TransformPoint(Px[i], Py[i])
                        print (PFX, "    <point x=\"",(xtemp-tgtxmin)*scale,"\" y=\"2\" z=\"",(ytemp-tgtymin)*scale,"\" />",  file=f)
                    print (PFX, "</drawprism>",  file=f);


    if save_icetypes:
        with open(str_filename.replace('.shp', '.icetypes.xml'), 'w') as f:
#            icetypes = sorted(icetypes, key=itemgetter(0), reverse=True)
            for type in icetypes:
                conc = type[0]
                thic = type[1]

                rhop = 1000 #conc*100
                visco = 12.0        # default 1.2
                tau_yield = conc    # default 0.0001

                if (conc == 11):
                    visco = 1200.0
                    tau_yield = 100000

                if (conc == 11):
                    mkvalue = 0
                else:   # in the order the types appear, except fast ice is first
                    mkvalue=icetypes.index((conc,thic))

                print (mkvalue, type)
                print (PFX, "<phase mkfluid=\"",mkvalue,"\">", file=f)
#                print ("% CT = ",type[3]," EM = ",type[4], file=f)
                print (PFX, "    <rhop value=\"",rhop,"\" />", file=f)
                print (PFX, "    <visco value=\"",visco,"\" />", file=f)
                print (PFX, "    <tau_yield value=\"",tau_yield,"\" />", file=f)
                print (PFX, "    <HBP_m value=\"100\" />", file=f)
                print (PFX, "    <HBP_n value=\"0.8\" comment=\"lt 1: shear thinning gt 1: shear thickening\" />", file=f)
                print (PFX, "    <phasetype value=\"0\" comment=\"Non-Newtonian=0 only option in v5.0\" />", file=f)
                print (PFX, "</phase>", file=f)

        with open('accfluids.txt', 'w') as f:
            # Print a comma-separated list of existing fluid indices
            print(','.join([str(i) for i in range(len(icetypes))]), file=f)
