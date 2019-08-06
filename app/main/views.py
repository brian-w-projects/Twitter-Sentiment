from flask import render_template, request, jsonify, session, flash, redirect, url_for, current_app
from . import main
from .forms import TermForm
# from ..models import
import os
import dill
from keras.models import load_model
from ..model.AttentionLayer import AttentionLayer
from urllib import parse
import requests
from requests_oauthlib import OAuth1
import json
from keras import backend as K
from statistics import mean


@main.route('/', methods=['GET', 'POST'])
def index():
    form = TermForm(request.form)
    responses = None

    if request.method == 'POST':
        if form.validate():
            with open(os.path.join('app', 'key'), 'r') as file:
                count = 20
                query = parse.quote(form.term.data)
                auth = OAuth1(*file.read().splitlines())
                url = f'https://api.twitter.com/1.1/search/tweets.json?q={query}&result_type=popular&count={count}&lang=en'
                api_request = requests.get(url, auth=auth)
                if api_request.status_code != 200:
                    flash('Error with Twitter API', 'error')
                else:
                    responses = get_predictions([tweet['text'] for tweet in api_request.json()['statuses']])
                    responses = json.loads(responses.get_data().decode('utf-8'))
                    flash('Success', 'success')
        else:
            flash('Sorry, there was an error', 'error')
    return render_template('main/index.html', form=form, responses=responses)


@main.route('/predict', methods=['POST'])
def get_predictions(data=None):
    K.clear_session()
    if data is None:
        data = [v for v in request.get_json().values()]
    results = dict()
    results['success'] = 'False'
    try:
        with open(os.path.join('app', 'model', 'pipe.pkl'), 'rb') as file:
            dill._dill._reverse_typemap['ClassType'] = type
            pipe = dill.load(file)
            model = load_model(os.path.join('app', 'model', 'model.h5'),
                               custom_objects={'AttentionWithContext': AttentionLayer.AttentionWithContext})
            results['results'] = [{'id': k, 'tweet': r[0], 'score': float(r[1])} for k, r in
                       enumerate(zip(data, model.predict_proba(pipe.transform(data))[:, 1]), 0)]
            results['average'] = mean(r['score'] for r in results['results'])
            results['success'] = 'True'
    except Exception as e:
        print(e)
        return jsonify({})
    K.clear_session()
    return jsonify(results)
