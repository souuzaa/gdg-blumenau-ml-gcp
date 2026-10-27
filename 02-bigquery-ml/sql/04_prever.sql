-- Previsões no conjunto de teste, das menos confiantes para as mais confiantes.
-- Os casos do topo são os mais interessantes de olhar.
SELECT
  species AS especie_real,
  predicted_species AS especie_prevista,
  ROUND((
    SELECT prob FROM UNNEST(predicted_species_probs) WHERE label = predicted_species
  ), 3) AS confianca,
  culmen_length_mm,
  culmen_depth_mm,
  flipper_length_mm,
  body_mass_g
FROM ML.PREDICT(
  MODEL `gdg_blumenau.pinguins_especie`,
  (
    SELECT species, culmen_length_mm, culmen_depth_mm, flipper_length_mm, body_mass_g
    FROM `gdg_blumenau.pinguins_base`
    WHERE split = 'teste'
  )
)
ORDER BY confianca
LIMIT 20;
