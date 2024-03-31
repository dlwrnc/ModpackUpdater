import update_modpack


def get_pack_type():
    print("If you're updating data packs, please type 'data'. "
          "If you're updating resource packs, please type 'resource'")
    pack_type = input()
    if 'data' in pack_type:
        return False
    if 'resource' in pack_type:
        return True
    else:
        print(f"Input {pack_type} is invalid. If you're updating data packs, "
              f"please type 'data'. If you're update resource packs, "
              f"please type 'resource'")
        return get_pack_type()


def get_pack_format():
    print("Please enter the raw pack format to update to if you would like to"
          " use pack format. (A 'pack format' is usually a single integer.) "
          "If you want to use a target minecraft revision to be compatible "
          "with, or simply update to latest, just hit enter.")
    pack_format = input()
    return pack_format


def get_target_revision():
    print("Please enter the revision of minecraft to update to. If you "
          "just want to update to latest, hit enter.")
    target_revision = input()
    return target_revision


def get_filepaths():
    inp = 'blank'
    filepaths = []
    while inp != '':
        print("Please enter the filepath or filepath(s) of the zipfiles to update,"
              " hitting enter after each one. Please enter a blank space once"
              " you are finished. If you want to update all of the zipfiles"
              " in a single directory, just enter the directory path.")
        inp = input()
        if inp != '':
            filepaths.append(inp)
    return filepaths


if __name__ == '__main__':
    print("Welcome to minecraft updater.")
    is_resource_pack = get_pack_type()
    pack_format = get_pack_format() or 0
    target_rev = get_target_revision() or ""
    filepaths = get_filepaths()
    pack_type = {"resource pack" if is_resource_pack else "data pack"}
    print(f'pack type: {pack_type}')
    print(f'target_rev: {target_rev}')
    print(f'pack_format: {pack_format}')
    print(f'filepaths: {filepaths}')

    updater = update_modpack.UpdateModpack(filepaths, target_rev, pack_format, pack_type)
