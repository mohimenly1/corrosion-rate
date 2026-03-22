# Detailed Academic Report
## Development of a Predictive Corrosion Rate Model Based on Sodium Chloride Data Using a Power-Law and Arrhenius Formulation

---

## Title Page

**Project Title:**  
Development of an Intelligent System for Corrosion Rate Modeling and Prediction in Metallic Materials Using Experimental Data and a Multi-Interface Application

**Scientific Scope of This Report:**  
Development and validation of a predictive corrosion-rate model for `NaCl` samples using a power-law and Arrhenius-based formulation

**Prepared by:**  
Student / .....................................

**Supervised by:**  
Professor / .....................................

**Department:**  
.....................................

**University:**  
.....................................

**Date:**  
March 22, 2026

---

## Abstract

This report presents the development of a predictive corrosion-rate model based on an experimental dataset of fifty observations associated with sodium chloride concentration, temperature, and pH. The work was motivated by the need to move beyond an initial fixed empirical equation toward a data-derived predictive model with clearer physical interpretation and stronger statistical validity. Accordingly, the following model structure was adopted:

```text
CR = A × [Cl⁻]^b × exp(-K / Tₖ) × exp(c × pH)
```

where `CR` is the corrosion rate in `mm/yr`, `[Cl⁻]` represents chloride concentration in equivalent `NaCl` weight percent, `Tₖ` is the absolute temperature in Kelvin, and `A`, `b`, `K`, and `c` are model parameters estimated directly from data.

The model was linearized by taking the natural logarithm of both sides and was first fitted through multiple linear regression in the transformed domain. A nonlinear least-squares fitting stage was then implemented to evaluate the original nonlinear form. To ensure scientific rigor, the dataset was split into a training subset of 30 samples and a testing subset of 20 samples. Model performance was assessed using `R²`, `RMSE`, and `MAE`.

The results showed that the log-linearized model provided superior generalization on the unseen testing subset compared with the nonlinear alternative. The selected final model achieved `R² = 0.9606`, `RMSE = 0.6837 mm/yr`, and `MAE = 0.2723 mm/yr` on the test set. In addition, regression coefficients exhibited strong statistical significance through very low `p-values`. The final model was integrated into the operational software system at both backend and interface levels, converting the platform from a fixed-form calculator into a practical data-driven predictive tool.

---

## 1. Introduction

Corrosion is one of the most critical challenges affecting oil and gas facilities, petrochemical systems, transport infrastructure, storage assets, and metallic process equipment. Its consequences include direct economic losses, maintenance burden, safety risks, and environmental exposure. In oil and gas applications, quantitative corrosion modeling is particularly important because material selection, preventive maintenance planning, and operational risk assessment all depend on the ability to estimate material behavior under varying service conditions.

The initial version of the project relied on a fixed multi-factor empirical formulation that was useful for illustrating the general multiplicative structure of corrosion-rate estimation. However, such a formulation does not constitute a genuine predictive model because its coefficients are imposed a priori rather than derived from measured data. This motivated the development of a stronger model that combines physical interpretability with direct statistical estimation from experimental observations.

Based on this premise, a predictive model was constructed from real `NaCl` corrosion data using a structure that combines a power-law chloride term, an Arrhenius-type thermal term, and an exponential pH term. The model was then tested on unseen data to evaluate predictive performance rather than merely fit quality on the training subset.

---

## 2. Research Problem

The central problem addressed in this work is that a fixed empirical equation with manually imposed coefficients does not adequately satisfy the scientific objective of building a predictive corrosion model derived from actual experimental data and capable of representing the influence of the following key variables:

- chloride concentration
- temperature
- pH

The core scientific question is therefore:

**How can a predictive corrosion-rate model be constructed from real data in a way that remains physically interpretable and statistically valid on unseen observations?**

---

## 3. Objectives

This study aims to:

1. Replace the initial fixed empirical equation with a predictive, data-driven model.
2. Adopt a mathematically and physically meaningful model structure for chloride concentration, temperature, and pH effects.
3. Estimate model parameters directly from experimental data rather than assigning them manually.
4. Demonstrate statistical significance of the model coefficients using appropriate indicators such as `p-values`.
5. Validate predictive capability using a `train/test split`.
6. Integrate the resulting model into the software system so that it operates within the application rather than remaining an isolated analytical exercise.

---

## 4. Theoretical Basis

### 4.1 Temperature Effect

Corrosion behavior often exhibits temperature sensitivity of exponential type. An Arrhenius-style expression is commonly used to represent this dependence, leading to the thermal term:

```text
exp(-K / Tₖ)
```

