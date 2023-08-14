import pandas as pd
import numpy as np
import pulp
import typing as tp

class ScheduleOptimizer():
    @property
    def request_table(self) -> np.ndarray:
        return self.df_request_table.values.T
    
    @property
    def members(self) -> list[str]:
        return list(self.df_request_table.index)
    
    @property
    def days(self) -> list[int]:
        return list(self.df_request_table.columns)
    
    @property
    def n_member_day(self) -> int:
        return self.n_member_day_

    def __init__(self, df_request_table:pd.DataFrame, n_member_day:int) -> None:
        self.df_request_table:pd.DataFrame = df_request_table
        self.n_member_day_:int = n_member_day

    def optimize(self) -> pd.DataFrame:
        df_schedule:pd.DataFrame = pd.DataFrame(columns=self.days, index=np.arange(self.n_member_day))

        # 問題定義
        problem = pulp.LpProblem("schedule", sense=pulp.LpMaximize)

        # 変数定義
        x_dm = [[pulp.LpVariable(f"x_{m}{d}", cat=pulp.LpBinary) for m in self.members] for d in self.days]

        # 目的関数定義
        problem += pulp.lpSum([pulp.lpDot(self.request_table[i], x_dm[i]) for i in range(len(self.days))])

        # 制約関数定義
        for i, d in enumerate(self.days):
            problem += pulp.lpSum(x_dm[i]) == self.n_member_day

        for j, m in enumerate(self.members):
            problem += pulp.lpSum(list(zip(*x_dm))[j]) >= self.n_member_day * len(self.days) // len(self.members)
            problem += pulp.lpSum(list(zip(*x_dm))[j]) <= self.n_member_day * len(self.days) // len(self.members) + 1

        # 解決
        problem.solve()

        # 最適化結果から、シフトを作成
        shift = [list(map(lambda x: int(x.value()), x_d)) for x_d in x_dm]
        for i, d in enumerate(self.days):
            df_schedule[d] = [self.members[j] for j, x in enumerate(shift[i]) if x == 1]

        return df_schedule

# TODO :サンプルcsvを作るだけなので、他に移動したい。
def generate_sample_csv() -> tp.Union[int, pd.DataFrame]:
    n = 4  # 一度に入る人数

    members = ["A", "B", "C", "D", "E", "F", "G"]  # 　入る人
    days = np.arange(1, 31)  # 入る日

    df = pd.DataFrame(index=members, columns=days)

    # TODO:より高速な処理に変更したい。
    for index, row in df.iterrows():
        df.loc[index] = np.random.randint(low=1, high=n+1, size=len(days))

    df.to_csv("sample.csv")

    return n, df

if __name__ == "__main__":
    n, df = generate_sample_csv()

    opt = ScheduleOptimizer(df, n)
    df_schedule = opt.optimize()