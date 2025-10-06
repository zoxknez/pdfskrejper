"""
Start Flask App as Background Service
Run with: python start_app.py
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def start_flask_background():
    """Start Flask app as background process"""
    
    # Set environment variables
    env = os.environ.copy()
    env['FLASK_APP'] = 'app.py'
    env['FLASK_ENV'] = 'development'
    
    # Python executable path
    python_exe = sys.executable
    
    # Start Flask in background
    print("🚀 Starting Flask application in background...")
    print(f"   Python: {python_exe}")
    print(f"   Working Dir: {Path.cwd()}")
    
    # Use START command to run in new window (Windows)
    cmd = [
        'cmd', '/c', 'start', 
        'Flask-App',  # Window title
        '/min',  # Minimized
        python_exe, '-m', 'flask', 'run', 
        '--host=0.0.0.0', 
        '--port=5000'
    ]
    
    try:
        # Start process detached from parent
        subprocess.Popen(
            cmd,
            env=env,
            cwd=str(Path.cwd()),
            creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.DETACHED_PROCESS
        )
        
        print("\n✅ Flask application started!")
        print("   URL: http://127.0.0.1:5000")
        print("   Status: Running in background")
        print("\n💡 To stop: Find 'Flask-App' window or use Task Manager")
        
        # Wait a bit to let it start
        time.sleep(2)
        
        # Check if it's running
        import requests
        try:
            response = requests.get('http://127.0.0.1:5000', timeout=5)
            if response.status_code in [200, 302, 404]:
                print("\n✅ Server is responding!")
        except Exception as e:
            print(f"\n⚠️  Server starting... (may take a few seconds)")
            
    except Exception as e:
        print(f"\n❌ Error starting Flask: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = start_flask_background()
    if success:
        print("\n🎉 Application is running in background!")
        print("   You can close this terminal window.")
    else:
        print("\n❌ Failed to start application.")
        sys.exit(1)