where `K` represents the simplified thermal coefficient corresponding to `Eₐ / R` in the adopted formulation.

### 4.2 Chloride Effect

Chloride is widely recognized as a corrosion-promoting species in saline aqueous environments. Its effect was therefore represented by a power-law term:

```text
[Cl⁻]^b
```

This form allows the dataset to determine whether the chloride effect is weak, moderate, or strongly nonlinear.

### 4.3 pH Effect

pH is a major controlling variable in electrochemical corrosion behavior because it influences surface film stability and reaction kinetics. To capture this influence in a mathematically tractable form, an exponential representation was adopted:

```text
exp(c × pH)
```

The sign and magnitude of `c` determine whether increasing pH raises or lowers the corrosion rate within the observed domain.

---

## 5. Adopted Mathematical Model

The adopted predictive model is:

```text
CR = A × [Cl⁻]^b × exp(-K / Tₖ) × exp(c × pH)
```

where:

- `CR`: corrosion rate in `mm/yr`
- `[Cl⁻]`: chloride concentration expressed as `NaCl` weight percent
- `Tₖ`: temperature in Kelvin, where `Tₖ = T°C + 273.15`
- `A`: global calibration constant
- `b`: chloride exponent
- `K`: Arrhenius-related thermal coefficient
- `c`: pH coefficient

This model offers three important advantages:

1. It preserves physical interpretability.
2. Its coefficients can be estimated directly from data.
3. It can be linearized for robust initial estimation.

---

## 6. Model Linearization

To obtain reliable initial parameter estimates, the natural logarithm of both sides was taken:

```text
ln(CR) = ln(A) + b × ln([Cl⁻]) - K × (1 / Tₖ) + c × pH
```

This transforms the problem into a multiple linear regression problem where:

- the dependent variable is `ln(CR)`
- the predictors are:
  - `ln([Cl⁻])`
  - `1 / Tₖ`
  - `pH`

This step is methodologically important because it:

- converts the original model into a linear estimable form
- provides statistically grounded initial coefficients
- establishes the starting point for nonlinear fitting

---

## 7. Dataset

The model was built using the dataset:

`NaCl_50samples_corrosion_table_with_sources.csv`

The file contains fifty experimental samples directly related to sodium chloride conditions and includes the following fields:

- `NaCl (wt%)`
- `Temperature (°C)`
- `pH`
- `Estimated Corrosion Rate (mm/yr)`

### 7.1 Data Characteristics

The effective dataset used in training had the following characteristics:

- valid rows used: `50`
- minimum `NaCl`: `0.05 wt%`
- maximum `NaCl`: `10.00 wt%`
- minimum `pH`: `2.5`
- maximum `pH`: `9.0`
- minimum corrosion rate: `0.0016 mm/yr`
- maximum corrosion rate: `14.6544 mm/yr`

This wide range is valuable because it enables the model to capture both mild and aggressive corrosion regimes.

---

## 8. Data Processing

The data were processed using the following steps:

1. The CSV file was loaded using `pandas`.
2. Core columns were converted to numeric values.
3. Only invalid rows were removed.
4. Only rows with:
   - `NaCl > 0`
   - `CR > 0`
   were retained.
5. Temperature was converted from Celsius to Kelvin.

### 8.1 Treatment of Extreme Values

High corrosion-rate observations were treated as valid aggressive-condition samples rather than undesirable outliers. Accordingly:

- high-rate cases were retained
- no aggressive-condition observations were discarded
- the full observed response range was preserved for both training and validation

This decision was necessary to ensure that the model remained representative of realistic severe conditions.

---

## 9. Training and Validation Strategy

### 9.1 Data Split

The dataset was divided into:

- `30` training samples
- `20` testing samples

using:

```text
random_seed = 42
```

to preserve reproducibility.

### 9.2 Evaluation Metrics

The following metrics were used:

- `R²`: coefficient of determination
- `RMSE`: root mean square error in `mm/yr`
- `MAE`: mean absolute error

---

## 10. Fitting Procedure

### 10.1 Initial Linearized Fit

The first stage estimated the model parameters from the transformed linear equation:

```text
ln(CR) = ln(A) + b × ln([Cl⁻]) - K × (1 / Tₖ) + c × pH
```

The resulting initial estimates were:

- `A = 6,669,627.2015`
- `b = 0.1746906708`
- `K = 3834.6929348`
- `c = -0.9002988986`

### 10.2 Nonlinear Fit

A nonlinear least-squares fitting stage was then performed using a custom nonlinear optimization procedure initialized from the linearized solution. This stage evaluated the original model form directly on `CR` values rather than only on the logarithmic transformation.

### 10.3 Final Model Selection

