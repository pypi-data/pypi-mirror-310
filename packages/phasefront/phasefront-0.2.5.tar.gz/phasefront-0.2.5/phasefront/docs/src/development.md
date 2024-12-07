# Development Guide

## Getting Started

Clone and install in development mode:
```bash
git clone https://github.com/edge-energy/streem.git
cd phasefront
pip install -e .
```

## Version Management

The package version is managed automatically using git tags. Here's how it works:

### Development Mode

When installed with `pip install -e .`:
- Version is dynamically fetched from git tags
- Changes to code take effect immediately
- Supports version formats:
  ```
  v0.1.2      # Release version
  v0.1.2rc1   # Release candidate
  v0.2.2_ti   # Variant (adds +ti suffix)
  ```
- Development versions show commits since last tag:
  ```
  0.1.2+dev5.gabc123f  # 5 commits after v0.1.2
  0.1.2+dev5.gabc123f.dirty  # Uncommitted changes
  ```

### Release Mode

For building releases:
```bash
# Tag the version you want to release
git tag v0.2.2 # or v0.2.2_xx for variants

#Generate version file and build package
./build.sh
```

Important notes:
- Working directory must be clean (no uncommitted changes)
- Version is frozen in .build_version.txt during build
- Dirty working directory will cause build errors

## Common Issues

1. Build fails with version error:
   - Ensure you've run `./build.sh`
   - Check that git tags are correct
   - Commit or stash changes

2. Version shows as "dirty":
   - Only allowed in development mode
   - Commit or stash changes before release

3. Wrong version appearing:
   - Check current git tag (`git describe --tags`)
   - Ensure you're on the right branch