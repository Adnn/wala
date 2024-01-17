def load_env_file(file_path=".env"):
    env_dict = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Ignore comments and empty lines
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    env_dict[key] = value
    except FileNotFoundError:
        pass
    return env_dict
