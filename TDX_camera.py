from tdx_proxy import TDXProxy

proxy = TDXProxy(app_id="b12406018-21578451-da0e-4d27", app_key="6201510b-79c8-49ad-8558-6fb9432620c0")


def search_city(str):
    result = proxy.get(f'/v2/Road/Traffic/CCTV/City/{str}')
    print(result.content)

search_city("Taichung")