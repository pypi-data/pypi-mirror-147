from src.so4gp import so4gp

out_json, gps = so4gp.graank('c2k.csv', return_gps=True)
print(gps)
