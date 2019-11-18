

'''
Make geotiffs from LVIS
'''

from pyproj import Proj, transform # package for reprojecting data
from osgeo import gdal             # pacage for handling geotiff data
import numpy as np



#####################################

def writeTiff(data,lon,lat,res,epsg=3857,filename="lvis_image.tif"):
  '''
  Make a geotiff from an array of points
  '''

  # reproject data to be in metres
  inProj=Proj(init="epsg:4326")
  outProj=Proj(init="epsg:"+str(epsg))
  x,y=transform(inProj,outProj,lon,lat)

  # determine bounds
  minX=np.min(x)
  maxX=np.max(x)
  minY=np.min(y)
  maxY=np.max(y)

  # determine image size
  nX=int((maxX-minX)/res+1)
  nY=int((maxY-minY)/res+1)

  # pack in to array
  imageArr=np.full((nY,nX),-999.0)
  xInds=np.array((x-minX)/res,dtype=int)
  yInds=np.array((y-minY)/res,dtype=int)
  imageArr[yInds,xInds]=data

  # set geolocation information (note geotiffs count down from top edge in Y)
  geotransform = (minX, res, 0, maxY, 0, -res)

  # load data in to geotiff object
  dst_ds = gdal.GetDriverByName('GTiff').Create(filename, nY, nX, 1, gdal.GDT_Float32)

  dst_ds.SetGeoTransform(geotransform)    # specify coords
  srs = osr.SpatialReference()            # establish encoding
  srs.ImportFromEPSG(epsg)                # WGS84 lat/long
  dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
  dst_ds.GetRasterBand(1).WriteArray(imageArr)  # write image to the raster
  dst_ds.FlushCache()                     # write to disk
  dst_ds = None

  print("Image written to",filename)
  return

