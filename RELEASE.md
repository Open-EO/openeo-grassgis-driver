Steps when releasing openeo-grassgis-driver:

## 1. Prepare release and version
* Run in terminal
    ```
    ESTIMATED_VERSION=2.5.1

    gh api repos/Open-EO/openeo-grassgis-driver/releases/generate-notes -f tag_name="$ESTIMATED_VERSION" -f target_commitish=main -q .body
    ```
* Go to https://github.com/Open-EO/openeo-grassgis-driver/releases/new
* Copy the output of terminal command to the release description
* Change heading `## What's Changed` to `### Changed`, `### Fixed`, `### Added` or what applicable and sort list amongst these headings.
* You can [compare manually](https://github.com/Open-EO/openeo-grassgis-driver/compare/2.5.1...2.5.0) if all changes are included. If changes were pushed directly to main branch, they are not included.
* Check if `ESTIMATED_VERSION` increase still fits - we follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
* Fill in tag and release title with this version
* At the bottom of the release, add
  "generated with `gh api repos/Open-EO/openeo-grassgis-driver/releases/generate-notes -f tag_name="$ESTIMATED_VERSION" -f target_commitish=main -q .body`" and replace `$ESTIMATED_VERSION` with the actual version.

## 3. Release
* Now you can save the release

## 4. Update changelog
* Run in terminal
    ```
    curl https://api.github.com/repos/Open-EO/openeo-grassgis-driver/releases/latest | jq -r '. | "## [\(.tag_name)] - \(.published_at | strptime("%Y-%m-%dT%H:%M:%SZ") | strftime("%Y-%m-%d"))\nreleased from \(.target_commitish)\n\(.body) \n"'
    ```
* Copy the output to the top of the release list in [CHANGELOG.rst](https://github.com/Open-EO/openeo-grassgis-driver/blob/main/CHANGELOG.rst)
* Push changes in CHANGELOG.rst to main branch
