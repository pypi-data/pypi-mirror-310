import json

def lebanon_passport_extraction(passport_data, genai_client):
    message = genai_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        temperature=0.3,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"From the attached text, please extract the data in a structured format, the response should be a dictionary, having first_name, mother_name(mother full name), father_name, name which is last_name, passport_number, dob(dd/mm/yyyy), place_of_birth, nationality(ISO 3166-1 alpha-3 country code), issue_date, expiry_date(dd/mm/yyyy), gender(FEMALE, MALE), mrz1, mrz2, registry_place_and_issue_number(only 1, no _ar and _en). Note that the passport_number should always be  2 letters and 7 digits, if the length is less than 7 then append 0 in the start for passport_number_en and same way for passport_number_ar(numbers in passport arabic as well). The extracted details should be in arabic and a transliterated version as well having key_name_en, including id_number, dob(dd/mm/yyyy), names, gender etc.. the structure should be 'first_name_ar', 'first_name_en', father_name_ar, father_name_en, mother_name_ar, mother_name_en, id_number_ar, id_number_en, dob_ar, dob_en, place_of_birth_ar, place_of_birth_en, etc. Make sure that the response should only contain a dictionary, and nothing else. Here's the text for your task: {passport_data}"
                    }
                ]
            }
        ]
    )

    result = message.content[0].text

    try:
        back_data = json.loads(result)

        if back_data.get('first_name_ar', ''):
            back_data['first_name'] = back_data.pop('first_name_ar', '')
        
        if back_data.get('name_ar', ''):
            back_data['last_name'] = back_data.pop('name_ar', '')
        
        if back_data.get('name_en', ''):
            back_data['last_name_en'] = back_data.pop('name_en', '')
        
        if back_data.get('father_name_ar', ''):
            back_data['father_name'] = back_data.pop('father_name_ar', '')

        if back_data.get('dob_en', ''):
            back_data['dob'] = back_data.pop('dob_en', '')
        
        if back_data.get('place_of_birth_ar', ''):
            back_data['place_of_birth'] = back_data.pop('place_of_birth_ar', '')
        
        if back_data.get('passport_number_en', ''):
            back_data['passport_number'] = back_data.pop('passport_number_en', '')
            back_data['id_number'] = back_data.get('passport_number', '')
            try:
                del back_data['passport_number_ar']
            except:
                pass
        
        if back_data.get('expiry_date_en', ''):
            back_data['expiry_date'] = back_data.pop('expiry_date_en', '')
        
        if back_data.get('issue_date_en', ''):
            back_data['issue_date'] = back_data.pop('issue_date_en', '')
        
        if back_data.get('gender_en', ''):
            back_data['gender'] = back_data.pop('gender_en', '')
        
        if back_data.get('mrz1', '') and back_data.get('mrz2', ''):
            back_data['mrz'] = back_data.get('mrz1', '') + back_data.get('mrz2', '')
        
        if back_data.get('nationality_en', ''):
            back_data['nationality'] = back_data.pop('nationality_en', '')

        if not back_data.get('mother_name_en', ''):
            back_data['mother_name'], back_data['mother_name_en'] = '', ''

        if back_data.get('mother_name_en', ''):
            back_data['mother_name'] = back_data.pop('mother_name_en', '')
            
        if back_data.get('registry_place_and_issue_number_en', ''):
            back_data['registry_place_and_number'] = back_data.pop('registry_place_and_issue_number_en', '')
        
        if back_data.get('registry_place_and_issue_number', ''):
            back_data['registry_place_and_number'] = back_data.pop('registry_place_and_issue_number', '')
        
        if not back_data.get('registry_place_and_number', ''):
            back_data['registry_place_and_number'] = ''
        
        back_data['issuing_country'] = 'LBN'
            
    except Exception as e:
        print(f"Error in processing the extracted data: {e}")
        back_data = {}
    
    return back_data

