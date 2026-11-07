# Data documentation

Reference for reading and interpreting **Default of Credit Card Clients**. Follow the [setup guide](setup.md) to download the dataset and run the analysis.

## Source and license

- Official source: [UCI, dataset 350](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients).
- Creator: I-Cheng Yeh. DOI: [10.24432/C55S3H](https://doi.org/10.24432/C55S3H).
- Dataset license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribute the source when sharing data or results.
- Citation: Yeh, I. (2009). *Default of Credit Card Clients* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H.
- Introductory paper: I. Yeh and Che-hui Lien (2009), *The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients*, Expert Systems with Applications.

The dataset concerns credit card clients in Taiwan and next-month default classification. Monthly observations cover April–September 2005. The UCI donation date, January 25, 2016, is not the observation period.

## File format and loading

Local path: `data/default_of_credit_card_clients.xls`. Worksheet: `Data`.
Reference SHA-256:

```text
30c6be3abd8dcfd3e6096c828bad8c2f011238620f5369220bd60cfc82700933
```

The worksheet has two header rows: variable identifiers followed by descriptive names. Use `header=1` to read the 25 columns listed below.

```python
from pathlib import Path
import pandas as pd

# Run from the project root; from notebooks/, use ../data/ instead.
path = Path("data/default_of_credit_card_clients.xls")
df = pd.read_excel(path, sheet_name="Data", header=1, engine="calamine")
target = "default payment next month"
X = df.drop(columns=["ID", target])
y = df[target]
```

The project declares pandas and python-calamine as dependencies. `credit_default.paths.RAW_DATA_FILE` provides the shared XLS path relative to the repository root. Training reads the original XLS directly; no intermediate CSV or notebook export is required.

## Variable dictionary

Definitions and category codes follow the [UCI documentation](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients). Column names correspond to the worksheet's second row. Monetary amounts are in New Taiwan dollars (NT$), without currency conversion or inflation adjustment.

| UCI ID | Local column | Meaning / units |
| --- | --- | --- |
| ID | `ID` | Identifier; exclude from predictors |
| X1 | `LIMIT_BAL` | Credit granted, NT$; includes individual and supplementary family credit |
| X2 | `SEX` | Sex: 1 = male, 2 = female |
| X3 | `EDUCATION` | Education: 1 = graduate school, 2 = university, 3 = high school, 4 = other |
| X4 | `MARRIAGE` | Marital status: 1 = married, 2 = single, 3 = other |
| X5 | `AGE` | Age in years |
| X6 | `PAY_0` | Repayment status, September 2005 |
| X7 | `PAY_2` | Repayment status, August 2005 |
| X8 | `PAY_3` | Repayment status, July 2005 |
| X9 | `PAY_4` | Repayment status, June 2005 |
| X10 | `PAY_5` | Repayment status, May 2005 |
| X11 | `PAY_6` | Repayment status, April 2005 |
| X12 | `BILL_AMT1` | Statement balance, September 2005, NT$ |
| X13 | `BILL_AMT2` | Statement balance, August 2005, NT$ |
| X14 | `BILL_AMT3` | Statement balance, July 2005, NT$ |
| X15 | `BILL_AMT4` | Statement balance, June 2005, NT$ |
| X16 | `BILL_AMT5` | Statement balance, May 2005, NT$ |
| X17 | `BILL_AMT6` | Statement balance, April 2005, NT$ |
| X18 | `PAY_AMT1` | Payment amount, September 2005, NT$ |
| X19 | `PAY_AMT2` | Payment amount, August 2005, NT$ |
| X20 | `PAY_AMT3` | Payment amount, July 2005, NT$ |
| X21 | `PAY_AMT4` | Payment amount, June 2005, NT$ |
| X22 | `PAY_AMT5` | Payment amount, May 2005, NT$ |
| X23 | `PAY_AMT6` | Payment amount, April 2005, NT$ |
| Y | `default payment next month` | Target: 1 = default, 0 = no default in the next month |

For `PAY_0`, `PAY_2`, …, `PAY_6`, UCI defines −1 as payment on time; 1–8 as delay in months; and 9 as delay of nine months or more. The source page does not define the observed codes −2 and 0. Do not assign meanings to them without an additional source. Code 9 is documented but absent from the reference file.

There is no `PAY_1`. The latest period is `PAY_0`, aligned by month with `BILL_AMT1` and `PAY_AMT1`; subsequent indices move backward in time. October 2005 as the target month is an inference from the observation window and target name. UCI does not specify an operational default threshold in days on the dataset page.

## Notebook conventions

The dictionary uses original XLS column names. The repository notebook trims surrounding whitespace, converts names to lowercase, and replaces spaces with underscores: `LIMIT_BAL` becomes `limit_bal`, and the target becomes `default_payment_next_month`.

## Undocumented codes and interpretation

The file also contains `EDUCATION` codes 0, 5, and 6; `MARRIAGE` code 0; and repayment status codes −2 and 0. UCI does not explain these codes on the dataset page. Preserve them without assigning unsupported meanings.

Statement balances can be negative and payments can be zero; these values are not automatically missing data. Integer storage does not imply that category codes are quantitative measurements.
