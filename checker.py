import pandas as pd
import numpy as np
import json

class DataHealthChecker:
    def __init__(self, df):
        self.df = df
        self.report = {}

    def check_missing_data(self):
        """Analisa valores ausentes e sugere tratamentos."""
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        analysis = {}
        for col in self.df.columns:
            if missing[col] > 0:
                # Lógica de sugestão
                suggestion = "Remover linhas" if missing_pct[col] > 50 else "Imputar com Mediana/Média"
                analysis[col] = {
                    "missing_count": int(missing[col]),
                    "percentage": round(missing_pct[col], 2),
                    "suggestion": suggestion
                }
        self.report["missing_values"] = analysis

    def detect_outliers_iqr(self):
        """Detecta outliers em colunas numéricas usando o método IQR."""
        outliers_report = {}
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            count = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
            if count > 0:
                outliers_report[col] = {
                    "outlier_count": int(count),
                    "bounds": (round(lower_bound, 2), round(upper_bound, 2))
                }
        self.report["outliers"] = outliers_report

    def save_report_json(self, filename="health_report.json"):
        """Exporta o diagnóstico para JSON (bom para portfólio NoSQL)."""
        with open(filename, 'w') as f:
            json.dump(self.report, f, indent=4)
        print(f"Relatório salvo com sucesso em {filename}")

# Exemplo de uso:
data = {
    'id_entrega': [1, 2, 2, 4, 5], # ID 2 duplicado
    'valor_frete': [25.0, 1000.0, 15.0, np.nan, 20.0], # 1000 é outlier, um NaN
    'vendedor': ['Shopee', 'ML', 'Shopee', 'ML', 'Shopee']
}

df_test = pd.DataFrame(data)

# Executando a auditoria
checker = DataHealthChecker(df_test)
checker.check_missing_data()
checker.detect_outliers_iqr()
checker.save_report_json()

print("Análise concluída. Verifique o arquivo JSON gerado.")