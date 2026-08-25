import unittest

from coletar_precos import identificar_loja, limpar_preco, normalizar_url, termos_relevantes, url_de_produto


class TestColetor(unittest.TestCase):
    def test_identifica_lojas(self):
        self.assertEqual(identificar_loja("https://www.kabum.com.br/produto/123"), "KaBuM")
        self.assertEqual(identificar_loja("https://www.amazon.com.br/dp/ABC"), "Amazon")

    def test_normaliza_url(self):
        url = "https://www.kabum.com.br/produto/123"
        self.assertEqual(normalizar_url(f"  {url}  "), url)
        with self.assertRaises(ValueError):
            normalizar_url("kabum.com.br/produto/123")

    def test_limpa_preco(self):
        self.assertEqual(limpar_preco("R$ 2.499,90"), 2499.90)
        self.assertEqual(limpar_preco("2499.90"), 2499.90)
        self.assertIsNone(limpar_preco("indisponível"))

    def test_termos_relevantes(self):
        termos = termos_relevantes("GeForce RTX 4060 8GB Gaming")
        self.assertTrue({"4060", "8gb", "gaming"}.issubset(termos))

    def test_url_de_produto(self):
        self.assertTrue(url_de_produto("https://www.kabum.com.br/produto/123/gpu", "KaBuM"))
        self.assertFalse(url_de_produto("https://www.kabum.com.br/busca/gpu", "KaBuM"))


if __name__ == "__main__":
    unittest.main()
