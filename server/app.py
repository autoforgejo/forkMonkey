"""
ForkMonkey Backend Server

Flask API for managed adoption flows (Trustless and Full-Trust OAuth).
"""

import os
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from dotenv import load_dotenv

from github_service import GitHubService

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:*',
    'https://roeiba.github.io',
    'https://*.github.io'
])

# Configuration
GITHUB_CLIENT_ID = os.getenv('GITHUB_APP_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_APP_CLIENT_SECRET', '')
GITHUB_APP_ID = os.getenv('GITHUB_APP_ID', '')
GITHUB_PRIVATE_KEY = os.getenv('GITHUB_PRIVATE_KEY', '')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'forkmonkey-api'})


@app.route('/api/adopt/trustless', methods=['POST'])
def trustless_adoption():
    """
    Trustless adoption endpoint.
    
    Expected JSON body:
    {
        "github_username": "string",
        "customization": {
            "name": "string (optional)",
            "body_color": "string (optional)",
            "face_expression": "string (optional)",
            "accessory": "string (optional)"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        username = data.get('github_username', '').strip()
        if not username:
            return jsonify({'success': False, 'error': 'GitHub username is required'}), 400
        
        customization = data.get('customization', {})
        
        # Initialize GitHub service
        try:
            github_service = GitHubService()
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        
        # Perform full trustless setup
        result = github_service.full_setup_for_trustless(username, customization)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        app.logger.error(f"Trustless adoption error: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@app.route('/api/adopt/oauth/authorize', methods=['GET'])
def oauth_authorize():
    """
    Initiate OAuth flow.
    
    Returns the authorization URL for the GitHub App.
    """
    if not GITHUB_CLIENT_ID:
        return jsonify({
            'success': False, 
            'error': 'OAuth not configured. Please use Manual or Trustless method.'
        }), 503
    
    # Build authorization URL
    redirect_uri = request.args.get('redirect_uri', f"{request.host_url}api/adopt/oauth/callback")
    
    auth_url = (
        f"https://github.com/apps/forkmonkey-adopter/installations/new"
        f"?client_id={GITHUB_CLIENT_ID}"
    )
    
    return jsonify({
        'success': True,
        'auth_url': auth_url
    })


@app.route('/api/adopt/oauth/callback', methods=['GET'])
def oauth_callback():
    """
    OAuth callback handler.
    
    Receives the installation ID after user authorizes the GitHub App.
    """
    installation_id = request.args.get('installation_id')
    setup_action = request.args.get('setup_action')
    
    if not installation_id:
        return redirect('/web/?error=oauth_failed')
    
    # Store installation ID in session/database for the complete step
    # For now, redirect back to the frontend with the installation ID
    return redirect(f'/web/?oauth_complete=true&installation_id={installation_id}')


@app.route('/api/adopt/oauth/complete', methods=['POST'])
def oauth_complete():
    """
    Complete OAuth adoption.
    
    Uses the GitHub App installation to fork and set up the repository
    directly in the user's account.
    
    Expected JSON body:
    {
        "installation_id": "string",
        "customization": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        installation_id = data.get('installation_id')
        customization = data.get('customization', {})
        
        if not installation_id:
            return jsonify({'success': False, 'error': 'Installation ID required'}), 400
        
        # Initialize GitHub service
        # Token is not needed here as we use app credentials from env
        try:
            github_service = GitHubService(token="dummy") # Token required by init check but unused for app flow
        except ValueError:
            # Bypass token check if possible or mock it, 
            # actually GitHubService requires token in init.
            # We can pass a dummy token since we won't use self.github for this flow
            # or better, refactor GitHubService to make token optional.
            # For now, passing a dummy if GITHUB_TOKEN env var is missing (which it shouldn't be).
            github_service = GitHubService(token="app-flow-placeholder")
        
        # Perform full OAuth setup
        result = github_service.full_setup_for_oauth(installation_id, customization)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        app.logger.error(f"OAuth completion error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/validate/username', methods=['GET'])
def validate_username():
    """
    Validate GitHub username exists.
    
    Query params:
        username: GitHub username to validate
    """
    username = request.args.get('username', '').strip()
    
    if not username:
        return jsonify({'valid': False, 'error': 'Username is required'}), 400
    
    try:
        github_service = GitHubService()
        result = github_service.validate_username(username)
        return jsonify(result), 200 if result.get('valid') else 404
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"🐵 ForkMonkey API starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
