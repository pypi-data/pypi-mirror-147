from src.so4gp import so4gp

out_json, gps = so4gp.graank('DATASET.csv', return_gps=True)
print(gps)
