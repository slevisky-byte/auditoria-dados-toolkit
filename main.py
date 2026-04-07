from checker import DataHealthChecker
import pandas as pd

# 1. Carregue seu arquivo (pode ser um CSV que você tenha ou o exemplo abaixo)
df = pd.read_csv("seu_arquivo.csv") 

# 2. Execute a auditoria
checker = DataHealthChecker(df)
checker.check_missing_data()
checker.detect_outliers_iqr()

# 3. Gere o relatório
checker.save_report_json("diagnostico_final.json")s