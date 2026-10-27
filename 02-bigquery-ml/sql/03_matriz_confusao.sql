-- Onde o modelo confunde uma espécie com outra. Linhas = real, colunas = previsto.
SELECT *
FROM ML.CONFUSION_MATRIX(
  MODEL `gdg_blumenau.pinguins_especie`,
  (
    SELECT species, culmen_length_mm, culmen_depth_mm, flipper_length_mm, body_mass_g
    FROM `gdg_blumenau.pinguins_base`
    WHERE split = 'teste'
  )
);
