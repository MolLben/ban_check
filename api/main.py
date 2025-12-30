from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/bancheck', methods=['GET'])
def check_ban_status():
    uid = request.args.get('uid')
    if not uid or not uid.isdigit():
        return jsonify({"status": 400, "error": "Invalid UID"}), 400

    try:
        url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={uid}"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        data = res.json()

        if data.get("status") != "success":
            return jsonify({"status": 500, "error": "Garena API failed"}), 500

        is_banned = data["data"].get("is_banned", 0)
        period = data["data"].get("period", 0)

        return jsonify({
            "status": 200,
            "data": {
                "is_banned": is_banned,
                "period": period,
                "nickname": "UNKNOWN",
                "region": "UNKNOWN"
            }
        })

    except Exception as e:
        return jsonify({"status": 500, "error": str(e)}), 500