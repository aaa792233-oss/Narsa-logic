from datetime import datetime, timedelta

# जुना डेटा: तारीख, वार आणि आलेली जोडी
historical_data = [
    {"date": "2026-05-04", "day": "Monday", "jodi": "51"},
    {"date": "2026-05-05", "day": "Tuesday", "jodi": "76"},
    {"date": "2026-05-11", "day": "Monday", "jodi": "51"}, # ११ तारखेला पुन्हा ५१ आला
    {"date": "2026-05-12", "day": "Tuesday", "jodi": "33"},
    {"date": "2026-05-18", "day": "Monday", "jodi": "51"}, # १८ तारखेला पुन्हा ५१ आला
    {"date": "2026-05-19", "day": "Tuesday", "jodi": "76"}, # ७६ पुन्हा आला
]

def analyze_chart(target_jodi, data):
    dates_found = []
    days_found = []
    
    # दिलेल्या जोडीचा इतिहास तपासणे
    for record in data:
        if record["jodi"] == target_jodi:
            dates_found.append(datetime.strptime(record["date"], "%Y-%m-%d"))
            days_found.append(record["day"])
            
    if len(dates_found) < 2:
        return "अंदाज लावण्यासाठी जुना डेटा कमी आहे."

    # १. कोणत्या वारी हा आकडा जास्त येतो ते शोधणे
    most_common_day = max(set(days_found), key=days_found.count)
    
    # २. दोन निकालांमधील सरासरी दिवसांचा गॅप (कालावधी) काढणे
    gaps = []
    for i in range(len(dates_found) - 1):
        gap = (dates_found[i+1] - dates_found[i]).days
        gaps.append(gap)
        
    average_gap = sum(gaps) / len(gaps) # सरासरी गॅप (दिवस)
    
    # ३. शेवटच्या तारखेवरून पुढील संभाव्य तारीख काढणे
    last_date = dates_found[-1]
    next_predicted_date = last_date + timedelta(days=int(average_gap))
    
    return {
        "most_common_day": most_common_day,
        "average_gap_days": int(average_gap),
        "next_date_prediction": next_predicted_date.strftime("%Y-%m-%d")
    }

# समजा आपल्याला '51' या जोडीचा पॅटर्न पाहायचा आहे
jodi_to_check = "51"
result = analyze_chart(jodi_to_check, historical_data)

print(f"--- 📊 {jodi_to_check} जोडीचे विश्लेषण ---")
print(f"१. हा आकडा जास्त करून या वारी येतो: {result['most_common_day']}")
print(f"२. हा आकडा पुन्हा येण्यासाठी सरासरी गॅप (दिवस): {result['average_gap_days']} दिवस")
print(f"३. पुढील संभाव्य तारीख (अंदाजे): {result['next_date_prediction']}")
