-- Cria uma view com os pinguins da tabela pública e uma coluna de split.
-- 80% vai para treino, 20% para teste. O hash deixa a divisão fixa: roda de novo, dá o mesmo resultado.
CREATE OR REPLACE VIEW `gdg_blumenau.pinguins_base` AS
SELECT
  species,
  island,
  sex,
  culmen_length_mm,
  culmen_depth_mm,
  flipper_length_mm,
  body_mass_g,
  IF(MOD(ABS(FARM_FINGERPRINT(TO_JSON_STRING(p))), 10) < 8, 'treino', 'teste') AS split
FROM `bigquery-public-data.ml_datasets.penguins` AS p
WHERE culmen_length_mm IS NOT NULL
  AND culmen_depth_mm IS NOT NULL
  AND flipper_length_mm IS NOT NULL
  AND body_mass_g IS NOT NULL;
