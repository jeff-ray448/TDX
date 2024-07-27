from tdx_proxy import TDXProxy

proxy = TDXProxy(app_id="", app_key="")


def search_city(str):
    result = proxy.get(f'/v2/Road/Traffic/CCTV/City/{str}')
    print(result.content)

search_city("Taichung")
