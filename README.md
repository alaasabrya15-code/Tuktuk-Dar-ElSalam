
name: Extract game ZIP

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  extract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Extract ZIP
        run: |
          sudo apt-get update
          sudo apt-get install -y unzip
          mkdir -p extracted
          unzip -o grok-workspace.zip -d extracted
          find extracted -type f | sort | head -300

      - name: Save extracted files
        uses: actions/upload-artifact@v4
        with:
          name: extracted-game-project
          path: extracted/
          retention-days: 7
