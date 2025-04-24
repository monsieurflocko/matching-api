from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

# 1. CSV einlesen
def load_companies_from_csv(filepath):
    companies = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            companies.append({
                "id": row["company_id"],
                "name": row["name"],
                "entscheidungsstruktur": int(row["score_entscheidungsstruktur"]),
                "entwicklung": int(row["score_entwicklung"]),
                "balance": int(row["score_balance"])
            })
    return companies

# 2. Matching berechnen
def calculate_match_score(user_data, company_data):
    diff_sum = 0
    num_keys = 0
    for key in ["entscheidungsstruktur", "entwicklung", "balance"]:
        if key in user_data and key in company_data:
            diff_sum += abs(user_data[key] - company_data[key])
            num_keys += 1
    if num_keys == 0:
        return 0
    return round(1 - (diff_sum / (2 * num_keys)), 2)

# 3. API Endpoint
@app.route('/match', methods=['POST'])
def match():
    data = request.get_json()
    user_data = data["user_data"]

    companies = load_companies_from_csv("unternehmen_matching_v1.csv")
    
    results = []
    for company in companies:
        score = calculate_match_score(user_data, company)
        results.append({
            "company": company["name"],
            "score": score
        })

    # Top 5 Ergebnisse zurückgeben
    results.sort(key=lambda x: x["score"], reverse=True)
    top_matches = results[:5]

    return jsonify(top_matches)

# 4. Startpunkt (nicht notwendig auf Render)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

# Test taetigkeit 
taetigkeit = request.user_data.get("taetigkeit", "")
print("Userwunsch:", taetigkeit)
