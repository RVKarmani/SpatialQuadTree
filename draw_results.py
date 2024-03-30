import matplotlib.pyplot as plt
from argparse import ArgumentParser


def get_parser():
    parser = ArgumentParser()
    parser.add_argument("--task", type=str, default="m", choices=["m", "h", "t"], help="tree map, hitting rate, time")
    
    return parser



def draw_ht2num():
    """
    hitting rate to the number of data   

    Parameters:
    - hitting_rate: list
    - random_rate: list
    """
    print("Drawing hitting to random rate...")
    
    hitting_rate = []
    random_rate = []


def draw_t2r():
    """
    time to the random rate of data

    Parameters:
    - t_naive: list
    - t_bulk: list
    - random_rate: list
    """
    print("Drawing time to random rate...")
    
    t_naive = []
    t_bulk = []
    random_rate = []


def draw_tree():
    print("Drawing the tree map...")

    points = []


    
def main():
    args = get_parser().parse_args()
    if args.task == "m":
        draw_tree()
    elif args.task == "h":
        draw_ht2num()
    elif args.task == "t":
        draw_t2r()


if __name__ == "__main__":
    main()
