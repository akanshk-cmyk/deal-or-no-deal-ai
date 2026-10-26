"""Retired local-weight setup entry point; ADR-008 selects hosted embeddings."""


def main():
    # Stop before filesystem, environment, optional import or network work.
    raise SystemExit("LOCAL_EMBEDDINGS_RETIRED: Nebius hosted setup is pending; no download performed.")


if __name__ == "__main__":
    main()
