from flask import Blueprint, request, jsonify
from service.news_service import NewsService

news_blueprint = Blueprint('news', __name__)

# 添加新闻
@news_blueprint.route('/add', methods=['POST'])
def add_news():
    data = request.json
    title = data.get('title')
    publishdate = data.get('publishdate')
    content = data.get('content')
    sourceid = data.get('sourceid')
    industryid = data.get('industryid')
    sentimentid = data.get('sentimentid')
    stockid = data.get('stockid')

    if not title:
        return jsonify({"success": False, "message": "标题不能为空"}), 400

    result = NewsService.add_news(title, publishdate, content, sourceid, industryid, sentimentid, stockid)
    return jsonify(result)


# 获取单条新闻
@news_blueprint.route('/<int:newsid>', methods=['GET'])
def get_news(newsid):
    news = NewsService.get_news_by_id(newsid)
    if news:
        return jsonify(news)
    else:
        return jsonify({"success": False, "message": "新闻不存在"}), 404


# 获取所有新闻
@news_blueprint.route('/all', methods=['GET'])
def get_all_news():
    news_list = NewsService.get_all_news()
    return jsonify(news_list)


# 删除新闻
@news_blueprint.route('/delete', methods=['POST'])
def delete_news():
    data = request.json
    newsid = data.get('newsid')

    if not newsid:
        return jsonify({"success": False, "message": "newsid 必须提供"}), 400

    result = NewsService.delete_news(newsid)
    return jsonify(result)


# 更新新闻
@news_blueprint.route('/update', methods=['POST'])
def update_news():
    data = request.json
    newsid = data.get('newsid')
    title = data.get('title')
    content = data.get('content')
    publishdate = data.get('publishdate')
    sourceid = data.get('sourceid')
    industryid = data.get('industryid')
    sentimentid = data.get('sentimentid')
    stockid = data.get('stockid')

    if not newsid:
        return jsonify({"success": False, "message": "newsid 必须提供"}), 400

    result = NewsService.update_news(newsid, title, content, publishdate, sourceid, industryid, sentimentid, stockid)
    return jsonify(result)
