# controllers/industry_controller.py
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from service.industry_service import IndustryService

industry_blueprint = Blueprint('industry', __name__)
CORS(industry_blueprint)  # 允许跨域请求

@industry_blueprint.route('/create', methods=['POST'])
def create_industry():
    """
    创建行业
    """
    data = request.json
    industryname = data.get('industryname')
    description = data.get('description')

    if not industryname:
        return jsonify({"success": False, "message": "行业名称不能为空"}), 400

    result = IndustryService.create_industry(industryname, description)
    return jsonify(result)

@industry_blueprint.route('/all', methods=['GET'])
def get_all_industries():
    """
    获得所有行业
    """
    result = IndustryService.get_all_industries()
    return jsonify(result)

@industry_blueprint.route('/<int:industryid>', methods=['GET'])
def get_industry_by_id(industryid):
    """
    通过id查行业
    """
    result = IndustryService.get_industry_by_id(industryid)
    return jsonify(result)

@industry_blueprint.route('/<int:industryid>', methods=['PUT'])
def update_industry(industryid):
    """
    更新某个行业信息
    """
    data = request.json
    new_name = data.get('industryname')
    new_description = data.get('description')

    result = IndustryService.update_industry(industryid, new_name, new_description)
    return jsonify(result)

@industry_blueprint.route('/delete/<int:industryid>', methods=['DELETE'])
def delete_industry(industryid):
    """
    删除某个行业
    """
    result = IndustryService.delete_industry(industryid)
    return jsonify(result)
