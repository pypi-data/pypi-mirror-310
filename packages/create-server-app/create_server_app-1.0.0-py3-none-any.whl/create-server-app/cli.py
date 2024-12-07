import argparse
from create_server import create_server_app

def main():
    parser = argparse.ArgumentParser(description="Create a server app project.")
    parser.add_argument("name", type=str, help="The name of your project folder.")
    args = parser.parse_args()

    create_server_app(args.name)

if __name__ == "__main__":
    main()
