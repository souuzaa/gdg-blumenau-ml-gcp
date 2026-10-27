-- Treina uma regressão logística multiclasse só com as linhas de treino.
-- Leva em torno de um minuto. O slide da talk mostra uma versão resumida desta query.
CREATE OR REPLACE MODEL `gdg_blumenau.pinguins_especie`
OPTIONS (
  model_type = 'LOGISTIC_REG',
  input_label_cols = ['species'],
  data_split_method = 'NO_SPLIT'  -- o split já foi feito na view
) AS
SELECT
  species,
  culmen_length_mm,
  culmen_depth_mm,
  flipper_length_mm,
  body_mass_g
FROM `gdg_blumenau.pinguins_base`
WHERE split = 'treino';
