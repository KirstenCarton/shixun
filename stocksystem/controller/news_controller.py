from flask import Blueprint, request, jsonify
from service.news_service import NewsService

news_blueprint = Blueprint('news', __name__)


@news_blueprint.route('/add', methods=['POST'])
def add_news():
    """
    添加新闻
    """
    data = request.json
    title = data.get('title')
    url = data.get('url')
    content = data.get('content')
    publishdate = data.get('publishdate')
    sourceid = data.get('sourceid')
    industryid = data.get('industryid')
    sentimentid = data.get('sentimentid')
    stockid = data.get('stockid')

    if not title or not url or not content:
        return jsonify({"success": False, "message": "标题不能为空"}), 400

    result = NewsService.add_news(title, url, content, publishdate, sourceid, industryid, sentimentid, stockid)
    return jsonify(result)



@news_blueprint.route('/<int:newsid>', methods=['GET'])
def get_news(newsid):
    """
    获取单条新闻
    """
    news = NewsService.get_news_by_id(newsid)
    if news:
        return jsonify(news)
    else:
        return jsonify({"success": False, "message": "新闻不存在"}), 404



@news_blueprint.route('/all', methods=['GET'])
def get_all_news():
    """
    获取所有新闻
    """
    news_list = NewsService.get_all_news()
    return jsonify(news_list)



@news_blueprint.route('/delete/<int:newsid>', methods=['DELETE'])
def delete_news(newsid):
    """
    删除新闻
    """
    result = NewsService.delete_news(newsid)
    return jsonify(result)



@news_blueprint.route('/update', methods=['PUT'])
def update_news():
    """
    更新新闻
    """
    data = request.json
    newsid = data.get('newsid')
    title = data.get('title')
    url = data.get('url')
    content = data.get('content')
    publishdate = data.get('publishdate')
    sourceid = data.get('sourceid')
    industryid = data.get('industryid')
    sentimentid = data.get('sentimentid')
    stockid = data.get('stockid')

    if not newsid:
        return jsonify({"success": False, "message": "newsid 必须提供"}), 400


    result = NewsService.update_news(newsid, title, url, content, publishdate, sourceid, industryid, sentimentid, stockid)
    return jsonify(result)

