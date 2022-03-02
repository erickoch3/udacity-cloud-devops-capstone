from cn_news_cluster.web import app


def main():
    try:
        app.run(host='0.0.0.0', port=80, debug=False) 
    except KeyboardInterrupt:
        print("\nUser interrupted session.\n")

if __name__ == "__main__":
    main()
