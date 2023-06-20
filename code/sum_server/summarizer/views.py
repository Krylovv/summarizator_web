from django.shortcuts import render
from .forms import UserForm
import requests
import json
import re

def do_cleanup(value):
    value = value.replace("\n", " ").replace('\r\n', ' ').replace("\"", "").replace("»", "").replace("«", "")
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    value = (emoji_pattern.sub(r'', value))  # no emoji
    return value


def news_form(request):
    submitbutton = request.POST.get("submit")
    print(submitbutton)
    news = ''
    form = UserForm(request.POST or None)
    context = {'form': form, 'news': news, 'submitbutton': submitbutton}
    if form.is_valid():
        news = form.cleaned_data.get("news")
        text = news
        do_cleanup(text)
        payload = json.dumps({
            "instances": [
                {"text": text,
                 "num_beams": 5,
                 "num_return_sequences": 20,
                 "length_penalty": 1.0
                 }
            ]
        })
        headers = {
            'Content-type': 'application/json'
        }
        url = "https://api.aicloud.sbercloud.ru/public/v2/summarizator/predict"
        response = requests.request("POST", url, headers=headers, data=payload)
        response_obj = json.loads(response.text)
        summ_txt = response_obj['prediction_best']['bertscore']
        context = {'form': form, 'news': news, 'summ_txt': summ_txt, 'submitbutton': submitbutton}
    return render(request, 'news_getter.html', context)



