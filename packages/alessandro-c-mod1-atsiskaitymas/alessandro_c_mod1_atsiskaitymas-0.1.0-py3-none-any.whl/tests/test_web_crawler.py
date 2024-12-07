import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from alessandro_c_mod1_atsiskaitymas.web_crawler import web_crawler


class TestWebCrawler(unittest.TestCase):

    @patch('requests.get')
    @patch('lxml.html.fromstring')
    @patch('csv.DictWriter')
    def test_save_to_csv(self, mock_csv_writer, mock_fromstring, mock_get):
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.text = '<html><body><div class="product-item"><input name="productName" value="Product 1"/><input name="productPrice" value="10.99"/><input name="productBrand" value="Brand A"/></div></body></html>'
        mock_get.return_value = mock_response

        mock_tree = MagicMock()
        mock_tree.xpath.return_value = [
            MagicMock(
                xpath=lambda x: ["Product 1"] if "productName" in x else ["10.99"] if "productPrice" in x else ["Brand A"]
            )
        ]
        mock_fromstring.return_value = mock_tree

        mock_csv_file = StringIO()
        mock_csv_writer.return_value = MagicMock(writeheader=MagicMock(), writerows=MagicMock())

        web_crawler(url="https://www.gintarine.lt/maistas-ir-papildai-sportininkams", timeout=60, output_format="csv")

        mock_csv_writer.assert_called()
        mock_csv_writer.return_value.writeheader.assert_called_once()
        mock_csv_writer.return_value.writerows.assert_called_once()

    @patch('requests.get')
    @patch('lxml.html.fromstring')
    def test_invalid_url(self, mock_fromstring, mock_get):
        mock_get.side_effect = Exception("Network error")

        result = web_crawler(url="https://invalid-url", timeout=60, output_format="dict")

        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()