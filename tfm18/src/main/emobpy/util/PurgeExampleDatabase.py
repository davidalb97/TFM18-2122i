from tfm18.src.main.emobpy.util.EmobpyUtil import purge_database, fixed_set_seed


def main():
    fixed_set_seed()
    purge_database()


if __name__ == '__main__':
    main()
