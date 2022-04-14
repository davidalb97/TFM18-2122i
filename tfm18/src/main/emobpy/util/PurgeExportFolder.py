from tfm18.src.main.emobpy.util.EmobpyUtil import purge_export_folder, fixed_set_seed


def main():
    fixed_set_seed()
    purge_export_folder()


if __name__ == '__main__':
    main()
