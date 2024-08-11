import json
import requests
import google.generativeai as genai

def lambda_handler(event, context):
    try:
        input = event['input']
        
        #send input to slack bot
        bot_headers = {'Content-type': 'application/json',}
        json_data = {'text': input,}

        bot_response = requests.post(
            'https://hooks.slack.com/services/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',
            headers=bot_headers,
            json=json_data,
        )

        input, details = input.split(' ;')

        # Initialize variables to hold city, state, and postcode
        city = state = postcode = ""

        # Split the details part by hyphens to separate city, state, and postcode
        try:
          for detail in details.split('-'):
              key, value = detail.split(':')
              if key == ' city':
                  city = value
              elif key == 'state':
                  state = value
              elif key == 'postcode':
                  postcode = value
        except Exception as e:
          print("Error")

        # location = " in " + postcode + " " + city + " "
        location = " in " + city + " "

        default_response = {'top_restaurants': [{'name': 'Le Bernardin',
                    'description': 'Le Bernardin is a seafood restaurant in New York City. It has been awarded four stars by the New York Times and three stars by the Michelin Guide.',
                    'rating': 4.5,
                    'price': '$$$$',
                    'best_food_items': ['Oysters', 'Lobster', 'Dover sole'],
                    'top_2_reviews': [{'author': 'Pete Wells',
                      'source': 'New York Times',
                      'review': 'Le Bernardin is a seafood restaurant that defines excellence. The food is impeccable, the service is flawless, and the atmosphere is elegant and inviting.'},
                      {'author': 'Michael Bauer',
                      'source': 'San Francisco Chronicle',
                      'review': 'Le Bernardin is one of the best seafood restaurants in the world. The chef, Eric Ripert, is a master of his craft, and the menu is full of innovative and delicious dishes.'}]},
                    {'name': 'Masa',
                    'description': 'Masa is a Japanese restaurant in New York City. It has been awarded three stars by the Michelin Guide and is considered one of the best sushi restaurants in the world.',
                    'rating': 4.75,
                    'price': '$$$$$',
                    'best_food_items': ['Omakase', 'Sashimi', 'Nigiri'],
                    'top_2_reviews': [{'author': 'Pete Wells',
                      'source': 'New York Times',
                      'review': 'Masa is a sushi restaurant that transcends the ordinary. The chef, Masa Takayama, is a master of his craft, and the omakase menu is a culinary journey that is both exquisite and unforgettable.'},
                      {'author': 'Michael Bauer',
                      'source': 'San Francisco Chronicle',
                      'review': 'Masa is one of the most expensive restaurants in New York City, but it is also one of the best. The food is impeccable, the service is flawless, and the atmosphere is elegant and serene.'}]},
                    {'name': 'Per Se',
                    'description': 'Per Se is a modern American restaurant in New York City. It has been awarded three stars by the Michelin Guide and is considered one of the best restaurants in the world.',
                    'rating': 4.5,
                    'price': '$$$$',
                    'best_food_items': ['Tasting menu', 'Foie gras', 'Lobster'],
                    'top_2_reviews': [{'author': 'Pete Wells',
                      'source': 'New York Times',
                      'review': 'Per Se is a modern American restaurant that is both innovative and delicious. The chef, Thomas Keller, is a culinary genius, and the tasting menu is a journey through the world of fine dining.'},
                      {'author': 'Michael Bauer',
                      'source': 'San Francisco Chronicle',
                      'review': 'Per Se is one of the most expensive restaurants in New York City, but it is also one of the best. The food is impeccable, the service is flawless, and the atmosphere is elegant and sophisticated.'}]},
                    {'name': 'Eleven Madison Park',
                    'description': 'Eleven Madison Park is a modern American restaurant in New York City. It has been awarded three stars by the Michelin Guide and is considered one of the best restaurants in the world.',
                    'rating': 4.75,
                    'price': '$$$$',
                    'best_food_items': ['Tasting menu', 'Foie gras', 'Lobster'],
                    'top_2_reviews': [{'author': 'Pete Wells',
                      'source': 'New York Times',
                      'review': 'Eleven Madison Park is a modern American restaurant that is both innovative and delicious. The chef, Daniel Humm, is a culinary genius, and the tasting menu is a journey through the world of fine dining.'},
                      {'author': 'Michael Bauer',
                      'source': 'San Francisco Chronicle',
                      'review': 'Eleven Madison Park is one of the most expensive restaurants in New York City, but it is also one of the best. The food is impeccable, the service is flawless, and the atmosphere is elegant and sophisticated.'}]},
                    {'name': 'The Modern',
                    'description': 'The Modern is a modern American restaurant in New York City. It has been awarded two stars by the Michelin Guide and is considered one of the best restaurants in the city.',
                    'rating': 4.25,
                    'price': '$$$',
                    'best_food_items': ['Tasting menu', 'Foie gras', 'Lobster'],
                    'top_2_reviews': [{'author': 'Pete Wells',
                      'source': 'New York Times',
                      'review': 'The Modern is a modern American restaurant that is both innovative and delicious. The chef, Gabriel Kreuther, is a culinary genius, and the tasting menu is a journey through the world of fine dining.'},
                      {'author': 'Michael Bauer',
                      'source': 'San Francisco Chronicle',
                      'review': 'The Modern is one of the most expensive restaurants in New York City, but it is also one of the best. The food is impeccable, the service is flawless, and the atmosphere is elegant and sophisticated.'}]}]}

        genai.configure(api_key=key)

        # Set up the model
        generation_config = {
          "temperature": 0.9,
          "top_p": 1,
          "top_k": 0,
          "max_output_tokens": 2048,
        }
        
        
        safety_settings = [
          {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_ONLY_HIGH"
          },
          {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_ONLY_HIGH"
          },
          {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_ONLY_HIGH"
          },
          {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_ONLY_HIGH"
          },
        ]

        # Calling Gemini API
        model = genai.GenerativeModel(model_name="gemini-1.5-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        if "restaurant" in input.lower() or "restaurants" in input.lower():
          if "in " in input.lower():
            prompt = "Top 5 " +input+ " open now with restaurant description, rating, price, best food items, top 2 reviews and generate response in json format using these keys name, description, rating, price, best_food_items(String), top_2_reviews (author, review)"
          else:
            prompt = "Top 5 " +input + " " + location + " open now with restaurant description, rating, price, best food items, top 2 reviews and generate response in json format using these keys name, description, rating, price, best_food_items(String), top_2_reviews (author, review)"
        else:
          if "in " in input.lower():
            prompt = "Top 5 "+input + " restaurants" + " open now with restaurant description, rating, price, best food items, top 2 reviews and generate response in json format using these keys name, description, rating, price, best_food_items(String), top_2_reviews (author, review)"
          else:
            prompt = "Top 5 " +input + " restaurants" + location + " open now with restaurant description, rating, price, best food items, top 2 reviews and generate response in json format using these keys name, description, rating, price, best_food_items(String), top_2_reviews (author, review)"
        
        prompt_parts = [
          prompt,
        ]

        bot_response = requests.post(
            'https://hooks.slack.com/services/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',
            headers=bot_headers,
            json={'text': prompt,},
            )
        
        try:
            response = model.generate_content(prompt_parts)
            formated_text = json.loads(response.text.replace("```", "").replace("json", ""))
            formated_text = {'restaurants': formated_text}
        except Exception as e:
            print("Error formatting response: " + str(e))
            
            bot_response = requests.post(
            'https://hooks.slack.com/services/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',
            headers=bot_headers,
            json={'text': "Error in formatting" + str(e),},
            )
            return {
            'statusCode': 200,
            'body': default_response
            }

            
        # Add maps link
        try:
          for rest_name, rest_value in formated_text.items():
            if len(rest_value) != 5:
              return {'statusCode': 200, 'body': default_response}
            for restaurant in rest_value:        
                if "restaurant_name" in restaurant or "Restaurant_Name" in restaurant or "restaurant" in restaurant or "Name" in restaurant:
                    try:
                        restaurant["name"] = restaurant["restaurant_name"]
                        restaurant["map_link"] = ("https://maps.google.com/?q=" + restaurant["restaurant_name"] + " " + input).replace(" ", "+")
                    except:
                        pass
                    try:
                        restaurant["name"] = restaurant["Restaurant_Name"]
                        restaurant["map_link"] = ("https://maps.google.com/?q=" + restaurant["Restaurant_Name"] + " " + input).replace(" ", "+")
                    except:
                        pass
                    try:
                        restaurant["name"] = restaurant["restaurant"]
                        restaurant["map_link"] = ("https://maps.google.com/?q=" + restaurant["restaurant"] + " " + input).replace(" ", "+")
                    except:
                        pass
                    try:
                        restaurant["name"] = restaurant["Name"]
                        restaurant["map_link"] = ("https://maps.google.com/?q=" + restaurant["name"] + " " + input).replace(" ", "+")
                    except:
                        pass
                elif "name" in restaurant:
                  try:
                      restaurant["map_link"] = ("https://maps.google.com/?q=" + restaurant["name"] + " " + input).replace(" ", "+")
                  except:  
                    pass  
                      
        except Exception as e:
            print("Error adding map: " + str(e))
            
            bot_response = requests.post(
            'https://hooks.slack.com/services/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',
            headers=bot_headers,
            json={'text': "Error in adding map" + str(e),},
            )
            return {
            'statusCode': 200,
            'body': default_response
            }
        
        # Return the formatted text as the response
        bot_response = requests.post(
            'https://hooks.slack.com/services/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',
            headers=bot_headers,
            json={'text': "Success response",},
            )
        return {
            'statusCode': 200,
            'body': formated_text
        }

    except Exception as e:
        # Handle any exceptions and return an error response
        bot_response = requests.post(
            'https://hooks.slack.com/services/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',
            headers=bot_headers,
            json={'text': "Error Misc " + str(e),},
            )
        return {
            'statusCode': 200,
            'body': default_response
        }