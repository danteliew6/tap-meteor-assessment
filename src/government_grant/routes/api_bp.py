from flask import Blueprint
from ..controllers.ApiController import ApiController

api_bp = Blueprint("api_bp", __name__)

# class_bp.route('/classlist', methods=['GET'])(ClassController.getClassList)
api_bp.route('/create-household', methods=['POST'])(ApiController.createHousehold)
# api_bp.route('/add-matches', methods=['POST'])(MatchController.addMatches)
# api_bp.route('/get-team-rankings', methods=['GET'])(MatchController.getTeamRankings)
# api_bp.route('/delete-competition-data', methods=['DELETE'])(MatchController.deleteCompetitionData)