Model selection was based on a clear rule:

**The final model was chosen as the model with the lower test-set RMSE on unseen data.**

Accordingly, the log-linearized model was selected as the final operational model because it generalized better than the nonlinear alternative on the test subset.

---

## 11. Statistical Results

### 11.1 Final Selected Parameters

The final selected model parameters were:

- `A = 6669627.201485091`
- `b = 0.1746906708229655`
- `K = 3834.6929347967016`
- `c = -0.900298898552911`

### 11.2 Performance of the Final Model

#### Training Set

- `R² = 0.9832`
- `RMSE = 0.3610 mm/yr`
- `MAE = 0.1079 mm/yr`

#### Test Set

- `R² = 0.9606`
- `RMSE = 0.6837 mm/yr`
- `MAE = 0.2723 mm/yr`

#### Full Dataset

- `R² = 0.9719`
- `RMSE = 0.5149 mm/yr`
- `MAE = 0.1736 mm/yr`

### 11.3 Nonlinear Model for Comparison

The nonlinear candidate model produced:

#### Training Set

- `R² = 0.9987`
- `RMSE = 0.0996 mm/yr`

#### Test Set

- `R² = 0.8832`
- `RMSE = 1.1765 mm/yr`

This indicates that although the nonlinear model fit the training data more closely, it generalized less effectively on unseen test data, suggesting a greater tendency toward overfitting in this dataset.

---

## 12. Statistical Significance of the Coefficients

The linearized regression summary produced the following key results:

### 12.1 Intercept `ln(A)`

- coefficient: `15.713075`
- standard error: `0.786267`
- `t-stat`: `19.9844`
- `p-value`: `0.0`

### 12.2 Chloride Coefficient `b`

- coefficient: `0.174691`
- standard error: `0.039627`
- `t-stat`: `4.4083`
- `p-value`: `0.00001`

### 12.3 Thermal Coefficient Associated with `1/Tₖ`

- coefficient: `-3834.692935`
- standard error: `233.275167`
- `t-stat`: `-16.4385`
- `p-value`: `0.0`

### 12.4 pH Coefficient

- coefficient: `-0.900299`
- standard error: `0.020729`
- `t-stat`: `-43.4312`
- `p-value`: `0.0`

### 12.5 Interpretation

These results indicate strong statistical significance of the model coefficients because:

- the absolute `t-stat` values are high
- the `p-values` are extremely small

This supports the adopted model not only numerically, but also statistically.

---

## 13. Scientific Discussion

### 13.1 Interpretation of the Chloride Exponent

The chloride exponent `b` is positive in the selected model, indicating that increasing chloride concentration is associated with an increase in corrosion rate within the studied range. This is fully consistent with the known role of chlorides in accelerating corrosion in saline environments.

### 13.2 Interpretation of the Thermal Term

The thermal component `exp(-K / Tₖ)` produces temperature-dependent exponential behavior consistent with Arrhenius-type kinetics. This supports the physical plausibility of the adopted model structure.

### 13.3 Interpretation of the pH Term

The pH coefficient is negative, indicating that increasing pH within the studied domain is associated with lower corrosion rates. This is reasonable in many environments where acidity intensifies corrosive attack.

### 13.4 Why the Nonlinear Model Was Not Selected

The nonlinear model was not rejected because it was mathematically invalid. Rather, it was not selected because its predictive performance on unseen test data was weaker than that of the linearized model. Therefore, the final choice was based on generalization quality rather than training-set fit alone.

---

## 14. Completeness of the Adopted Methodology

The present work satisfies the essential elements required for a scientifically defensible predictive corrosion model:

### 14.1 Replacement of the Fixed Equation

The original fixed empirical equation was replaced by a model whose coefficients were estimated directly from data.

### 14.2 Adoption of a Physically Meaningful Structure

The selected equation combines a power-law chloride effect, an Arrhenius-type thermal effect, and an exponential pH effect.

### 14.3 Logarithmic Transformation

The model was linearized and estimated in transformed form to generate robust initial parameter values.

### 14.4 Suitability of the Dataset

The training data did not contain zero chloride values, and the minimum chloride concentration was `0.05 wt%`, making `ln([Cl⁻])` well-defined.

### 14.5 Retention of High Corrosion Values

High-rate observations were preserved and not removed, ensuring representation of aggressive conditions.

### 14.6 Linear Regression Stage

Multiple linear regression was performed and coefficient significance was quantified.

### 14.7 Nonlinear Regression Stage

Nonlinear fitting was implemented and evaluated on the original model form.

### 14.8 Validation on Unseen Data

A `30/20` train-test split was applied and model selection was based on test-set performance.

