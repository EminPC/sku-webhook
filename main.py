import json
import os
from dotenv import load_dotenv
from utils import get_shopify_products, update_sku

load_dotenv()

with open("sku_config.json") as f:
    config = json.load(f)

def extract_field(product, field_name, mode):
    value = product.get(field_name, "")
    if not value:
        return ""
    if mode == "first_char":
        return value[0].upper()
    return value

def generate_sku(product, counter):
    parts = [config["prefix"]]
    for field in config["fields"]:
        part = extract_field(product, field["source"], field["mode"])
        parts.append(part)
    parts.append(str(counter))
    if config.get("suffix"):
        parts.append(config["suffix"])
    return config["separator"].join(parts)

def main():
    products = get_shopify_products()
    counter = config["start_number"]

    for product in products:
        variant = product["variants"][0]  # Nur erste Variante
        if config["apply_to"] == "missing_sku_only" and variant["sku"]:
            continue
        new_sku = generate_sku(product, counter)
        update_sku(product["id"], variant["id"], new_sku)
        print(f"SKU gesetzt für {product['title']}: {new_sku}")
        counter += 1

if __name__ == "__main__":
    main()