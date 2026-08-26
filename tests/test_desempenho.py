import unittest

from desempenho import adicionar_indice_radar, carregar_base_tecnica


class TestDesempenho(unittest.TestCase):
    def setUp(self):
        self.base = carregar_base_tecnica()

    def test_base_tem_fontes_e_metricas_validas(self):
        self.assertEqual(len(self.base), 7)
        self.assertFalse(self.base["Fonte_Benchmark"].str.strip().eq("").any())
        self.assertFalse(self.base["Fonte_Especificacoes"].str.strip().eq("").any())
        self.assertTrue((self.base["FPS_1080p"] >= self.base["FPS_1440p"]).all())

    def test_indice_fica_entre_zero_e_cem(self):
        for foco in ("Gamer 1080p", "Gamer 1440p", "Jogos + streaming"):
            resultado = adicionar_indice_radar(self.base, foco)
            self.assertTrue(resultado["Score"].between(0, 100).all())

    def test_4070_super_lidera_desempenho_raster(self):
        lider = self.base.sort_values("FPS_1440p", ascending=False).iloc[0]
        self.assertEqual(lider["GPU"], "GeForce RTX 4070 SUPER 12GB")

    def test_b580_supera_4060_em_1440p_raster(self):
        fps = self.base.set_index("GPU")["FPS_1440p"]
        self.assertGreater(fps["Intel Arc B580 12GB"], fps["GeForce RTX 4060 8GB"])


if __name__ == "__main__":
    unittest.main()

