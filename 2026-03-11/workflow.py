import requests

from parsel import Selector
PDP_HEADER = {
"Host": "www.delhaize.be",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "https://www.delhaize.be/nl/shop/Koude-en-warme-dranken/Frisdrank/c/v2DRISOF?q=%3Arelevance&sort=relevance",
"Connection":"keep-alive",
#"Cookie":"""deviceSessionId=2a168c09-ea47-9d43-30ac-01b3260a0f3e; AWS=true; _abck=19BFF43EDE27D2A00E89EED0E7EE17AE~-1~YAAQBDdlX3ilkKCcAQAAEc3X1g9dt/h2w5MnvY7nMzVZnyfrYM2dNf676RTXZZTpRcJdUW5Il4GSLYftgw4famHpgytg/YV4shuHqbX1b7s8wNMXOq50c9Xf8LYRZHssK9hfjASkay9uK2cX5NeY7hckJG09u5m2zPl+cw1lW8Ral/QczmFoIw61pK1UytUyePPH36vqiKzJFifgCUPNj7ejRqKBVbbKxLk/BvJb/idm6Rk8E6zXjMgQqMmgmm1zmMPVuK9HBSSxTjIIDhUVbtx9QWYc4px6gg+/hcIm82j7y/DLNIwMe6QZyUJE3shDKu7NwmBwsa4w/NmZIhcHyWwivzTAJle8Kq49dq9L9/t2BEGoqV4hM0FI/rsLE9WEW6pwdjCOqOVpkXdXEjzNdm3VN5xHwIaNMpHBnvF7kBBvKT74LhOfSzRhYQVPKcv30eHbwOWRbcMfIg2S87fBQpTRonYDrGMSZ2+XmC6tDX38xUO0cLZmjXB/7jbIPA==~-1~-1~-1~-1~-1; ak_bmsc=C5164CAC2DCE2A979FE96EF5D8C5C0F1~000000000000000000000000000000~YAAQBDdlX+GmkKCcAQAAN+DX1h/oJou2byCcbMwmLBgvj3zu/TR11glhUVWmaH+fQawKUNAC95HFcGcUPAet1UbmUlsfw2BZfeV1NfdFVpvHVVS1Fd9PtZgyU7Lzkx/s/9e5EJmNiEm5Eu/CQxeZXk3YvmSckY9ntnyEnhAeP3YwY6TM5fUIA8M6pBek4OpNBeCsyc1EEsXhi2/hMB9likbGxq4KwxPrji201q87nDg87ApfnTn9/3x07GNVctVFoARwO+7qHkNV3E0NoanMirNuJ68X5we0AT2wiWfgdo1EIVSV5dmXEDhsGQpds5VKEx+utBL8SYrKaF7mI4+5Y3WVXXnI1PV0lFqcvuYpKU7wNekPMKGwO0tc3GPpi+P3ropS5YQS+TqZHxyPcrZIuDg6Y28J58QZaE2gtZYz/7Iv5kZTdMr5W6UMfi+v0Wbu0VdUQ9x9fg==; bm_sz=BECF713CBC068A6D3EB50C49F87398EE~YAAQDPsQYFYGPLecAQAAl3si1x/NNdDW7ozY54l0wXARXfY2+xkHjaDAE9mKTy9eoIVvr2pteQVrTpsQrK5ivfDc4rKsMbXknqSoOZ7ePXjW4RFDT5IEm2xsaragSDNL3j/VsySBF7IdpnQi+XTkLZflxm3pFY4e0v/d8g2WjIjcqKkiiP8SHjhUmm+fI5aiu0up/8YQAyUED8qfcAo5XzDz67NxeRNdc7pvjR9V9XVDLNcr7Hw0TlH7J2QMAvVI4QTeHooni7QgBOKhmua30+TYN2OTC1Vzv70B8sEnn8e4vOn/cSeVu1bzxo6GLpjhsIfT0Qca/JVLjjQiCcn3LVa5a9k6fOG+JlYUb8MurTnGM1w5S7QHfCO/hHBVcbk4kGMDJKPo22RIIsTOlm3/j3mgMlyT7/TK1MwI5wrwkdHx/5XTYwz8a0i+KHAEtrc/XJ9ZFHQU2/lGUFWRjoqUHMR8Gt9xjZk6sxGS3Ug3Pe+jYcfyUkAqtTfZL39jLkRVBopdr+wIHq2ZMSMPmaRszyHQgMFdYeuHwR9bU/pSxA==~3552324~4338246; dtCookie=v_4_srv_8_sn_7AD5A890C6FA3F8A98B7EF6B661081FB_perc_100000_ol_0_mul_1_app-3Ab0bf94df3db180f6_0; rxVisitor=1773130992774SBB0ESIOD9ELEFH2O9UBONF8ISGIGCLD; dtPC=-12978$130992773_642h1vMLKKKIFFFKFOMRMUIFRKPCAOVRFIHAIU-0e0; rxvt=1773132795401|1773130992775; dtSa=-; bm_sv=7FD00704BE1050A8D87F64D17CC72101~YAAQDPsQYI4MPLecAQAAGrMi1x/C7Yk6IRq+QFgyzrwMKiYrKM5mWPWVEiC7KLgaC0J846U5kvZpc1OVank9UWr7+bV6sAOvm9u47Q4d+fbIQbruaG5ATPPnWHMN6PbBUpJg7UgFs5QTSPkCtAi1Go4GJDgXEdG+u9WtIj7f7ZPiyRpg8PfM/tk8WmLQH0RovGadjDrFkq/t4LXx5J/+ENxKh21Bzm08wg38l5sSU9E7pQIhDkfAGw8nZwkFXPa2jWVm~1; liquidFeeThreshold=0; AWSALB=dgo0GmlhvWazVmGUmpkmEq7GDKxtsnZPteqKZ+Q70JGpZc5YoMF4hoz4xwfs93/Lj7XwTDL7kq2AhCBwLPxU8/fkLwU4iVcpmxUNddFIIK2ARx1uB0uv2msrQmqu; AWSALBCORS=dgo0GmlhvWazVmGUmpkmEq7GDKxtsnZPteqKZ+Q70JGpZc5YoMF4hoz4xwfs93/Lj7XwTDL7kq2AhCBwLPxU8/fkLwU4iVcpmxUNddFIIK2ARx1uB0uv2msrQmqu; groceryCookieLang=nl; VersionedCookieConsent=v%3A2%2Cessential%3A1%2Canalytics%3A1%2Csocial%3A1%2Cperso_cont_ads%3A1%2Cpartner_ads%3A1%2Cads_external%3A1; mbox=PC#ef854cbbd03e406c9dadd0ea69f2af03.37_0#1836380694|session#0ef2c7abe983467f8a2c285b6451c490#1773137755; v_cust=0; at_check=true; s_pls=not%20logged; AMCV_2A6E210654E74B040A4C98A7%40AdobeOrg=179643557%7CMCMID%7C27901059950321160403796148955145464818%7CMCAID%7CNONE%7CvVersion%7C5.5.0%7CMCIDTS%7C20523; s_fid=24643EBF4D784131-2083A76703CA002F; s_sq=%5B%5BB%5D%5D; s_cc=true; BCSessionID=b636acf7-6813-4d07-9a74-c29ecca6eabe; _gcl_au=1.1.1646814762.1773131016; kndctr_2A6E210654E74B040A4C98A7_AdobeOrg_identity=CiYyNzkwMTA1OTk1MDMyMTE2MDQwMzc5NjE0ODk1NTE0NTQ2NDgxOFIRCNfW4LbNMxgBKgRJUkwxMAPwAdfW4LbNMw==; _cs_c=1; _cs_id=43c45347-5456-a06a-9cba-759da8d307ed.1773131017.1.1773135896.1773131017.1.1807295017935.1.x; _cs_s=38.0.U.9.1773137774690; _fbp=fb.1.1773131021424.984711941216810683; _pin_unauth=dWlkPVlXSTVObUZqWTJZdE16RmxPQzAwTkRreUxXRTBNbVl0TXpOaU56WTVaVEF3WlRRNA; s_ppn=market%3Acold%20and%20hot%20drinks%3Asodas%3Aother%20sparkling%20sodas%3Aproduct%20details; gpv_loginStatus=not%20logged; _cs_mk=0.06364409714374653_1773135471650; kndctr_2A6E210654E74B040A4C98A7_AdobeOrg_cluster=irl1""",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User":"?1",
"Priority": "u=0, i",
"TE": "trailers",
}

