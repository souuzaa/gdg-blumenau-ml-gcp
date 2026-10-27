-- Previsão para um pinguim que não está na tabela.
SELECT
  predicted_species AS especie_prevista,
  predicted_species_probs AS probabilidades
FROM ML.PREDICT(
  MODEL `gdg_blumenau.pinguins_especie`,
  (
    SELECT
      45.0 AS culmen_length_mm,
      15.5 AS culmen_depth_mm,
      215.0 AS flipper_length_mm,
      5000.0 AS body_mass_g
  )
);
