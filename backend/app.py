"""
Structural Engineering Analyzer
Backend API

This module provides the backend API for the
Structural Engineering Analyzer.

It connects the frontend to the calculation engine
for beam and column calculations.
"""

from flask import Flask, jsonify, request

from calculations.beams.beam_calculator import calculate_beam
from calculations.columns.column_calculator import calculate_column


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# HOME / HEALTH CHECK
# =========================================================

@app.route("/", methods=["GET"])
def home():
    """
    Basic API health check.
    """

    return jsonify({
        "application": "Structural Engineering Analyzer",
        "status": "running",
        "message": "Backend API is working."
    })


# =========================================================
# BEAM CALCULATION
# =========================================================

@app.route("/api/beam/calculate", methods=["POST"])
def calculate_beam_api():
    """
    Receive beam parameters and perform a beam calculation.

    Expected JSON input:

        {
            "beam_width": 300,
            "overall_depth": 500,
            "concrete_cover": 25,
            "main_bar_diameter": 16,
            "dead_load": 10,
            "live_load": 5,
            "span": 6,
            "concrete_strength": 25,
            "steel_strength": 500,
            "link_diameter": 8
        }
    """

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data was provided."
            }), 400

        result = calculate_beam(
            beam_width=float(data["beam_width"]),
            overall_depth=float(data["overall_depth"]),
            concrete_cover=float(data["concrete_cover"]),
            main_bar_diameter=float(data["main_bar_diameter"]),
            dead_load=float(data["dead_load"]),
            live_load=float(data["live_load"]),
            span=float(data["span"]),
            concrete_strength=float(
                data.get("concrete_strength", 25)
            ),
            steel_strength=float(
                data.get("steel_strength", 500)
            ),
            link_diameter=float(
                data.get("link_diameter", 8)
            )
        )

        return jsonify({
            "success": True,
            "type": "beam",
            "result": result
        })

    except KeyError as error:

        return jsonify({
            "success": False,
            "error": f"Missing required parameter: {error.args[0]}"
        }), 400

    except ValueError as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "success": False,
            "error": "An unexpected error occurred.",
            "details": str(error)
        }), 500


# =========================================================
# COLUMN CALCULATION
# =========================================================

@app.route("/api/column/calculate", methods=["POST"])
def calculate_column_api():
    """
    Receive column parameters and perform a column calculation.

    Expected JSON input will depend on the parameters
    supported by calculate_column().
    """

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data was provided."
            }), 400

        result = calculate_column(
            **data
        )

        return jsonify({
            "success": True,
            "type": "column",
            "result": result
        })

    except TypeError as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except ValueError as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "success": False,
            "error": "An unexpected error occurred.",
            "details": str(error)
        }), 500


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def page_not_found(error):
    """
    Handle unknown API routes.
    """

    return jsonify({
        "success": False,
        "error": "API endpoint not found."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Handle unsupported HTTP methods.
    """

    return jsonify({
        "success": False,
        "error": "HTTP method not allowed."
    }), 405


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
