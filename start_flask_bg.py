"""
Start Flask App as Background Service - Simple Version
"""
import os
import sys
import subprocess
from pathlib import Path


def start_flask_simple():
    """Start Flask app in background using PowerShell"""
    
    # Set environment
    python_exe = sys.executable
    flask_module = '-m flask run --host=0.0.0.0 --port=5000'
    
    print("🚀 Starting Flask application in background...")
    print(f"   URL: http://127.0.0.1:5000")
    
    # Create PowerShell script
    ps_script = f"""
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
Start-Process -FilePath "{python_exe}" -ArgumentList "{flask_module}" -WindowStyle Hidden -PassThru
Write-Host "Flask started in background!"
"""
    
    # Save to temp file
    ps_file = Path("start_flask_temp.ps1")
    ps_file.write_text(ps_script)
    
    try:
        # Execute PowerShell script
        result = subprocess.run(
            ['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(ps_file)],
            capture_output=True,
            text=True,
            cwd=str(Path.cwd())
        )
        
        if result.returncode == 0:
            print("\n✅ Flask application started in background!")
            print("   Check: http://127.0.0.1:5000")
            ps_file.unlink()  # Clean up
            return True
        else:
            print(f"\n❌ Error: {result.stderr}")
            ps_file.unlink()
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if ps_file.exists():
            ps_file.unlink()
        return False


if __name__ == '__main__':
    success = start_flask_simple()
    sys.exit(0 if success else 1)
