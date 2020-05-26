from main import app

# do not use this file for production use, only use for local running and testing of the application. Runs on port 8080

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
