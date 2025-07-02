import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

# 日本語フォントの設定（お使いの環境に合わせて適宜調整してください）
font_name = 'YuGothic'  # Windowsの場合
try:
    fm.findfont(font_name, fontext='ttf')
except ValueError:
    print(f"Warning: Font '{font_name}' not found. Trying common fallback fonts.")
    if 'Windows' in plt.get_backend():
        font_name = 'MS Gothic'
    elif 'Darwin' in plt.get_backend():
        font_name = 'Hiragino Sans GB'
    else:
        font_name = 'IPAexGothic'
    try:
        fm.findfont(font_name, fontext='ttf')
    except ValueError:
        print(f"Error: No suitable Japanese font found. Please install one or specify manually.")
        font_name = 'DejaVu Sans'

plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False # マイナス記号を正しく表示するため

# 所得税の速算表データ
brackets = [
    (1_000, 1_949_000, 0.05, 0),
    (1_950_000, 3_299_000, 0.10, 97_500),
    (3_300_000, 6_949_000, 0.20, 427_500),
    (6_950_000, 8_999_000, 0.23, 636_000),
    (9_000_000, 17_999_000, 0.33, 1_536_000),
    (18_000_000, 39_999_000, 0.40, 2_796_000),
    (40_000_000, np.inf, 0.45, 4_796_000)
]

# 各課税所得に対する税額を計算する関数
def calculate_tax(income):
    if income <= 0: # 所得が0以下の場合は税額も0
        return 0
    for lower, upper, rate, deduction in brackets:
        if lower <= income <= upper:
            return income * rate - deduction
        elif income > upper and upper != np.inf:
            pass
    if income > brackets[-2][1]: # 最高税率区間
        rate = brackets[-1][2]
        deduction = brackets[-1][3]
        return income * rate - deduction
    return 0

# プロット用の所得と実効税率のリスト
x_max = 45_000_000 # X軸の最大値
# 所得が低すぎると実効税率の計算が不安定になるため、開始点を少し上げる
x_values = np.linspace(10_000, x_max, 500) # 1万円から4500万円まで500点

plot_incomes = []
plot_effective_rates = []

for income in x_values:
    tax_amount = calculate_tax(income)
    if income > 0: # 分母が0にならないようにチェック
        effective_rate = (tax_amount / income) * 100
        plot_incomes.append(income)
        plot_effective_rates.append(effective_rate)

# グラフの作成
plt.figure(figsize=(12, 7))

# 実効税率のグラフ
plt.plot(plot_incomes, plot_effective_rates, linestyle='-', color='red', label='実効税率')

# 軸ラベルとタイトル
plt.xlabel('課税される所得金額 (円)', fontsize=14)
plt.ylabel('実効税率 (%)', fontsize=14)
plt.title('所得金額に対する実効税率の推移', fontsize=16)

# グリッドの表示
plt.grid(True, linestyle='--', alpha=0.7)

# X軸の目盛りのフォーマット（円表示）
formatter_x = plt.FuncFormatter(lambda x, p: format(int(x), ','))
plt.gca().xaxis.set_major_formatter(formatter_x)
plt.xticks(np.arange(0, x_max + 1, 5_000_000))

# Y軸の目盛りのフォーマット（%表示）
formatter_y = plt.FuncFormatter(lambda y, p: f'{y:.1f}%')
plt.gca().yaxis.set_major_formatter(formatter_y)

# Y軸の表示範囲を調整（0%から最高税率+αまで）
plt.ylim(0, 45) # 最高税率が45%なので、少し余裕を持たせる

# 凡例の表示
plt.legend(fontsize=12)

# 各税率区間の境界にテキストで名目税率を表示（任意）
# 実効税率のグラフ上に表示するのは少し複雑になるため、ここでは省略します。
# グラフの傾きが急に変わる場所が税率区間の境界に当たります。

plt.tight_layout()
plt.show()