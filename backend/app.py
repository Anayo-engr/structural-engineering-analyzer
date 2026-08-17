"""
Structural Engineering Analyzer
Backend API

Connects the frontend to the beam and column
calculation engines.
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
    Check whether the backend API is running.
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
    Perform a beam calculation.

    Required parameters:
        beam_width
        overall_depth
        concrete_cover
        main_bar_diameter
        dead_load
        live_load
        span

    Optional parameters:
        concrete_strength
        steel_strength
        link_diameter
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
            main_bar_diameter=float(
                data["main_bar_diameter"]
            ),
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
            "error": (
                f"Missing required parameter: "
                f"{error.args[0]}"
            )
        }), 400

    except (ValueError, TypeError) as error:

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
    Perform a column calculation.

    Required parameters:
        column_width
        column_depth
        dead_load
        live_load

    Optional parameters:
        concrete_strength
        steel_strength
        preferred_bar_diameter
    """

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data was provided."
            }), 400

        result = calculate_column(
            column_width=float(
                data["column_width"]
            ),
            column_depth=float(
                data["column_depth"]
            ),
            dead_load=float(
                data["dead_load"]
            ),
            live_load=float(
                data["live_load"]
            ),
            concrete_strength=float(
                data.get("concrete_strength", 25)
            ),
            steel_strength=float(
                data.get("steel_strength", 500)
            ),
            preferred_bar_diameter=float(
                data.get("preferred_bar_diameter", 16)
            )
        )

        return jsonify({
            "success": True,
            "type": "column",
            "result": result
        })

    except KeyError as error:

        return jsonify({
            "success": False,
            "error": (
                f"Missing required parameter: "
                f"{error.args[0]}"
            )
        }), 400

    except (ValueError, TypeError) as error:

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
    Handle unknown routes.
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
