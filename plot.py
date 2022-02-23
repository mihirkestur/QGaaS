import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("logs.csv")

plt.xlabel('Frame numbers')
plt.ylabel('Similarity ratio')

plt.title("Similarity ratio comparison with respect to previous frames")

plt.plot(df["similarity"], ls = '-')

plt.show()