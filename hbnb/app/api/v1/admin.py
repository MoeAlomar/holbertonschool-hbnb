from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from app.services import facade

api = Namespace('admin', description='Admin operations')

# Reuse user model for admin creation
user_model = api.model('AdminUser', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'is_admin': fields.Boolean(description='Admin flag', default=False)
})

# For amenity creation and update
amenity_model = api.model('AdminAmenity', {
    'name': fields.String(required=True, description='Amenity name')
})

# ------------------------
# Admin: Create a new user
# ------------------------
@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    def post(self):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(user_data)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 201

# ---------------------------------------
# Admin: Update any user (email, password)
# ---------------------------------------
@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    @api.expect(user_model, validate=False)
    def put(self, user_id):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        # Ensure unique email
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {'error': 'User not found'}, 404

        return {
            'message': 'User updated successfully',
            'id': updated_user.id,
            'email': updated_user.email
        }, 200

# -----------------------------
# Admin: Add a new amenity
# -----------------------------
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def post(self):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        amenity = facade.create_amenity(data)
        return {'id': amenity.id, 'name': amenity.name}, 201

# --------------------------------
# Admin: Update an existing amenity
# --------------------------------
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def put(self, amenity_id):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        updated = facade.update_amenity(amenity_id, data)
        if not updated:
            return {'error': 'Amenity not found'}, 404

        return {'message': 'Amenity updated', 'id': updated.id, 'name': updated.name}, 200
