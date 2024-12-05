import os
import argparse
import configparser

def run_command(command):
    result = os.system(command)
    if result != 0:
        print(f"Command failed with exit code {result}")
        exit(result)

def parse_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return {
        'source_dir': config['CBUILD'].get('source_dir', ''),
        'sources': config['CBUILD'].get('sources', '').split(','),
        'defines': config['CBUILD'].get('defines', '').split(','),
        'output_type': config['CBUILD'].get('output_type', 'exe'),
        'output_dir': config['CBUILD'].get('output_dir', 'build/'),
        'libraries': config['CBUILD'].get('libraries', '').split(','),
        'project_name': config['CBUILD'].get('project_name', 'MyProject'),
        'include_dirs': config['CBUILD'].get('include_dirs', '').split(','),
        'library_dirs': config['CBUILD'].get('library_dirs', '').split(',')
    }

def collect_source_files(source_dir):
    source_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.c'):
                source_files.append(os.path.join(root, file))
    return source_files

def build_project(config):
    project_name = config['project_name']
    print(f"[CBUILD] : Building Project `{project_name}`\n")
    sources = config['sources']
    defines = config['defines']
    libraries = config['libraries']
    source_dir = config['source_dir']
    output_dir = config['output_dir']
    output_type = config['output_type']
    include_dirs = config['include_dirs']
    library_dirs = config['library_dirs']

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if source_dir:
        sources += collect_source_files(source_dir)

    object_files = []
    for source in sources:
        source = source.strip()
        if source:
            object_file = os.path.join(output_dir, os.path.basename(source).replace('.c', '.o'))
            include_flags = " ".join([f"-I{dir.strip()}" for dir in include_dirs if dir.strip()])
            run_command(f"gcc -c {source} {include_flags} -o {object_file}")
            object_files.append(object_file)

    c_defines = "".join([f"-D{define.strip()} " for define in defines if define.strip()])
    link_flags = " ".join([f"-l{lib.strip()}" for lib in libraries if lib.strip()])
    library_flags = " ".join([f"-L{lib_dir.strip()}" for lib_dir in library_dirs if lib_dir.strip()])
    object_files_str = " ".join(object_files)

    if output_type == 'exe':
        run_command(f"gcc {c_defines} {object_files_str} {library_flags} {link_flags} -o {output_dir}/{project_name}.exe")
    elif output_type == 'dll':
        run_command(f"gcc -shared {object_files_str} {library_flags} {link_flags} -o {output_dir}/{project_name}.dll")
    elif output_type == 'static_lib':
        run_command(f"ar rcs {output_dir}/{project_name}.a {object_files_str}")

    for file in object_files:
        run_command(f"del {file.replace("/", "\\")}")
    
    print(f"[CBUILD] : Built Project `{project_name}` At `{output_dir}`\n")

def main():
    parser = argparse.ArgumentParser(description="CBUILD - A Simple C Build Tool")
    parser.add_argument('config', help="Path to the .cbuild configuration file")
    args = parser.parse_args()

    config = parse_config(args.config)

    build_project(config)