### 14.9 Performance Metrics

`R²`, `RMSE`, and `MAE` were computed and retained as part of the final model record.

---

## 15. Integration into the Software System

The work was not limited to theoretical analysis. The final model was integrated into the software system through:

- a model training layer
- a backend calculation service
- a persisted model file
- API endpoints for inference and model inspection
- application interfaces that display the selected equation, fit method, and evaluation metrics

Thus, the project now combines:

1. scientific modeling
2. statistical validation
3. practical software integration

---

## 16. Strengths of the Work

The main strengths of the work can be summarized as follows:

- transition from a fixed equation to a data-driven predictive model
- adoption of a physically interpretable model form
- use of real experimental data
- retention of aggressive-condition observations
- validation on unseen data
- explicit reporting of predictive performance metrics
- statistical significance assessment of the coefficients
- comparison between linearized and nonlinear fitting
- final model selection based on test-set performance
- deployment of the model into a functional application

---

## 17. Current Scientific Limitations

The current study also has clearly identifiable boundaries:

- the present model is based on a fifty-sample `NaCl` dataset and would benefit from larger future datasets
- the model currently focuses on chloride concentration, temperature, and pH
- additional variables such as flow velocity, pressure, dissolved gases, exposure time, and surface condition may further improve future predictive capability

Nevertheless, the present work successfully fulfills the objective of constructing a statistically validated predictive model from real data.

---

## 18. Conclusion

This work demonstrated the feasibility of constructing a predictive corrosion-rate model from real experimental data using a mathematically interpretable structure combining chloride concentration, temperature, and pH effects. The project successfully moved from a fixed empirical equation to a trained predictive model, implemented both linearized and nonlinear fitting stages, validated performance on unseen test data, and selected the final model using objective predictive criteria.

The selected final model achieved:

- `R² = 0.9606`
- `RMSE = 0.6837 mm/yr`
- `MAE = 0.2723 mm/yr`

The model coefficients exhibited strong statistical significance, and the resulting model was integrated directly into the operational software system. The outcome is therefore a predictive model that is academically defensible and practically usable.

---

## 19. Future Recommendations

Future work may include:

1. expanding the dataset to include more observations and broader conditions
2. introducing additional explanatory variables such as flow, pressure, and dissolved gases
3. comparing the present formulation with alternative statistical or machine-learning models
4. performing external validation on independent datasets
5. expanding the interface with richer reporting and advanced visualization

---

## 20. List of Figures

### Figure 1: Main Web Dashboard

Main web-based corrosion platform showing server status, model status, and summary indicators.

### Figure 2: Corrosion Calculation Input Form

Web-based calculation form containing material type, temperature, pH, NaCl percentage, and medium.

### Figure 3: Calculation Result Using the Predictive Model

Calculation output showing corrosion rate in `mm/yr` and `mpy`, together with the adopted model information.

### Figure 4: CSV Upload Interface

Web-based upload interface used to import corrosion data as CSV files.

### Figure 5: Statistical Charts

Statistical visualizations showing corrosion rate versus pH, temperature, medium, and material comparison.

### Figure 6: Stored Data Table

Web-based data table showing stored samples and filterable corrosion records.

---

## 21. Appendix of Figures

### Figure 1: Main Web Dashboard

![Figure 1: Main Web Dashboard](images/01_dashboard_overview.png)

### Figure 2: Corrosion Calculation Input Form

![Figure 2: Corrosion Calculation Input Form](images/02_calculation_form.png)

### Figure 3: Calculation Result Using the Predictive Model

![Figure 3: Calculation Result Using the Predictive Model](images/03_calculation_result.png)

### Figure 4: CSV Upload Interface

![Figure 4: CSV Upload Interface](images/04_csv_upload.png)

### Figure 5: Statistical Charts

![Figure 5: Statistical Charts](images/06_statistics_charts.png)

### Figure 6: Stored Data Table

![Figure 6: Stored Data Table](images/07_samples_table.png)

---

## 22. Executive Conclusion

The original fixed empirical equation was replaced with a predictive model derived from fifty real `NaCl` corrosion samples using the formulation `CR = A × [Cl⁻]^b × exp(-K/Tₖ) × exp(c × pH)`. The model was linearized and fitted through multiple regression to obtain statistically significant initial parameters, then nonlinear fitting was implemented and evaluated. Using a `30/20` train-test split, the log-linearized model demonstrated superior generalization on unseen testing data, achieving `R² = 0.9606` and `RMSE = 0.6837 mm/yr`. High-rate aggressive-condition observations were retained rather than discarded, and the final model was integrated directly into the software system. 
