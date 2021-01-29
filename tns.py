#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on December 2020

Developed and tested on:

- Linux 18.04 LTS
- Windows 10
- Python 3.7 (Spyder)

@author: Nikola Knezevic ASTRO DATA
"""

import os
import requests
import json
from collections import OrderedDict
import pandas as pd

###########################################################################################
####################################### PARAMETERS ########################################

TNS="www.wis-tns.org"
#TNS="sandbox.wis-tns.org"
url_tns_api="https://"+TNS+"/api/get"

# API key for Bot
api_key="e51ca292d25dffd9504b3f496dc755b80a864e40"
# list that represents json file for search obj
search_obj=[("ra",""), ("dec",""), ("radius",""), ("units",""), ("objname",""), 
            ("objname_exact_match",0), ("internal_name",""), 
            ("internal_name_exact_match",0), ("objid",""), ("public_timestamp","")]
# list that represents json file for get obj
get_obj=[("objname",""), ("objid",""), ("photometry","0"), ("spectra","1")]

# current working directory
cwd=os.getcwd()
# directory for downloaded files
download_dir=os.path.join(cwd,'downloaded_files')

###########################################################################################
###########################################################################################


###########################################################################################
######################################## FUNCTIONS ########################################

# function for changing data to json format
def format_to_json(source):
    # change data to json format and return
    parsed=json.loads(source,object_pairs_hook=OrderedDict)
    #result=json.dumps(parsed,indent=4)
    return parsed

# function for search obj
def search(url,json_list):
  try:
    # url for search obj
    search_url=url+'/search'
    # change json_list to json format
    json_file=OrderedDict(json_list)
    # construct the list of (key,value) pairs
    search_data=[('api_key',(None, api_key)),('data',(None,json.dumps(json_file)))]
    # search obj using request module
    response=requests.post(search_url, files=search_data)
    # return response
    return response
  except Exception as e:
    return [None,'Error message : \n'+str(e)]

# function for get obj
def get(url,json_list):
  try:
    # url for get obj
    get_url=url+'/object'
    # change json_list to json format
    json_file=OrderedDict(json_list)
    # construct the list of (key,value) pairs
    get_data=[('api_key',(None, api_key)),('data',(None,json.dumps(json_file)))]
    # get obj using request module
    response=requests.post(get_url, files=get_data)
    # return response
    return response
  except Exception as e:
    return [None,'Error message : \n'+str(e)]

# function for downloading file
def get_file(url):
  try:
    # take filename
    filename=os.path.basename(url)
    # downloading file using request module
    response=requests.post(url, files=[('api_key',(None, api_key))],stream=True)
    # saving file
    path=os.path.join(download_dir,filename)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response:
                f.write(chunk)
        print ('File : '+filename+' is successfully downloaded.')
    else:
        print ('File : '+filename+' was not downloaded.')
        print ('Please check what went wrong.')
  except Exception as e:
    print ('Error message : \n'+str(e))



def makedf(jsont,keys):
    dictt = {}
    for key in keys:
        if key == 'discmagSURVfilter':
            dictt[key] = [jsont['discmagfilter']['family']+'-'+jsont['discmagfilter']['name']]
        elif key == 'discovery_data_source':
            dictt[key] = [jsont['discovery_data_source']['group_name']]
        elif key == 'brightmag':
            mags = []
            for phot in jsont['photometry']:
                try:
                    if phot['flux_unit']['name'] == 'ABMag':
                        if float(phot['fluxerr'])<.4:
                            mags.append(float(phot['flux']))
                except:
                    pass #nofluxerr
            try:
                dictt[key] = [min(mags)]
            except:
                print('empty photometry')
                dictt[key] = [99]

        else:
            dictt[key] = [jsont[key]]
    df = pd.DataFrame.from_dict(dictt)
    return df

###########################################################################################
###########################################################################################




'''
    "reporter": "ALeRCE",
    "reporterid": 66140,
    "source": "bot",
    "discoverymag": 19.358,
    "discmagfilter": {
        "id": 110,
        "name": "g",
        "family": "ZTF"
    },
    "reporting_group": {
        "groupid": 74,
        "group_name": "ALeRCE"
    },
    "discovery_data_source": {
        "groupid": 48,
        "group_name": "ZTF"
    },
    "public": 1,
    "end_prop_period": null,
    "photometry": [

"photometry": [
        {
            "obsdate": "2021-01-12 13:07:10",
            "jd": 2459227.0466435,
            "flux": 20.0864,
            "fluxerr": 0.158485,
            "limflux": 20.4038,
            "flux_unit": {
                "id": 1,
                "name": "ABMag"
            },
            "instrument": {
                "id": 196,
                "name": "ZTF-Cam"
            },
            "telescope": {
                "id": 1,
                "name": "P48"
            },
            "filters": {
                "id": 110,
                "name": "g"
            },
            "exptime": 30,
            "observer": "Robot",
            "remarks": "Data provided by ZTF"
        },




'''

# EXAMPLE

# API key of your Bot:
api_key="e51ca292d25dffd9504b3f496dc755b80a864e40"

startyear = 2021
declim = 30
dfs = []
#force_confirmed_Ia = True

keys = ['objname','objid','redshift',"radeg","decdeg","radeg_err","decdeg_err",
        "hostname","host_redshift","internal_names","discoverer_internal_name","discoverydate",
        "reporter","discoverymag","discmagSURVfilter","discovery_data_source","brightmag"]

# search obj (here an example of cone search)
search_obj=[("ra","15:57:28"), ("dec","+30:03:39"), ("radius","1000"), ("units","degrees"), 
            ("objname",""), ("objname_exact_match",0), ("internal_name",""), 
            ("internal_name_exact_match",0), ("objid",""), ("public_timestamp","")]                   

response=search(url_tns_api,search_obj)
if None not in response:
    # Here we just display the full json data as the response
    json_data=format_to_json(response.text)
    #print (json_data["data"])
    for rdict in json_data["data"]['reply'][::-1]:
        get_obj=[("objname",rdict['objname']), ("objid",""), ("photometry","1"), ("spectra","1")]
        print(rdict['objname'])
        if str(rdict['objname'])[:4] >= str(startyear):
            response=get(url_tns_api,get_obj)
            json_data2=format_to_json(response.text)
            if not json_data2['data']['reply']['discoverydate'] is None:
                #if force_confirmed_Ia:
                isia = False
                if json_data2['data']['reply']["object_type"]['name'] == 'SN Ia': isia = True
                if float(json_data2['data']['reply']['decdeg'])>30: continue
                print(json.dumps(json_data2['data']['reply'],indent=4))
                df = makedf(json_data2['data']['reply'],keys)
                df['isIa'] = [isia]
                dfs.append(df)
                #dfs.append(pd.DataFrame.from_dict(json_data2['data']['reply']))
                #asdf
        #if len(dfs) > 100:
        #    break
else:
    print (response[1])

bigdf = pd.concat(dfs).set_index('objid')
print(bigdf)
bigdf.to_pickle("./tns.pkl")