API_HEADER = {
"Host": "www.delhaize.be",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
"Accept": "*/*",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Referer": "https://www.delhaize.be/nl/shop/Waters-Softdrinks-and-Fruitsap/Frisdrank/c/v2DRISOF",
"content-type": "application/json",
"apollographql-client-name": "be-dll-web-stores",
"apollographql-client-version": "e23db29dffd65300a7defc27c5ee37a4a7c75c87",
"x-apollo-operation-name": "GetCategoryProductSearch",
"x-apollo-operation-id": "841bc048e809cf7f460d0473995516d39464c46b70952bd8b26235f881f571b5",
"x-default-gql-refresh-token-disabled": "true",
"x-dtpc":"8$133198756_784h14vWKFTRODCCQWUFFHBUVARKMEDOPPOAPJC-0e0",
"tracestate":"4888dfe3-c11c5b27@dtr=1;0b01067f40b3afee;1;b0bf94df3db180f6;1773130992774SBB0ESIOD9ELEFH2O9UBONF8ISGIGCLD;EKGUUCMFPGMDKDRWWVBUKJAMNCRUHWME-0",
"traceparent":"00-4a19e37aeb1ccfbd1aad38c25604cdc4-0b01067f40b3afee-01",
"Connection": "keep-alive",
#"Cookie":"""deviceSessionId=2a168c09-ea47-9d43-30ac-01b3260a0f3e; AWS=true; _abck=19BFF43EDE27D2A00E89EED0E7EE17AE~-1~YAAQBDdlX3ilkKCcAQAAEc3X1g9dt/h2w5MnvY7nMzVZnyfrYM2dNf676RTXZZTpRcJdUW5Il4GSLYftgw4famHpgytg/YV4shuHqbX1b7s8wNMXOq50c9Xf8LYRZHssK9hfjASkay9uK2cX5NeY7hckJG09u5m2zPl+cw1lW8Ral/QczmFoIw61pK1UytUyePPH36vqiKzJFifgCUPNj7ejRqKBVbbKxLk/BvJb/idm6Rk8E6zXjMgQqMmgmm1zmMPVuK9HBSSxTjIIDhUVbtx9QWYc4px6gg+/hcIm82j7y/DLNIwMe6QZyUJE3shDKu7NwmBwsa4w/NmZIhcHyWwivzTAJle8Kq49dq9L9/t2BEGoqV4hM0FI/rsLE9WEW6pwdjCOqOVpkXdXEjzNdm3VN5xHwIaNMpHBnvF7kBBvKT74LhOfSzRhYQVPKcv30eHbwOWRbcMfIg2S87fBQpTRonYDrGMSZ2+XmC6tDX38xUO0cLZmjXB/7jbIPA==~-1~-1~-1~-1~-1; ak_bmsc=C5164CAC2DCE2A979FE96EF5D8C5C0F1~000000000000000000000000000000~YAAQBDdlX+GmkKCcAQAAN+DX1h/oJou2byCcbMwmLBgvj3zu/TR11glhUVWmaH+fQawKUNAC95HFcGcUPAet1UbmUlsfw2BZfeV1NfdFVpvHVVS1Fd9PtZgyU7Lzkx/s/9e5EJmNiEm5Eu/CQxeZXk3YvmSckY9ntnyEnhAeP3YwY6TM5fUIA8M6pBek4OpNBeCsyc1EEsXhi2/hMB9likbGxq4KwxPrji201q87nDg87ApfnTn9/3x07GNVctVFoARwO+7qHkNV3E0NoanMirNuJ68X5we0AT2wiWfgdo1EIVSV5dmXEDhsGQpds5VKEx+utBL8SYrKaF7mI4+5Y3WVXXnI1PV0lFqcvuYpKU7wNekPMKGwO0tc3GPpi+P3ropS5YQS+TqZHxyPcrZIuDg6Y28J58QZaE2gtZYz/7Iv5kZTdMr5W6UMfi+v0Wbu0VdUQ9x9fg==; bm_sz=BECF713CBC068A6D3EB50C49F87398EE~YAAQD/sQYAxMUqOcAQAA6W751h+28YxTesPUj812tEaKp2y2qrl2M4jtwBmLCmCeNbMXjv9i9whV13/kUd8LRsgQQjYKi8pVKYiDOa98DcuTOSZawfNCZu8VHMeSZPeB7GHPe0NO3nIvFoPX7AzL2Ux3Zn1pJjFZI/ZXfDFHypheF+cCG/vLpyRU03WwsFMVP9GdoFCCPgRNakrJE5ClJMapLcAoBBUispVq5B05OI8DgCBLP6z6lAJmQcrJzbOifWqxW004Mf/LGS6uBL61hv20sOJuHKO2osFj38MkuiM+M8cSxXjyg80ga8lCcPj3z221pgyOiYetpxGkbjmNcLojYvvkH84UIA3ikILRMwOSVYZWe5Aki1+luhSKzaeUM8BpeqinRHdSPt1t93fpjZfGOahjHeBEMuI3UnEfTMaOqfy/+AD2Yec+9FDS0vD5P9qJw+jfTHKIBLk6FIF7g/NzKH4In2YnnDgma/K0bFK2xbsQcmRt2QQHeF00vg+d0b+RzZn5k1mEmCsVHPHcdGaIcQD3svXTQYruhH7Z~3552324~4338246; dtCookie=v_4_srv_8_sn_7AD5A890C6FA3F8A98B7EF6B661081FB_perc_100000_ol_0_mul_1_app-3Ab0bf94df3db180f6_0; rxVisitor=1773130992774SBB0ESIOD9ELEFH2O9UBONF8ISGIGCLD; dtPC=-12978$130992773_642h1vMLKKKIFFFKFOMRMUIFRKPCAOVRFIHAIU-0e0; rxvt=1773132795401|1773130992775; dtSa=-; bm_sv=7FD00704BE1050A8D87F64D17CC72101~YAAQD/sQYJxMUqOcAQAAQnf51h/DrlKKoYIQVDHAF/Xnwhyf0NH2N0nb9MRYR4CbcqHpTrCK3LBGcz9Wcri2BSjuNRBMG5GrJYm4wiKJWIqRDVJBz7WZmYzU+i6K2aP2rYX9aK+epe1CN0BxIkVAexPNWBhUhnVi8HuMFnrCKB+NQHicw3Fu8pEmzR4oylF5dZk4q+6wRLIVmSbySvXTIClDAeAkZeYjc6URBPKQJrc6HTjv/pAKw6B7XNPRR/bQfFkj~1; liquidFeeThreshold=0; AWSALB=JhOLgFS/W+5DOwT9a0JGjeDiCVCMLnBAkIxixjw5oaSmhRujo6lmgz1qGiQcwpczGGJoUbwROlGPBy58xKrUSY0r6hBbi1+B5hDbanXI+xxCSGJf5CWkd7eNKLgR; AWSALBCORS=JhOLgFS/W+5DOwT9a0JGjeDiCVCMLnBAkIxixjw5oaSmhRujo6lmgz1qGiQcwpczGGJoUbwROlGPBy58xKrUSY0r6hBbi1+B5hDbanXI+xxCSGJf5CWkd7eNKLgR; groceryCookieLang=nl; VersionedCookieConsent=v%3A2%2Cessential%3A1%2Canalytics%3A1%2Csocial%3A1%2Cperso_cont_ads%3A1%2Cpartner_ads%3A1%2Cads_external%3A1; mbox=session#ef854cbbd03e406c9dadd0ea69f2af03#1773135063|PC#ef854cbbd03e406c9dadd0ea69f2af03.37_0#1836377788; v_cust=0; at_check=true; s_pls=not%20logged; AMCV_2A6E210654E74B040A4C98A7%40AdobeOrg=179643557%7CMCMID%7C27901059950321160403796148955145464818%7CMCAID%7CNONE%7CvVersion%7C5.5.0%7CMCIDTS%7C20523; s_fid=24643EBF4D784131-2083A76703CA002F; s_ppn=market%3Akoude%20en%20warme%20dranken%3Afrisdrank%3Acategory; gpv_loginStatus=not%20logged; s_sq=%5B%5BB%5D%5D; s_cc=true; BCSessionID=b636acf7-6813-4d07-9a74-c29ecca6eabe; _gcl_au=1.1.1646814762.1773131016; kndctr_2A6E210654E74B040A4C98A7_AdobeOrg_identity=CiYyNzkwMTA1OTk1MDMyMTE2MDQwMzc5NjE0ODk1NTE0NTQ2NDgxOFIRCNfW4LbNMxgBKgRJUkwxMAPwAdfW4LbNMw==; kndctr_2A6E210654E74B040A4C98A7_AdobeOrg_cluster=irl1; _cs_c=1; _cs_id=43c45347-5456-a06a-9cba-759da8d307ed.1773131017.1.1773133140.1773131017.1.1807295017935.1.x; _cs_s=34.0.U.9.1773134974219; _fbp=fb.1.1773131021424.984711941216810683; _pin_unauth=dWlkPVlXSTVObUZqWTJZdE16RmxPQzAwTkRreUxXRTBNbVl0TXpOaU56WTVaVEF3WlRRNA; _cs_mk=0.41697145583602546_1773132859460""",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"Priority": "u=4",
"TE":"trailers",

}



