from flask import Blueprint, request, g
from flask_structured_api.core.models.responses import SuccessResponse
from flask_structured_api.core.services.auth import AuthService
from flask_structured_api.core.models.requests.auth import RegisterRequest, LoginRequest, RefreshTokenRequest, APIKeyRequest
from flask_structured_api.core.models.responses.auth import TokenResponse, UserResponse
from flask_structured_api.core.db import get_session
from flask_structured_api.core.auth import require_auth
from flask_structured_api.core.exceptions import APIError
import hashlib

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    register_data = RegisterRequest(**data)

    db = next(get_session())
    auth_service = AuthService(db)

    user = auth_service.register_user(register_data)

    return SuccessResponse(
        message="User registered successfully",
        data=user.dict()
    ).dict(), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return access token"""
    data = request.get_json()
    login_data = LoginRequest(**data)

    db = next(get_session())
    auth_service = AuthService(db)

    token = auth_service.login(login_data)

    return SuccessResponse(
        message="Login successful",
        data=token.dict()
    ).dict()


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user information"""
    db = next(get_session())
    auth_service = AuthService(db)

    user = auth_service.get_user_by_id(g.user_id)
    if not user:
        raise APIError(
            message="User not found",
            code="AUTH_USER_NOT_FOUND",
            status_code=404
        )

    return SuccessResponse(
        message="Current user retrieved successfully",
        data=UserResponse.from_orm(user).dict()
    ).dict()


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token"""
    data = request.get_json()
    refresh_data = RefreshTokenRequest(**data)

    db = next(get_session())
    auth_service = AuthService(db)

    token = auth_service.refresh_token(refresh_data.refresh_token)

    return SuccessResponse(
        message="Token refreshed successfully",
        data=token.dict()
    ).dict()


@auth_bp.route('/api-keys', methods=['GET'])
@require_auth
def list_api_keys():
    """List all API keys for the authenticated user"""
    db = next(get_session())
    auth_service = AuthService(db)

    keys = auth_service.get_user_api_keys(g.user_id)
    return SuccessResponse(
        message="API keys retrieved",
        data={
            'items': [{
                'id': key.id,
                'name': key.name,
                'last_used_at': key.last_used_at,
                'created_at': key.created_at,
            } for key in keys]
        }
    ).dict()


@auth_bp.route('/api-keys', methods=['POST'])
@require_auth
def create_api_key():
    """Generate a new API key for the authenticated user"""
    data = request.get_json()
    key_data = APIKeyRequest(**data)

    db = next(get_session())
    auth_service = AuthService(db)

    # Create new API key
    api_key = auth_service.create_api_key(
        user_id=g.user_id,
        name=key_data.name,
        scopes=key_data.scopes
    )

    return SuccessResponse(
        message="API key created successfully",
        data={
            'key': api_key,  # Only time the raw key is exposed
            'name': key_data.name,
            'scopes': key_data.scopes
        }
    ).dict(), 201


@auth_bp.route('/api-keys/<int:key_id>', methods=['DELETE'])
@require_auth
def revoke_api_key(key_id: int):
    """Revoke an API key"""
    db = next(get_session())
    auth_service = AuthService(db)

    # Get the current key hash if we're using API key auth
    current_key_hash = None
    if hasattr(g, 'api_key'):
        current_key_hash = hashlib.sha256(g.api_key.encode()).hexdigest()

    auth_service.revoke_api_key(key_id, g.user_id, current_key_hash)
    return SuccessResponse(
        message="API key revoked successfully"
    ).dict()
