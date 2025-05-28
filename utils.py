import os
import requests

def get_shopify_products():
    url = f"{os.getenv('SHOPIFY_STORE_URL')}/admin/api/2025-04/products.json"
    headers = {
        "X-Shopify-Access-Token": os.getenv("SHOPIFY_ACCESS_TOKEN"),
        "Content-Type": "application/json"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()["products"]

def extract_numeric_id(gid):
    if isinstance(gid, str) and gid.startswith("gid://"):
        return int(gid.split("/")[-1])
    return gid  # already numeric

def update_sku(product_id, variant_id, new_sku):
    extracted_variant_id = extract_numeric_id(variant_id)
    url = f"{os.getenv('SHOPIFY_STORE_URL')}/admin/api/2025-04/variants/{extracted_variant_id}.json"
    headers = {
        "X-Shopify-Access-Token": os.getenv("SHOPIFY_ACCESS_TOKEN"),
        "Content-Type": "application/json"
    }
    data = { "variant": { "id": extracted_variant_id, "sku": new_sku } }
    res = requests.put(url, json=data, headers=headers)
    res.raise_for_status()
    return res.json()