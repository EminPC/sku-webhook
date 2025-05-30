# server.py
from flask import Flask, request, jsonify
from utils import update_sku
from main import generate_sku
import json
with open("sku_config.json") as f:
    config = json.load(f)

app = Flask(__name__)

@app.route("/webhook/sku", methods=["POST"])
def sku_webhook():
    data = request.json
    product = data.get("product", data)
    variant = product["variants"][0]

    if variant.get("sku"):
        return jsonify({"status": "SKU vorhanden"}), 200

    new_sku = generate_sku(product, config["start_number"])
    update_sku(product["id"], variant["id"], new_sku)
    return jsonify({"status": "SKU gesetzt", "sku": new_sku}), 200

# Render startet automatisch mit `gunicorn server:app`