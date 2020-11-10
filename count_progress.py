if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Return progress')
    parser.add_argument('--output', required=True,
                        help='output cell')
    args = parser.parse_args()
    sd = lambda a: len(a.replace(".",""))
    print(sd(args.output))