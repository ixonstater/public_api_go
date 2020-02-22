from src.resources import instance

def main(global_config, **settings):
    inst = instance.Instance()
    return inst.initServer()
