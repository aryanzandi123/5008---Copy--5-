from flask import Flask, jsonify, render_template, request, make_response
import json
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search/<protein>')
def search_protein(protein):
    return jsonify({
        "status": "found",
        "protein": protein,
        "has_interactions": True,
        "interaction_count": 5,
        "last_queried": "2023-01-01",
        "query_count": 1
    })

@app.route('/api/visualize/<protein>')
def get_visualization(protein):
    # Mock data structure matching the new requirements
    mock_data = {
        "snapshot_json": {
            "main": "ATXN3",
            "proteins": ["ATXN3", "PNKP", "ATM", "VCP"],
            "interactions": [
                {
                    "source": "ATXN3",
                    "target": "PNKP",
                    "type": "direct",
                    "direction": "main_to_primary",
                    "arrow": "inhibits",
                    "confidence": 0.9,
                    "interaction_effect": "inhibition",
                    "pathways": [{"name": "DNA Damage Response", "id": "pathway_DNA_Damage_Response"}],
                    "functions": [{"function": "DNA Repair", "arrow": "activates"}]
                },
                {
                    "source": "PNKP",
                    "target": "ATM",
                    "type": "direct", # Should be visualized as chain
                    "direction": "main_to_primary", # Relative to PNKP as pseudo-main? Or just direct link.
                    "arrow": "activates",
                    "confidence": 0.95,
                    "interaction_effect": "activation",
                    "pathways": [{"name": "DNA Damage Response", "id": "pathway_DNA_Damage_Response"}],
                    "functions": [{"function": "Signaling", "arrow": "activates"}],
                     "_direct_mediator_link": True # Marking it as a direct link extracted from chain
                },
                {
                     "source": "ATXN3",
                     "target": "VCP",
                     "type": "direct",
                     "arrow": "binds",
                     "interaction_effect": "binding",
                     "pathways": []
                }
            ],
            "pathways": [
                {
                    "id": "pathway_DNA_Damage_Response",
                    "name": "DNA Damage Response",
                    "interactor_ids": ["PNKP", "ATM"],
                    "interaction_count": 2
                }
            ]
        },
        "ctx_json": {}
    }

    from visualizer import create_visualization_from_dict
    html = create_visualization_from_dict(mock_data)

    response = make_response(html)
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5009, debug=True)
