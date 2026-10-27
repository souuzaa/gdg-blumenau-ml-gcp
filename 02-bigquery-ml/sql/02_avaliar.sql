-- Avalia o modelo em pinguins que ele nunca viu (split = 'teste').
SELECT *
FROM ML.EVALUATE(
  MODEL `gdg_blumenau.pinguins_especie`,
  (
    SELECT species, culmen_length_mm, culmen_depth_mm, flipper_length_mm, body_mass_g
    FROM `gdg_blumenau.pinguins_base`
    WHERE split = 'teste'
  )
);