url = "https://www.delhaize.be/nl/shop/Koude-en-warme-dranken/Frisdrank/Energiedrank/Zero-Sugar-Energiser/p/S2025042200851860099"



###### C R A W L E R ###############################

api = "https://www.delhaize.be/api/v1/"

variables = {
    "lang": "nl",
    "searchQuery": "",
    "category": "v2DRISOF",
    "pageNumber": 0,
    "pageSize": 20,
    "filterFlag": True,
    "fields": "PRODUCT_TILE",
    "plainChildCategories": True
}

extensions = {
    "persistedQuery": {
        "version": 1,
        "sha256Hash": "6207aa07553962b9956d475b63737d2b03b3eb7b7e6fa6ffbfc709f9894c5bdd"
    }
}

page = 0

while True:
    
    variables["pageNumber"] = page

    params = {
        "operationName": "GetCategoryProductSearch",
        "variables": json.dumps(variables),
        "extensions": json.dumps(extensions)
    }


    response = requests.get(api,headers=API_HEADER,params=params)
    print(response.status_code)
    res = response.json()
    data = res["categoryProductSearch"]
    products = data.get("products")
    if products:
        for pdp in products:
            link = pdp.get("url")
            id = pdp.get("code")
    

        page += 1
    else:
        break






################ P A R S E R #####################
    breadcrumb = sel.xpath('//div[@class="sc-45z6bh-1 fvXBHk"]/h3[contains(text(),"Special storage requirements")]/following-sibling::div/div//text()').extract()
    print(breadcrumb)