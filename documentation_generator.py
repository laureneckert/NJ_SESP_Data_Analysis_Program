#NJSESP
#Lauren Eckert

import subprocess
import os
import shutil
import re

def generate_uml_diagrams(package_path, output_directory, project_name='MyProject'):
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Properly quote the package path
    quoted_package_path = f'"{package_path}"'

    # Build the pyreverse command
    pyreverse_cmd = f'pyreverse -o dot -p {project_name} {quoted_package_path} -a 2 -s 2'

    # Execute the pyreverse command in the package directory
    subprocess.run(pyreverse_cmd, shell=True, cwd=package_path)

    # Move the generated 'dot' files to the output directory
    dot_files = [file for file in os.listdir(package_path) if file.endswith('.dot')]
    for dot_file in dot_files:
        shutil.move(os.path.join(package_path, dot_file), os.path.join(output_directory, dot_file))

    # Convert 'dot' files to 'png' using the Graphviz 'dot' layout engine
    for dot_file in dot_files:
        full_dot_path = os.path.join(output_directory, dot_file)
        output_png = full_dot_path.replace('.dot', '.png')
        subprocess.run(['dot', '-Tpng', full_dot_path, '-o', output_png], shell=True)


# Example usage
path_to_package = r'C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\NJSESP_Data_Analysis_Program\NJ_SESP_Data_Analysis_Program'
path_to_output = r'C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\NJSESP_Data_Analysis_Program\NJ_SESP_Data_Analysis_Program\documentation'
generate_uml_diagrams(path_to_package, path_to_output)
