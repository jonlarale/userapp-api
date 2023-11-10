from api import create_api
from conf import cfg

api = create_api()

if __name__ == "__main__":
    api.run(host="0.0.0.0", port=cfg.PORT)