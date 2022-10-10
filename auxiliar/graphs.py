import os
import matplotlib as mpl
if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

runs = [0, 2, 3, 4, 5]
legend_properties = {'size': 8}

plt.figure(figsize=(5, 5))
plt.subplot(211)
plt.plot(runs, [0.7999, 0.7917, 0.7896, 0.7828, 0.7907], '--C0o',
         runs, [0.6709, 0.7823, 0.7783, 0.7777, 0.7724], '--C1s',
         runs, [0.6363, 0.5626, 0.5980, 0.5664, 0.5822], '--C2^', linewidth=0.7, markersize=5)
plt.legend(['PGR-crowd', 'DDI', 'BC5CDR'], prop=legend_properties, bbox_to_anchor=(0, 1.02, 1, 0.2),
           loc="lower left", borderaxespad=0, mode="expand", ncol=3, frameon=False)
plt.ylabel('Accuracy', fontsize=8, weight='bold')
plt.margins(x=0, tight=True)
plt.ylim(0.5, 0.9)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.subplot(212)
plt.plot(runs, [0.7462, 0.7100, 0.7081, 0.7116, 0.7100], '--C0o',
         runs, [0.7168, 0.7930, 0.7901, 0.7892, 0.7847], '--C1s',
         runs, [0.6289, 0.5567, 0.5816, 0.5704, 0.5354], '--C2^', linewidth=0.7, markersize=5)
plt.ylabel('F-measure', fontsize=8, weight='bold')
plt.xlabel('Targeted knowledge added entities', fontsize=8, weight='bold')
plt.margins(x=0, tight=True)
plt.ylim(0.5, 0.9)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.savefig('tk.png', bbox_inches='tight')

plt.figure(figsize=(5, 5))
plt.subplot(211)
plt.plot(runs, [0.7999, 0.7962, 0.7968, 0.7939, 0.7978], '--C0o',
         runs, [0.6709, 0.8788, 0.8783, 0.8702, 0.8682], '--C1s',
         runs, [0.6363, 0.6237, 0.6498, 0.6079, 0.6271], '--C2^', linewidth=0.7, markersize=5)
plt.legend(['PGR-crowd', 'DDI', 'BC5CDR'], prop=legend_properties, bbox_to_anchor=(0, 1.02, 1, 0.2),
           loc="lower left", borderaxespad=0, mode="expand", ncol=3, frameon=False)
plt.ylabel('Accuracy', fontsize=8, weight='bold')
plt.margins(x=0, tight=True)
plt.ylim(0.5, 0.9)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.subplot(212)
plt.plot(runs, [0.7462, 0.7367, 0.7271, 0.7194, 0.7227], '--C0o',
         runs, [0.7168, 0.8690, 0.8660, 0.8610, 0.8587], '--C1s',
         runs, [0.6289, 0.6228, 0.6428, 0.6066, 0.6245], '--C2^', linewidth=0.7, markersize=5)
plt.ylabel('F-measure', fontsize=8, weight='bold')
plt.xlabel('Contextual knowledge added entities', fontsize=8, weight='bold')
plt.margins(x=0, tight=True)
plt.ylim(0.5, 0.9)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.savefig('ck.png', bbox_inches='tight')
