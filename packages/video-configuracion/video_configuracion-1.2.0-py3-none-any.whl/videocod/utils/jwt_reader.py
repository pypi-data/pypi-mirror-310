def read_jwt_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            jwt_token = file.read().strip()
        return jwt_token
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError as e:
        print(f"Error reading file: {e}")
