from json import JSONDecodeError
from django.test import TestCase
from core.models import Article, Tag, Category


class TestCoreUrls(TestCase):
    def setUp(self) -> None:
        """Create a test article"""
        # First we create a tag and a category
        self.tag = Tag.objects.create(name="Test Tag")
        self.category = Category.objects.create(name="Test Category")

        # Then we create an article
        self.article = Article.objects.create(
            title="Test Article",
            content="Test Content",
            description="Test Description",
            category=self.category,
        )

        # And add its tag
        self.article.tags.add(self.tag)

    def test_home(self):
        """Test that the root url returns a 404"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 404)

    def test_all_articles_endpoint_SUCCESS(self):
        """Test that the articles endpoint returns a 200"""
        response = self.client.get("/api/v1/articles/")
        self.assertEqual(response.status_code, 200)

    def test_all_articles_returned_JSON_format(self):
        """Test that the all articles endpoint returns
        the articles in the right json format"""
        response = self.client.get("/api/v1/articles/")

        # Check if response is proper json format
        self.assertEqual(response["Content-Type"], "application/json")

        try:
            response.json()
        except JSONDecodeError:
            self.fail("Response is not json")

    def test_all_articles_returned_good_data(self):
        """Test that the returned data has the right keys
        and values types"""

        response = self.client.get("/api/v1/articles/")

        data = response.json()

        # Only one article should be returned
        self.assertEqual(len(data), 1)

        # Check types
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
        self.assertIsInstance(data[0]["id"], int)
        self.assertIsInstance(data[0]["title"], str)
        self.assertIsInstance(data[0]["description"], str)
        # Tags
        self.assertIsInstance(data[0]["tags"], list)
        self.assertIsInstance(data[0]["tags"][0], str)
        
        # Category
        self.assertIsInstance(data[0]["category"], str)

        # Date is returned with stftime()
        self.assertIsInstance(data[0]["creation_date"], str)

        # And then data
        self.assertEqual(data[0]["id"], self.article.id)
        self.assertEqual(data[0]["title"], self.article.title)
        self.assertEqual(data[0]["description"], self.article.description)

        tag_names = list(self.article.tags.values_list("name", flat=True))
        self.assertEqual(data[0]["tags"], tag_names)
        
        self.assertEqual(data[0]["category"], self.article.category.name)

        self.assertEqual(
            data[0]["creation_date"], self.article.creation_date.strftime("%B %d, %Y")
        )

    def test_single_article_endpoint_NOT_FOUND(self):
        """Test that the single article endpoint returns a 404
        if the article does not exist"""
        response = self.client.get("/api/v1/article/5")

        # Article does not exist
        self.assertEqual(response.status_code, 404)

    def test_single_article_endpoint_SUCCESS(self):
        """Test that the single article endpoint returns a 200
        if the article exists"""

        article_id = self.article.id
        response = self.client.get(f"/api/v1/article/{article_id}")

        # Article does not exist
        self.assertEqual(response.status_code, 200)

    def test_single_article_returned_format(self):
        """Test that the single article endpoint returns
        the article in the right format"""

        article_id = self.article.id
        response = self.client.get(f"/api/v1/article/{article_id}")

        data = response.json()

        # Check types
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["id"], int)
        self.assertIsInstance(data["title"], str)
        self.assertIsInstance(data["description"], str)
        self.assertIsInstance(data["content"], str)

        # Tags
        self.assertIsInstance(data["tags"], list)
        self.assertIsInstance(data["tags"][0], str)
        
        # Category
        self.assertIsInstance(data["category"], str)

        # Date is returned with stftime()
        self.assertIsInstance(data["creation_date"], str)

        # And then data
        self.assertEqual(data["id"], self.article.id)
        self.assertEqual(data["title"], self.article.title)
        self.assertEqual(data["description"], self.article.description)

        tag_names = list(self.article.tags.values_list("name", flat=True))
        self.assertEqual(data["tags"], tag_names)
        
        self.assertEqual(data["category"], self.article.category.name)

        self.assertEqual(
            data["creation_date"], self.article.creation_date.strftime("%B %d, %Y")
        )


class TestCoreEndpoints(TestCase):
    pass
