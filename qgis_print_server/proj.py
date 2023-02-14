from pyproj import Proj, transform


def reproject(lon,lat):
    inProj = Proj('epsg:4326')
    outProj = Proj('epsg:2100')

    x2,y2 = transform(inProj,outProj,x=lat,y=lon)

    return {
        "x": x2,
        "y": y2
    }