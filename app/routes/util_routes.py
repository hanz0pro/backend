from flask import jsonify
from . import api
from app.services.util_service import get_user_count, get_debug_token_info
from ..custom_annotations import requires_role


@api.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the API!"}), 200


@api.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@api.route('/db-check', methods=['GET'])
@requires_role("admin")
def db_check():
    try:
        count = get_user_count()
        return jsonify({"db": "ok", "users": count}), 200
    except Exception as e:
        return jsonify({"db": "error", "details": str(e)}), 500


@api.route('/admin/only', methods=['GET'])
@requires_role("admin")
def admin_only_endpoint():
    return jsonify({"msg": "Witaj adminie!"})

@api.route('/debug-token', methods=['GET'])
def debug_token():
    response, code = get_debug_token_info()
    return jsonify(response), code


@api.route('/.well-known/appspecific/com.chrome.devtools.json')
def ignore_devtools_probe():
    return '', 204
