from flask import Flask, jsonify, request
import requests
from app import app

url = "https://api.hatchways.io/assessment/blog/posts?tag="

@app.route('/api/ping')
def ping_api():
    return jsonify({"success": True})

@app.route('/api/posts')
def get_posts():
    tags = request.args.get('tags')
    sort_by = request.args.get('sortBy')
    direction = request.args.get('direction')
    blog_posts = []
    if sort_by == None:
        sort_by = 'id'
    #check tags query param 
    if (tags == None):
        return jsonify({"error": "Tags parameter is required"}), 400
    # check sortBy query param
    if (sort_by not in ({None,'id','reads','likes','popularity'})):
        return jsonify({"error": "sortBy parameter is invalid"}), 400
    # check direction query param
    if (direction not in ({None, 'desc', 'asc'})):
        return jsonify({"error": "direction parameter is invalid"}), 400
    if direction == None or 'asc':
        direction_flag = False
    if direction == 'desc':
        direction_flag = True
    # get posts from hatchway api
    # if multiple tags must split up tags and make individual calls to hatchway API
    if ',' in tags:
        #make request to all tags
        tag_values = tags.split(',')
        for tag in tag_values:
            tagged_posts = requests.get(url + tag)
            tagged_posts = tagged_posts.json()['posts']
            for post in tagged_posts:
                if post not in blog_posts:
                    blog_posts.append(post)

        blog_posts = sorted(blog_posts, key=lambda k: k.get(sort_by),reverse=direction_flag)
        return jsonify({'posts': blog_posts})
    # defaults here if only single tag
    tagged_posts = requests.get(url + tags)
    blog_posts = tagged_posts.json()['posts']
    blog_posts = sorted(blog_posts, key=lambda k: k.get(sort_by),reverse=direction_flag)
    return jsonify({'posts': blog_posts})
