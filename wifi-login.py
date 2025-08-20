import subprocess
import time
import sys
import urllib.request
import urllib.parse

# Your credentials
USERNAME = "email"
PASSWORD = "password"

DEFAULT_REFRESH_HOURS = 11

def logout():
    """Logout from the portal"""
    try:
        data = urllib.parse.urlencode({'erase-cookie': 'on', 'submit': ''}).encode()
        req = urllib.request.Request(
            'https://portal.91springboard.com/logout',
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        with urllib.request.urlopen(req) as response:
            response_text = response.read().decode()
            print(f"Logout response status: {response.status}")
            print(f"Logout response: {response_text}")
            return response.status == 200
    except Exception as e:
        print(f"Logout failed: {e}")
        return False

def login():
    """Login to the portal"""
    try:
        data = urllib.parse.urlencode({
            'dst': 'https://91springboard.com',
            'popup': 'true',
            'username': f'{USERNAME}',
            'password': f'{PASSWORD}'
        }).encode()
        req = urllib.request.Request(
            'https://portal.91springboard.com/login',
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        with urllib.request.urlopen(req) as response:
            response_text = response.read().decode()
            print(f"Login response status: {response.status}")
            print(f"Login response: {response_text}")
            return response.status == 200
    except Exception as e:
        print(f"Login failed: {e}")
        return False


def main():
    # Parse CLI args
    refresh_hours = DEFAULT_REFRESH_HOURS
    if len(sys.argv) > 1:
        try:
            refresh_hours = float(sys.argv[1])
        except ValueError:
            print("[WARN] Invalid argument, using default 11 hrs")
            refresh_hours = DEFAULT_REFRESH_HOURS

    # If 0 is passed → run immediately once, then reset to default
    if refresh_hours == 0:
        logout()
        login()
        print(f"[INFO] Logged in successfully...")
        print(f"[INFO] Immediate refresh done. Next cycle will use {DEFAULT_REFRESH_HOURS} hours.")
        refresh_hours = DEFAULT_REFRESH_HOURS

    while True:
        logout()
        login()
        print(f"[INFO] Logged in successfully...")
        print(f"[INFO] Next refresh in {refresh_hours} hours...")

        # Sleep loop (minute chunks so it’s interruptible)
        for _ in range(int(refresh_hours * 60)):
            time.sleep(60)


if __name__ == "__main__":
    main()
