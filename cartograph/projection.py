import numpy as np

def mercator(lat, lon):
    r = 6371
    x = r*np.deg2rad(lon)
    y = r*np.log(np.tan(np.pi/4 + np.deg2rad(lat)/2))
    return x, y

def inverse_mercator(x, y):
    r = 6371
    lon = np.rad2deg(x/r)
    lat = np.rad2deg(2 * np.arctan(np.exp(y/r)) - np.pi/2)
    return lat, lon

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = np.deg2rad(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - np.log(np.tan(lat_rad) + (1 / np.cos(lat_rad))) / np.pi) / 2.0 * n)
    return xtile, ytile

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = np.arctan(np.sinh(np.pi * (1 - 2 * ytile / n)))
    lat_deg = np.rad2deg(lat_rad)
    return lat_deg, lon_deg
