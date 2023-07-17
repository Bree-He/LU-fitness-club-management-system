from flask import Blueprint

trainer_bp = Blueprint('trainer', __name__)

from trainer import trainer