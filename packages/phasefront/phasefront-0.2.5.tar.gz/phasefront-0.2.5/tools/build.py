import os
import sys
import inspect
import subprocess
import yaml
import tempfile

SRC_FOLDER = "phasefront"

def build_docs(version=None):
    try:
        # Ensure docs directory exists
        docs_dir = os.path.join(SRC_FOLDER, "docs")
        docs_src = os.path.join(docs_dir, "src")
        os.makedirs(docs_dir, exist_ok=True)

        # Define target paths
        target_path = os.path.join(docs_dir, 'PQ strEEm Python doc.pdf')
        version_path = os.path.join(docs_dir, '.doc_version')
        final_site_dir = os.path.join(docs_dir, 'site')  # Final site location

        # Define CSS content for PDF styling
        css_content = """
@page {
    size: letter portrait;
    margin: 20mm 20mm 20mm 20mm !important;  /* top right bottom left */

     @top-right {
       content: string(chapter);
       font-size: 9pt !important;
    }

    @bottom-center {
        content: string(copyright) !important;
        font-size: 9pt !important;
    }

    @bottom-right {
        content: counter(page) !important;
        font-size: 9pt !important;
    }
}

/* Define theme color variable */
:root > * {
    --md-primary-fg-color: #074CDF;
    --md-primary-fg-color--light: #0773FC;
    --md-primary-fg-color--dark: #074CDF;
}

#doc-toc * {
    border-color: var(--md-primary-fg-color--light) !important;
}

article h1,
article h2,
article h3 {
    border-color: var(--md-primary-fg-color) !important;
}

/* Content margins */
.md-grid {
    max-width: 85% !important;
}

div.col-md-9 h1:first-of-type {
    text-align: center;
    font-size: 10px;
    font-weight: 300;
}

article h1 {
    font-size: 10px;
}

.md-content {
    margin: 0 3rem !important;
}

.md-header {
    margin-left: 20mm;
    margin-right: 20mm;
}

.md-footer {
    margin-left: 20mm;
    margin-right: 20mm;
}

.md-nav__list * {
    border-color: var(--md-primary-fg-color) !important;
}

/* Keep other formatting rules */
body { counter-reset: page 1; }
article { page-break-after: always; }
h1, h2, h3 { page-break-after: avoid; }
pre { page-break-inside: avoid; }
"""

        # Create temp directory for build output
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_docs_src = os.path.join(temp_dir, 'docs', 'src')
            temp_site = os.path.join(temp_dir, 'site')  # Temporary build location
            os.makedirs(temp_docs_src, exist_ok=True)

            # Copy docs content to temp directory
            import shutil
            for item in os.listdir(docs_src):
                src = os.path.join(docs_src, item)
                dst = os.path.join(temp_docs_src, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            # Copy assets
            temp_assets = os.path.join(temp_dir, 'docs', 'assets')
            shutil.copytree(os.path.join(docs_dir, 'assets'), temp_assets)

            # Write CSS file
            css_path = os.path.join(temp_docs_src, 'custom.css')
            with open(css_path, 'w') as f:
                f.write(css_content)

            # Create mkdocs config
            config_path = os.path.join(temp_dir, 'mkdocs.yml')

            # Create mkdocs.yml in temp directory
            mkdocs_config = {
                'docs_dir': temp_docs_src,
                'site_dir': temp_site,  # Build in temp directory first
                'nav': [
                    {'Home': 'index.md'},
                    {'Development': 'development.md'}
                ],
                'plugins': [
                    'search',
                    {
                        'with-pdf': {
                            'output_path': 'PQ strEEm Python doc.pdf',
                            'cover_title': 'PQ strEEm Exploratory Data Analysis',
                            'cover_subtitle': "'phasefront' Python package",
                            'cover_logo': os.path.abspath(os.path.join(temp_assets, 'logo.png')),  # Use temp assets path
                            'author': f"Version {version}",  # Use passed version parameter
                            'toc_level': 3
                        }
                    }
                ],
                'site_name': "PQ strEEm Data Analysis",
                'site_description': "phasefront Python package",
                'copyright': "© 2024 PhaseFront and Renewable Edge LLC",
                'theme': {
                    'name': 'material',
                    'features': [
                        'navigation.sections',
                        'navigation.expand'
                    ],
                    'logo': 'assets/logo.png',
                    'favicon': 'assets/logo.png'
                },
                'use_directory_urls': False,
                'extra_css': ['custom.css']
            }

            # Write config
            with open(config_path, 'w') as f:
                yaml.dump(mkdocs_config, f)

            # Run mkdocs build
            env = os.environ.copy()
            env['ENABLE_PDF_EXPORT'] = '1'
            subprocess.run(["mkdocs", "build", "-f", config_path], check=True, env=env)

            # Copy the entire site directory to final location
            if os.path.exists(final_site_dir):
                shutil.rmtree(final_site_dir)
            os.makedirs(os.path.dirname(final_site_dir), exist_ok=True)
            shutil.copytree(temp_site, final_site_dir)

            # Copy generated PDF if it exists
            pdf_path = os.path.join(temp_site, 'PQ strEEm Python doc.pdf')
            if os.path.exists(pdf_path):
                shutil.copy2(pdf_path, target_path)
                with open(version_path, 'w') as f:
                    f.write(version)
            else:
                raise FileNotFoundError("PDF was not generated in expected location")

    except Exception as e:
        print(f"\nError building documentation: {e}", file=sys.stderr)
        print("Documentation will not be included in the package.\n", file=sys.stderr)

def get_version_from_git(fallback: str | None = None) -> str:
    """Get version from git tags, for editable installs only."""
    try:
        # Get the git describe output (including dirty state)
        result = subprocess.run(
            ["git", "describe", "--tags", "--dirty"],
            capture_output=True,
            text=True,
            check=True,
            cwd=os.path.dirname(__file__)
        )
        version = result.stdout.strip()

        # Strip 'v' prefix and convert to PEP 440
        if version.startswith('v'):
            version = version[1:]

        # Handle release candidates and dev versions separately
        if 'rc' in version:
            # Split into base version and rc part
            base, rc = version.split('rc', 1)
            if '-' in rc:  # Has dev commits after rc
                rc_num, dev = rc.split('-', 1)
                # Convert git describe format to PEP 440 dev format
                if '-g' in dev:
                    count = dev.split('-')[0]
                    hash = dev.split('-g')[1].split('.')[0]  # Handle potential .dirty suffix
                    version = f"{base}rc{rc_num}.dev{count}+g{hash}"
                else:
                    version = f"{base}rc{rc_num}"
            else:
                version = f"{base}rc{rc}"
        else:
            # Handle regular versions with safer parsing
            parts = version.split('-')
            if len(parts) > 1:
                base = parts[0]
                if len(parts) >= 3 and parts[-2].startswith('g'):
                    # Standard git describe format
                    dev_count = parts[-3]
                    git_hash = parts[-2][1:]  # Remove 'g' prefix
                    version = f"{base}.dev{dev_count}+{git_hash}"
                else:
                    # Simpler format or unknown
                    version = base
            else:
                version = parts[0]

        return version.replace('_', '+')

    except subprocess.CalledProcessError:
        if fallback is None:
            print("\nError: Could not get version from git!", file=sys.stderr)
            print("This could mean:", file=sys.stderr)
            print("1. git is not installed", file=sys.stderr)
            print("2. This is not a git repository", file=sys.stderr)
            print("3. No git tags exist yet", file=sys.stderr)
            print("\nPlease either:", file=sys.stderr)
            print("1. Install git and tag a version (git tag v0.1.0)", file=sys.stderr)
            print("2. Provide a fallback version number", file=sys.stderr)
            raise
        print("\nWarning: Could not get version from git.", file=sys.stderr)
        print("This is normal for editable installs without git version control.", file=sys.stderr)
        return fallback

def get_version():
    """Get version without triggering documentation build."""
    if any('editable' in arg for arg in sys.argv):
        return get_version_from_git("0.0.0")

    version_file = os.path.join(SRC_FOLDER, "_version.py")
    if not os.path.exists(version_file):
        print("\nError: _version.py not found!", file=sys.stderr)
        print("Please ensure version is tagged and run build.sh:", file=sys.stderr)
        print("1. Check current version: git describe --tags", file=sys.stderr)
        print("2. Add tag if needed, e.g.: git tag v0.2.2", file=sys.stderr)
        print("3. Build all components from the root of the repo: ./build.sh\n", file=sys.stderr)
        sys.exit(1)

    namespace = {}
    with open(version_file) as f:
        exec(f.read(), globals(), namespace)

    if '__version__' not in namespace:
        print("\nError: Invalid _version.py file!", file=sys.stderr)
        print("The file exists but doesn't define __version__.", file=sys.stderr)
        print("Please rebuild the package using ./build.sh\n", file=sys.stderr)
        sys.exit(1)

    return namespace['__version__']

def get_and_write_version_and_docs():
    """Version getter and build handler for setuptools."""
    # Get version first
    version = get_version()

    # Write version file if needed
    if any('editable' in arg for arg in sys.argv):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        version_file = os.path.join(project_root, SRC_FOLDER, "_version.py")
        os.makedirs(os.path.dirname(version_file), exist_ok=True)
        with open(version_file, "w") as f:
            f.write('# This file is auto-generated by build_version.py. DO NOT EDIT!\n')
            f.write('import os\n')
            f.write('import subprocess\n')
            f.write('import sys\n\n')
            f.write(inspect.getsource(get_version_from_git))
            f.write(f'\n__version__ = "{version}"\n')

    # Only build docs during sdist
    if 'sdist' in sys.argv:
        try:
            build_docs(version)  # Pass the version explicitly
        except Exception as e:
            print(f"\nWarning: Failed to build documentation: {e}", file=sys.stderr)
            print("Documentation will not be included in the package.\n", file=sys.stderr)

    return version
