import os, shutil

def copy_dir(source_path:str, dest_path:str) -> None:
    elements = os.listdir(source_path)
    print(elements)

    for ele in elements:
        if os.path.isfile(f"{source_path}/{ele}"):
            #print("copying file: ", ele)
            shutil.copy(f"{source_path}/{ele}",f"{dest_path}/{ele}")

        else:
            #print("copying dir: ", ele)
            os.mkdir(f"{dest_path}/{ele}")
            copy_dir(f"{source_path}/{ele}", f"{dest_path}/{ele}")