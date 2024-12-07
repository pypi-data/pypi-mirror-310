import requests
import sys
import datetime
from packaging import version
import os
import argparse

def find_packages_versions(package_name:str):
  url = f"https://pypi.org/pypi/{package_name}/json"
  data = requests.get(url).json()
  versions = list(data["releases"].keys())
  return versions


def get_latest_version(package_versions) -> str:
  if len(package_versions) == 1:
    return package_versions[0]

  
  versions = [version.parse(v) for v in package_versions]
  return str(max(versions))
        
      
  


def main(smart_requirements_path:str) -> None:
  # load packages and load as list
  try:
    smart_requirements_txt = open(smart_requirements_path, "r")
  except FileNotFoundError as e:
    print(e)
    return
    
  packages = smart_requirements_txt.readlines()
  updated_packages:str = f"# Updated with SmartPIP at {datetime.datetime.now()} https://github.com/L1Lbg/SmartPIP \n"

  # loop through packages
  for package in packages:
    # get all available versions of that package
    package_versions = find_packages_versions(package.split("==")[0])
    # and the user desired version
    desired_version = package.split("==")[1]
    #if user only wants the latest version
    if desired_version == "latest":
      updated_packages += f"{package.split('==')[0]}=={get_latest_version(package_versions)}\n"
      continue
    #if user wants a specific version but with the latest fragmented version
    elif "latest" in desired_version:
      # fragment the version
      fragments = desired_version.strip()
      fragments = fragments.split(".")
      # if latest is misplaced, raise error
      if fragments[-1] != "latest":
        raise Exception(f"You can only declare latest for the last fragment of the version. Package: {package}")

      # get the numerical version before it has to be automatically set to the latest
      num_version = desired_version.replace("latest","").strip()
      candidate_versions = list()
      for version in package_versions:
        # if version matches with first numbers specified by user
        if str(version).strip().startswith(str(num_version)):
          candidate_versions.append(version)

      # of all the possible packages, choose the most recent one
      updated_packages += f"{package.split('==')[0]}=={get_latest_version(candidate_versions)}\n"
      continue
        
    # if user wants a specific version
    else:
      updated_packages += f"{package}\n"
      continue

  requirements_dir = os.path.dirname(smart_requirements_path)  
  requirements_file_path = os.path.join(requirements_dir, "requirements.txt")  
  open(requirements_file_path, "w").write(updated_packages)


  



def cli():
    parser = argparse.ArgumentParser(description="Path to your smart_requirements.txt file")
    parser.add_argument('--file', type=str, help='Path to your smart_requirements.txt file', required=True)
    args = parser.parse_args()
    main(smart_requirements_path=args.file)

if __name__ == "__main__":
    cli()