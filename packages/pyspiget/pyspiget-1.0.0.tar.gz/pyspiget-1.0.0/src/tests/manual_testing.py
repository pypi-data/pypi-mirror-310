from src.pyspiget.spiget import Spiget, SpigetError

def main():
    spiget = Spiget()

    try:
        # Test get_status
        status = spiget.get_status()
        print("API Status:", status)

        # Test get_resources
        resources = spiget.get_resources(size=1)
        print("Resources:", resources)
        if resources:
            resource_id = resources[0].id

            # Test get_resource
            resource = spiget.get_resource(resource_id)
            print("Resource:", resource)

            # Test get_resource_versions
            resource_versions = spiget.get_resource_versions(resource_id, size=1)
            print("Resource Versions:", resource_versions)
            if resource_versions:
                version_id = resource_versions[0].id

                # Test get_resource_version
                resource_version = spiget.get_resource_version(resource_id, version_id)
                print("Resource Version:", resource_version)

                # Test get_resource_latest_version
                latest_version = spiget.get_resource_latest_version(resource_id)
                print("Latest Resource Version:", latest_version)

            # Test get_resource_updates
            resource_updates = spiget.get_resource_updates(resource_id, size=1)
            print("Resource Updates:", resource_updates)

            # Test get_resource_reviews
            resource_reviews = spiget.get_resource_reviews(resource_id, size=1)
            print("Resource Reviews:", resource_reviews)

            # Test get_resource_author
            resource_author = spiget.get_resource_author(resource_id)
            print("Resource Author:", resource_author)

        # Test get_authors
        authors = spiget.get_authors(size=5)
        print("Authors:", authors)
        if authors:
            author_id = authors[1].id # The first author is empty with id of -1 and name of "...", so we use the second one

            # Test get_author
            author = spiget.get_author(author_id)
            print("Author:", author)

            # Test get_author_resources
            author_resources = spiget.get_author_resources(author_id, size=1)
            print("Author Resources:", author_resources)

        # Test get_categories
        categories = spiget.get_categories(size=1)
        print("Categories:", categories)
        if categories:
            category_id = categories[0].id

            # Test get_category
            category = spiget.get_category(category_id)
            print("Category:", category)

            # Test get_category_resources
            category_resources = spiget.get_category_resources(category_id, size=1)
            print("Category Resources:", category_resources)

        # Test search_resources
        search_resources = spiget.search_resources(query="plugin", size=1)
        print("Search Resources:", search_resources)

        # Test search_authors
        search_authors = spiget.search_authors(query="author", size=1)
        print("Search Authors:", search_authors)

    except SpigetError as e:
        print("An error occurred:", e)


# Run from repo root with `PYTHONPATH=. python3 src/tests/manual_testing.py`
if __name__ == "__main__":
    main()
