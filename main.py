from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

# 1. CSV einlesen
def load_companies_from_csv(filepath):
    companies = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            companies.append({
                "id": row["company_id"],
                "name": row["name"],
                "entscheidungsstruktur": int(row["score_entscheidungsstruktur"]),
                "entwicklung": int(row["score_entwicklung"]),
                "balance": int(row["score_balance"])
            })
    return companies

# 2. Matching-Funktion
def calculate_score(user, company):
    differences = []
    for key in user:
        if key in company:
            diff = abs(user[key] - company[key])
            differences.append(diff)

    if differences:
        score = 1 - (sum(differences) / len(differences))
        return max(0, round(score, 2))
    return 0

# 3. POST-Endpoint
@app.route("/match", methods=["POST"])
def match():
    data = request.get_json()

    if "user_data" not in data:
        return jsonify({"error": "Missing user_data"}), 400

    user = data["user_data"]
    companies = load_companies_from_csv("unternehmen_matching_v1.csv")

    results = []
    for company in companies:
        score = calculate_score(user, company)
        results.append({
            "company_id": company["id"],
            "company_name": company["name"],
            "score": score
        })

    top_5 = sorted(results, key=lambda x: x["score"], reverse=True)[:5]
    return jsonify(top_5)

# 4. Server starten
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
