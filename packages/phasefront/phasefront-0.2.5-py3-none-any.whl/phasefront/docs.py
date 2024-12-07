import sys
import webbrowser
from argparse import ArgumentParser
from importlib.resources import files

def open_docs(prefer_pdf: bool = False) -> int:
    """Open documentation in system browser.

    Args:
        prefer_pdf: If True, try PDF first before falling back to HTML

    Returns:
        0 on success, 1 on failure
    """
    html_path = files('phasefront') / 'docs' / 'site' / 'index.html'
    pdf_path = files('phasefront') / 'docs' / 'PQ strEEm Python doc.pdf'

    if prefer_pdf:
        paths = [(pdf_path, "PDF"), (html_path, "HTML")]
    else:
        paths = [(html_path, "HTML"), (pdf_path, "PDF")]

    for path, format in paths:
        if path.exists():
            url = f"file://{path}"
            if webbrowser.open(url):
                return 0
            print(f"Error: Could not open {format} documentation", file=sys.stderr)

    print("Error: Documentation not found", file=sys.stderr)
    return 1

def main(argv: list[str] = sys.argv[1:]) -> int:
    parser = ArgumentParser(description="Open PhaseFront documentation in browser")
    parser.add_argument('--pdf', action='store_true',
                       help="prefer PDF format over HTML")
    args = parser.parse_args(argv)
    return open_docs(prefer_pdf=args.pdf)

if __name__ == '__main__':
    sys.exit(main())