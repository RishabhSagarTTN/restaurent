from google import genai
import json
from .models import Dishes
def AIdata(dish,disher):
    if  Dishes.objects.get(dish_sluger=disher).dish_detail=="":
        client = genai.Client(api_key="AIzaSyC8_1tSULwlcrywSLdxfP66aegp1Z3KuL0")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"write about {dish} what its benefit why its so popular in json if not able to generate give some interesting fact about the dish where it is originated,make  make sure it has only one key and in that key make the summary and remind that you have to, make only one key and the key name should be 'summary'",
        )

        temp=json.loads(response.text.replace("'","").replace("`","").replace("json",""))['summary']
        Dishes.objects.filter(dish_sluger=disher).update(dish_detail=temp)
        return temp
    return Dishes.objects.get(dish_sluger=disher).dish_detail
