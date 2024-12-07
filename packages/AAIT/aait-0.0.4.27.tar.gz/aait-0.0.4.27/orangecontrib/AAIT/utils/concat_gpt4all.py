# lucas va coder pour obtenir le chemin en sys.executable - remonter dossier a coté orange
# void -> string
import sys
import os
import shutil
import zipfile
import time
if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\","/"):
    from Orange.widgets.orangecontrib.AAIT.llm import GPT4ALL
else:
    from orangecontrib.AAIT.llm import GPT4ALL


def get_target_path(target="gpt4all"):
    python_path = sys.executable.replace("\\","/")
    dir_path = os.path.dirname(os.path.dirname(python_path))
    dir_path = dir_path+"/"+ target
    return dir_path

def get_list_file_to_copy_past():
    #C:\test_bug_orange\Orange_test_4all\Lib\site - packages\gpt4all - pypi - part1
    python_path = sys.executable.replace("\\","/")
    dir_path = os.path.dirname(python_path)
    dir_path=dir_path+"/lib/site-packages/"
    result=[]
    result.append(dir_path+"gpt4all-pypi-part1/gpt4all/gpt4all.zip.001")
    result.append(dir_path+"gpt4all-pypi-part2/gpt4all/gpt4all.zip.002")
    result.append(dir_path+"gpt4all-pypi-part3/gpt4all/gpt4all.zip.003")
    result.append(dir_path+"gpt4all-pypi-part4/gpt4all/gpt4all.zip.004")
    result.append(dir_path+"gpt4all-pypi-part5/gpt4all/gpt4all.zip.005")
    result.append(dir_path+"gpt4all-pypi-part6/gpt4all/gpt4all.zip.006")
    result.append(dir_path+"gpt4all-pypi-part7/gpt4all/gpt4all.zip.007")
    result.append(dir_path+"gpt4all-pypi-part8/gpt4all/gpt4all.zip.008")
    result.append(dir_path+"gpt4all-pypi-part9/gpt4all/gpt4all.zip.009")
    result.append(dir_path+"gpt4all-pypi-part10/gpt4all/gpt4all.zip.010")
    result.append(dir_path+"gpt4all-pypi-part11/gpt4all/gpt4all.zip.011")
    return result


# une focntion qui check que toute est ok
def check_if_everithing_is_ready_to_unzip():
    if os.path.isdir(get_target_path("gpt4all"))==False:
        print(get_target_path("gpt4all"))
        print("output dir not exist")
        return False
    python_path = sys.executable.replace("\\", "/")
    list_to_copy=get_list_file_to_copy_past()
    for element in list_to_copy:
        if os.path.isfile(element)==False:
            print(element+" not exist")
            return False
    return True


def copier_fichier(source, destination):
    with open(source, 'rb') as fsrc:
        with open(destination, 'wb') as fdst:
            fdst.write(fsrc.read())


# fonction_a_coder pour les copier coller
def copier_dossier(source, destination):

    # Créer le dossier de destination s'il n'existe pas
    os.makedirs(destination, exist_ok=True)
    destination_path = os.path.join(destination, os.path.basename(source))

    if os.path.isdir(source):
        print("dossier")
        copier_dossier(source, destination_path)
    else:
        print("fichier")
        copier_fichier(source, destination_path)




# focntion qui dezip sans 7 zip
def find_zip_parts(base_directory):
    # List to store paths of found zip parts
    zip_parts = []

    # Walk through all subdirectories and locate the .zip.001 files
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.startswith("gpt4all.zip.00"):
                zip_parts.append(os.path.join(root, file))



    # Sort by folder name since parts are in different directories
    zip_parts.sort()
    return zip_parts


def merge_and_unzip(zip_parts, output_zip):
    # Merge all the found zip parts into one file
    with open(output_zip, 'wb') as merged_zip:
        for part in zip_parts:
            with open(part, 'rb') as part_file:
                shutil.copyfileobj(part_file, merged_zip)

    # Unzip the merged zip file
    with zipfile.ZipFile(output_zip, 'r') as zip_ref:
        extract_dir = os.path.splitext(output_zip)[0]  # Create folder based on zip name
        zip_ref.extractall(extract_dir)
        print(f"Extracted to: {extract_dir}")

def test_if4all_need_to_be_installed():
    if os.path.isfile(GPT4ALL.get_gpt4all_exe_path()):
        return False
    python_path = sys.executable.replace("\\","/")
    dir_path = os.path.dirname(python_path)
    dir_path=dir_path+"/lib/site-packages/"
    if os.path.isfile(dir_path+"gpt4all-pypi-part1/gpt4all/gpt4all.zip.001")==False:
        return False
    return True

def unzip_gpt4all_if_needed():
    if False==test_if4all_need_to_be_installed():
        return

    if os.name!='nt':
        print("only for windows")
        return

    target_path = get_target_path()
    if os.path.isdir(target_path):
        shutil.rmtree(target_path)
        time.sleep(0.5)

    os.makedirs(target_path, exist_ok=True)
    list_file = get_list_file_to_copy_past()

    if check_if_everithing_is_ready_to_unzip()!=True:
        print("an error occurs")
        return
    if list_file != []:
        for elem in list_file:
            copier_dossier(elem, target_path)

    zip_parts = find_zip_parts(target_path)
    #merge_and_unzip(zip_parts, os.path.join(target_path, "gpt.zip"))
    time.sleep(0.5)
    # Chemin vers le premier fichier .zip.001
    archive_path = target_path+"/gpt4all.zip.001"
    filenames = [target_path+"/gpt4all.zip.001", target_path+"/gpt4all.zip.002",target_path+"/gpt4all.zip.003",target_path+"/gpt4all.zip.004",target_path+"/gpt4all.zip.005",target_path+"/gpt4all.zip.006",target_path+"/gpt4all.zip.007",target_path+"/gpt4all.zip.008",target_path+"/gpt4all.zip.009",target_path+"/gpt4all.zip.010",target_path+"/gpt4all.zip.011"]
    with open(target_path+'/result.zip', 'ab') as outfile:# append in binary mode
        for fname in filenames:
            with open(fname, 'rb') as infile:  # open in binary mode also
                outfile.write(infile.read())
                time.sleep(1)

    with zipfile.ZipFile(target_path+'/result.zip', 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(target_path))

    # Clear useless .zip files
    for filename in filenames:
        if os.path.exists(filename):
            os.remove(filename)
    if os.path.exists(target_path+"/result.zip"):
        os.remove(target_path+"/result.zip")


if __name__ == "__main__":
    unzip_gpt4all_if_needed()