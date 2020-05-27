from main import app

# do not use this file for production use, only use for local running and testing of the application. Runs on port 8080 on local loopback

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
